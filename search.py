import os
import math
from utils import tokenize

# query = "hotel parking wifi 5"
query = "bicycle non-smoking new york"

query_tokens = tokenize(query)

docs_score = {}
N = 9604
with open("./data/indexer_usa.csv", "r") as indexer, open("./data/terms_ids_usa.csv") as terms_ids:
    indexes = indexer.readlines()
    indexes = [index.split("\t") for index in indexes]
    terms = terms_ids.readlines()
    terms = [term.split("\t")[1].strip() for term in terms]



query_type = "AND"
boolean_indexes = {}
for qtoken in query_tokens:
    if qtoken not in terms:
        print("not in indexes")
        continue
    termID = terms.index(qtoken)
    posting = indexes[termID]
    id = int(posting[0])
    posting = {
        "cf": int(posting[1]),
        "df": int(posting[2]),
        "documents": [
            {
                "doc_id": int(id),
                "tf": int(tf)
            } for id, tf in zip(posting[3::2], posting[4::2])
        ]
    }
    boolean_indexes[id] = posting

if query_type == "AND":
    doc_id_sets = [set(doc['doc_id'] for doc in item['documents']) for item in boolean_indexes.values()]
    doc_id_intersection = set.intersection(*doc_id_sets)
    for item in boolean_indexes.values():
        item['documents'] = [doc for doc in item['documents'] if doc['doc_id'] in doc_id_intersection]
elif "OR":
    pass




for qtoken in query_tokens:
    if qtoken not in terms:
        print("not in indexes")
        continue
    termID = terms.index(qtoken)
    posting = boolean_indexes[termID]

    cf = posting["cf"]
    df = posting["df"]

    tf = 1
    idf = math.log10(N/df)

    tf_idf = tf*idf

    for doc in posting["documents"]:
        wf = 1+math.log10(doc["tf"])
        if doc["doc_id"] not in docs_score.keys():
            docs_score[doc["doc_id"]] = tf_idf * wf
        else:
            docs_score[doc["doc_id"]] += tf_idf * wf

docs_score = sorted(docs_score.items(), key=lambda x:x[1], reverse=True)
if len(docs_score) > 10:
    docs_score = docs_score[:10]

with open("./data/urls_ids_usa.csv", "r") as f:
    lines = f.readlines()
    for doc in docs_score:
        doc_id = doc[0]
        print(lines[int(doc_id)+1].split()[1][:-1])
        # TODO: vypisat nieco ine, aj skore