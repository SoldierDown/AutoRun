import os, json, uuid

filename = 'checklist.json'
with open(filename, 'r') as f:
    data = json.load(f)
    data['cars']["Nissan"] = "3rd"
    # add, remove, modify content

with open("latestchecklist.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=4)