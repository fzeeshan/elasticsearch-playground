#!/bin/bash

ES_HOST=""

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -es|--es-host)
	ES_HOST="$2"
    shift # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

if [[ -z "$ES_HOST" ]]; then
	echo "usage: build_index.sh --es-host <host>"
fi

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
