#!/usr/bin/python

import json
import fileinput

data = {}
data['score'] = 0.0
data['output'] = ''

for line in fileinput.input():
        data['output'] += line

print json.dumps(data)
