import json

try:
    with open('products.json', 'r') as json_file:
        data = json.load(json_file)
except Exception as E:
    data = {}



with open('products.json', 'w') as json_file:
    json.dump(data, json_file, indent = 4)

