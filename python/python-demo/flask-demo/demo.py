import json

with open('data.json',mode='r') as f:
    data = json.load(f)

print(data)