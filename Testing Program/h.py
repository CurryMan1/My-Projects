import json

file = 'data.json'
data = json.load(open(file, 'r'))

print(data)
data['x'] = {'balance': 90}
print(data)
with open(file, 'w') as f:
    f.write(json.dumps(data, indent=2))
