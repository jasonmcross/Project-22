import json

with open('example.json') as f:
    data = json.load(f)

for key, value in data.items():
    print(key)
    print()
    for s in value:
        print(s)
        print()
        print()
