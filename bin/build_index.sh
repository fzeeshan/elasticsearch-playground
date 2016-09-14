#!/bin/bash

ES_HOST="192.168.5.253"
ES_PORT=9200
ES_HOSTNAME="${ES_HOST}:${ES_PORT}"
INDEX_NAME="reviews"

curl -XPUT "${ES_HOSTNAME}/${INDEX_NAME}" -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 2,
            "number_of_replicas" : 1
        }
    }
}'
