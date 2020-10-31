#!/usr/bin/env python3

import json
import sys

# check for parameters
if(len(sys.argv) != 2):
    exit(2)

# get the file name
file_name = sys.argv[1]

with open(file_name) as f:
    data = json.load(f)

for i in data['data']:
    sys.stdout.write(str(i) + '\n')