#!/usr/bin/env python

import os
import sys
import json

from elasticsearch import Elasticsearch

import cli


if __name__ == "__main__":
    parser = cli.make_parser()
    parser.add_argument(
        "dirname", help="directory to read bulk index request files from")
    args = parser.parse_args()

    dirname = args.dirname
    filenames = [os.path.join(dirname, name) for name in os.listdir(dirname)]

    es = Elasticsearch([args.es_host])

    for fname in filenames:
        with open(fname) as f:
            bulk_data = [json.loads(line) for line in f]

        print("bulk indexing %s..." % fname)
        res = es.bulk(body=bulk_data)
