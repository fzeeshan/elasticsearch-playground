#!/bin/bash

#ES_HOST = "http://ec2-54-165-225-95.compute-1.amazonaws.com"
ES_HOST="ec2-54-162-125-44.compute-1.amazonaws.com"
ES_PORT=9200
ES_HOSTNAME="${ES_HOST}:${ES_PORT}"
INDEX_NAME="reviews"

curl -XDELETE "${ES_HOSTNAME}/${INDEX_NAME}"
