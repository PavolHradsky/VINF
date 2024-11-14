import os

BASE_DIR = "data/wiki"

with open("data/extracted_usa.csv", "r") as extracted:
    data = extracted.readlines()[1:]
    data = [x.split('\t') for x in data]
    names = [x[1].replace("&amp;", "&") for x in data]
# print(names[0:10])

for filename in os.listdir(BASE_DIR):
    if not filename.startswith("part-"): continue
    
    with open(f"{BASE_DIR}/{filename}", "r") as wikifile:
        wikidata = wikifile.readlines()
        wikidata = [x.split('\t') for x in wikidata]
        print(wikidata[0][2])
        break

