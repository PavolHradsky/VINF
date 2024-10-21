import json
import os
import re

from utils import tokenize
result = []
result_words = []

if not os.path.exists("./data/indexer_usa.json"):
    with open("./data/extracted_usa.csv", "r") as extracted:
        for i, line in enumerate(extracted.readlines()):
            if i == 0:
                continue
            print(i)

            words = tokenize(line)
            id = int(words[0])
            words = words[1:]
        
            for word in words:
                if not word in result_words:
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
                    result_words.append(word)
                else:
                    the_word = result[result_words.index(word)]
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


def get_data_from_json(json_path: str) -> list:
    result = []
    with open(json_path, "r") as f:
        result = json.loads(f.read())
        result = sorted(result, key=lambda x: x["count"], reverse=True)
    return result

get_data_from_json("./data/indexer_usa.json")

def write_terms_ids(terms_ids_path: str, data: list):
    with open(terms_ids_path, "w+") as f:
        for i, word in enumerate(data):
            f.write(f"{i}\t{word['word']}\n")

write_terms_ids("./data/terms_ids_usa.csv")

with open("./data/indexer_usa.csv", "w+") as f:
    for i, word in enumerate(result):
        print(i)
        f.write(f"{i}\t{word['count']}\t{len(word['documents'])}")
        for doc in word["documents"]:
            f.write(f"\t{doc['id']}\t{doc['count']}")
        f.write("\n")