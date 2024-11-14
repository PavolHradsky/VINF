import os
BASE_DIR = "data/wiki"

with open("data/wiki.csv", "w+") as f:
    for filename in os.listdir(BASE_DIR):
        if not filename.startswith("part-"): continue
        with open(f"{BASE_DIR}/{filename}", "r") as wikifile:
            for line in wikifile:
                line = line.replace('\x00', '')
                line = line.replace('\'\'\'', '')
                line = line.replace('""', '')
                # line = [x.split('\t') for x in line]
                f.write(line)
