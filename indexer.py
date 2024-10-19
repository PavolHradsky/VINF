import json
import os
import re

result = []

if not os.path.exists("./data/indexer_usa.json"):
    with open("./data/extracted_usa.csv", "r") as extracted:
        for i, line in enumerate(extracted.readlines()):
            if i == 0:
                continue
            print(i)

            # words = line.split()
            line = line.lower()
            line = line.replace("\t", " ")
            line = line.replace(",", " ")
            line = line.replace(".", " ")
            line = line.replace("/", " ")
            line = line.replace(";", " ")
            line = line.replace("\"", " ")
            line = line.replace("\'", " ")
            line = line.replace("(", " ")
            line = line.replace(")", " ")
            line = line.replace("[", " ")
            line = line.replace("]", " ")
            line = line.replace("*", " ")
            line = line.replace(":", " ")
            line = line.replace("!", " ")
            line = line.replace("+", " ")
            line = line.replace("=", " ")
            words = line.split()
            id = int(words[0])
            words = words[1:]
        
            for word in words:
                if not any(x for x in result if x["word"] == word):
                    result.append({
                        "word": word,
                        "count": 1,
                        "documents": [
                            {
                                "id": id,
                                "count": 1
                            }
                        ]
                    })
                else:
                    the_word = next(x for x in result if x["word"] == word)
                    the_word["count"] += 1
                    if not any(x for x in the_word["documents"] if x["id"] == id):
                        the_word["documents"].append({
                            "id": id,
                            "count": 1
                        })
                    else:
                        the_document = next(x for x in the_word["documents"] if x["id"] == id)
                        the_document["count"] += 1

        # break

    # print(result)
    with open("./data/indexer_usa.json", "w+") as f:
        f.write(json.dumps(result, indent=2))

result = []
with open("./data/indexer_usa.json", "r") as f:
    result = json.loads(f.read())
    result = sorted(result, key=lambda x: x["count"], reverse=True)

with open("./data/indexer_usa.csv", "w+") as f:
    for i, word in enumerate(result):
        print(i)
        f.write(f"{i}\t{word['word']}\t{word['count']}")
        for doc in word["documents"]:
            f.write(f"\t{doc['id']}\t{doc['count']}")
        f.write("\n")