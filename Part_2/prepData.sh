#!/usr/bin/env bash

# clear the database space
mongo prepNoSQL.js

# preprare the A dataset
curl https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.min.json --output A
python3 formatJson.py A | sed "s/\bFalse\b/'False'/g" | sed "s/\bTrue\b/'True'/g" > A.json
mongoimport -d corona -c A --legacy --file A.json

rm -rf A
rm -rf A.json

# preprare the B dataset
curl https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.min.json --output B 
python3 formatJson.py B > B.json 
mongoimport -d corona -c B --legacy B.json

rm -rf B
rm -rf B.json

# prepare the C dataset
curl https://opendata.ecdc.europa.eu/covid19/testing/json/ --output C.json
mongoimport -d corona -c C --legacy --file C.json --jsonArray

rm -rf C.json