import os
import math

query = "nearly here"

query = query.lower()
query = query.replace("\t", " ")
query = query.replace(",", " ")
query = query.replace(".", " ")
query = query.replace("/", " ")
query = query.replace(";", " ")
query = query.replace("\"", " ")
query = query.replace("\'", " ")
query = query.replace("(", " ")
query = query.replace(")", " ")
query = query.replace("[", " ")
query = query.replace("]", " ")
query = query.replace("*", " ")
query = query.replace(":", " ")
query = query.replace("!", " ")
query = query.replace("+", " ")
query = query.replace("=", " ")
query_tokens = query.split()

docs_score = {}
N = 9604
with open("./data/indexer_usa.csv", "r") as indexer:
    indexes = indexer.readlines()
    indexes = [index.split("\t") for index in indexes]
    terms = [x[1] for x in indexes]
    
    for qtoken in query_tokens:
        if qtoken not in terms:
            print("not in indexes")
            continue
        termID = terms.index(qtoken)
        posting = indexes[termID]

        cf = posting[2]
        doc_ids = posting[3::2]
        tfs = posting[4::2]

        tf = 1
        df = len(doc_ids)
        idf = math.log10(N/df)

        tf_idf = tf*idf

        for doc_id, tf in zip(doc_ids, tfs):
            wf = 1+math.log10(int(tf))
            if doc_id not in docs_score.keys():
                docs_score[doc_id] = tf_idf * wf
            else:
                docs_score[doc_id] += tf_idf * wf

docs_score = sorted(docs_score.items(), key=lambda x:x[1], reverse=True)
if len(docs_score) > 20:
    docs_score = docs_score[:20]
# print(docs_score)

with open("./data/urls_ids_usa.csv", "r") as f:
    lines = f.readlines()
    for doc in docs_score:
        doc_id = doc[0]
        print(lines[int(doc_id)+1].split()[1][:-1])