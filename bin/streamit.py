import os
import sys
import time
try:
    import ujson as json
except ImportError:
    import json

import argparse
from datetime import datetime

from item_lookup import enrich


def stream_json(fname):
    with open(fname) as f:
        for line in f:
            try:
                yield json.loads(line)
            except:
                continue


def convert_doc(doc):
    helpful = doc.get('helpful', (0, 0))
    count, total = helpful
    del doc['helpful']

    doc['helpful_count'] = count
    doc['helpful_total'] = total

    doc['category'] = category

    if 'reviewTime' in doc:
        try:
            date = doc['reviewTime']
            month, day, year = date.split()
            day = day.replace(',', '')
            dt = datetime(day=int(day), month=int(month), year=int(year))
            doc['reviewTime'] = dt.strftime('%Y-%m-%d')
        except Exception as e:
            del doc['reviewTime']

    return doc


def enrich_doc(doc):
    item_id = doc['asin']
    info = enrich(item_id)
    doc.update(info)


def make_parser():
    parser = cli.make_parser()
    parser.add_argument("input_file")
    parser.add_argument(
        "-b", "--batch-size",
        type=int, default=1000,
        help="size of indexing batches to write")
    parser.add_argument(
        "-e", "--enrich",
        action="store_true")
    parser.add_argument(
        "-lb", "--last-batch",
        type=int, default=0)
    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    fname = args.input_file
    category = '-'.join(fname.split('-')[:-1])

    stream = stream_json(fname)

    op_dict = {"create": {
        "_index": args.index_name,
        "_type":  args.type_name,
    }}

    batch_size = args.batch_size
    batch_num = 0

    try:
        os.mkdir(category)
    except OSError:
        print("Dir already exists: %s" % category)

        if not args.last_batch:
            sys.exit(0)

    # consume generator up to stopping point (last batch processed)
    # and resume after that.
    if args.last_batch:
        for _ in xrange(args.last_batch):
            for _ in xrange(batch_size):
                try:
                    stream.next()
                except StopIteration:
                    print("Consumed full data stream while reading to last batch %d" %
                            args.last_batch)
                    sys.exit(0)

            batch_num += 1


    lines = []
    for num, doc in enumerate(stream):
        try:
            doc = convert_doc(doc)
            if args.enrich:
                time.sleep(1)
                enrich_doc(doc)

            lines.append(json.dumps(op_dict))
            lines.append(json.dumps(doc))
        except Exception as e:
            print(e)
            continue

        if len(lines) == batch_size:
            name = "%s-bulk%d.json" % (category, batch_num)
            outname = os.path.join(category, name)
            with open(outname, 'w') as f:
                f.write('\n'.join(lines) + '\n')

            print('wrote batch %d to %s' % (batch_num, outname))
            batch_num += 1
            lines = []

    # Write any remaining lines
    if lines:
        name = "%s-bulk%d.json" % (category, batch_num)
        outname = os.path.join(category, name)
        with open(outname, 'w') as f:
            f.write('\n'.join(lines))

        print('wrote batch %d to %s' % (batch_num, outname))
