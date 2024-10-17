import os


query = "Bratislava nearly"

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

docs = []
dfs = []
with open("./data/indexer1.csv", "r") as indexer:
    indexes = indexer.readlines()
    for qtoken in query_tokens:
        tf_d = 0
        for line in indexes:
            words = line.split()
            if qtoken == words[1]:
                word_id = words[0]
                for doc_id, count in zip(words[3::2], words[4::2]):
                    docs.append(int(doc_id))
                    dfs.append(int(count))
                break
print(docs)
print(dfs)
        # tf_d = 