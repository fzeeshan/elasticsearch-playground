SOURCE=http://snap.stanford.edu/data/amazon/productGraph/categoryFiles

all: rebuild parse index

rebuild:
	./bin/delete-mapping.sh
	./bin/build_index.sh
	./bin/put_mappings.py

parse:
	python ./bin/streamit.py grocery-and-gourmet-food-5cores.json
	python ./bin/streamit.py android-apps-5cores.json
	python ./bin/streamit.py movies-and-tv-5cores.json
	python ./bin/streamit.py electronics-5cores.json
	#python ./bin/streamit.py cell-phones-and-accessories-5cores.json

index:
	python ./bin/bulk_index.py grocery-and-gourmet-food
	python ./bin/bulk_index.py android-apps
	python ./bin/bulk_index.py movies-and-tv
	python ./bin/bulk_index.py electronics
	#python ./bin/bulk_index.py cell-phones-and-accessories

get:
	wget $(SOURCE)/reviews_Grocery_and_Gourmet_Food_5.json.gz
	wget $(SOURCE)/reviews_Apps_for_Android_5.json.gz
	wget $(SOURCE)/reviews_Movies_and_TV_5.json.gz
	wget $(SOURCE)/reviews_Electronics_5.json.gz
	wget $(SOURCE)/reviews_Cell_Phones_and_Accessories_5.json.gz

extract:
	gunzip reviews_Grocery_and_Gourmet_Food_5.json.gz
	mv reviews_Grocery_and_Gourmet_Food_5.json grocery-and-gourmet-food-5cores.json
	gunzip reviews_Apps_for_Android_5.json.gz
	mv reviews_Apps_for_Android_5.json android-apps-5cores.json
	gunzip reviews_Movies_and_TV_5.json.gz
	mv reviews_Movies_and_TV_5.json movies-and-tv-5cores.json
	gunzip reviews_Electronics_5.json.gz
	mv reviews_Electronics_5.json electronics-5cores.json
	gunzip reviews_Cell_Phones_and_Accessories_5.json.gz
	mv reviews_Cell_Phones_and_Accessories_5.json cell-phones-and-accessories-5cores.json
