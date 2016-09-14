import argparse


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--es-host",
        help="ElasticSearch ip/dns")
    parser.add_argument(
        "-in", "--index-name",
        default="reviews",
        help="name of the index to index/query against")
    parser.add_argument(
        "-tn", "--type-name",
        default="review",
        help="name of the type to index/query against")
    return parser
