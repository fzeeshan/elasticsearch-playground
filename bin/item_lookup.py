"""
Product Advertising API:
    https://affiliate-program.amazon.com/gp/advertising/api/detail/faq.html

"""
import sys
import json

from amazon.api import AmazonAPI

import aws_access

amazon = AmazonAPI(aws_access.access_key, aws_access.secret_access_key, aws_access.associate_tag)


def lookup(item_id):
    product = amazon.lookup(ItemId=item_id)
    return product


def enrich(item_id):
    product = lookup(item_id)
    info = {}

    if product.title:
        info['title'] = product.title
    if product.brand:
        info['brand'] = product.brand
    if product.editorial_reviews:
        info['editorialReviews'] = product.editorial_reviews
    if product.list_price:
        info['price'] = product.list_price[0]
    if product.manufacturer:
        info['manufacturer'] = product.manufacturer
    if product.region:
        info['region'] = product.region
    if product.features:
        info['features'] = product.features

    return info


if __name__ == "__main__":
    item_id = sys.argv[1]
    info = enrich(item_id)
    print json.dumps(info, indent=4)
