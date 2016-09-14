#!/usr/bin/env python
import os
import sys
import json

from elasticsearch import Elasticsearch

import cli


if __name__ == "__main__":
    parser = cli.make_parser()
    parser.add_argument(
        "-m", "--mapping-file", default="review-mapping.json")
    args = parser.parse_args()

    fname = args.mapping_file
    with open(fname) as f:
        mapping = json.load(f)

    es = Elasticsearch([args.es_host])

    if not es.indices.exists(args.index_name):
        print("%s index DNE" % args.index_name)
        sys.exit(-1)

    existing = es.indices.get_mapping(index=args.index_name, doc_type=args.type_name)
    if existing:
        print("review type mappings already exist.")
        print(json.dumps(existing, indent=4))
        sys.exit(-1)

    es.indices.put_mapping(index=args.index_name, doc_type=args.type_name, body=mapping)
