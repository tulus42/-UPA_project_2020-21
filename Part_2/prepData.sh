#!/usr/bin/env bash

# clear the database space
mongo prepNoSQL.js

# preprare the A dataset
curl https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.min.json --output A
python3 formatJson.py A > A1.json
cat A1.json | sed "s/\bFalse\b/'False'/g" > A2.json
cat A2.json | sed "s/\bTrue\b/'True'/g" > A.json
mongoimport -d corona -c A --legacy --file A.json

rm -rf A
rm -rf A1.json
rm -rf A2.json
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