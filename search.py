import os
import math
from utils import tokenize


def get_indexes(indexer_path):
    with open(indexer_path, "r") as indexer:
        indexes = indexer.readlines()
        indexes = [index.split("\t") for index in indexes]
    return indexes


def get_terms(terms_ids_path):
    with open(terms_ids_path, "r") as terms_ids:
        terms = terms_ids.readlines()
        terms = [term.split("\t")[1].strip() for term in terms]
    return terms


def boolean_search(query_tokens, terms, indexes, query_type: str = "AND"):
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

    return boolean_indexes


def search(query_tokens, terms, boolean_indexes, limit = 10, N = 9604):
    docs_score = {}
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
    if len(docs_score) > limit:
        docs_score = docs_score[:limit]
    return docs_score


def print_results(docs_score, urls_ids_path, extracted_path):
    with open(urls_ids_path, "r") as f:
        urls_ids = f.readlines()

    with open(extracted_path, "r") as f:
        extracted = f.readlines()

    for doc in docs_score:
        doc_id = doc[0]
        score = doc[1]
        url = urls_ids[int(doc_id)+1].split()[1][:-1]

        doc_extracted = extracted[int(doc_id)+1].split("\t")
        name = doc_extracted[1]
        address = doc_extracted[2]
        about = doc_extracted[3]

        print("=====================================")
        print(f"Name:\t\t{name}")
        print(f"Score:\t\t{score:.4f}")
        print(f"Address:\t{address}")
        print(f"About:\t\t{about[:100]}...")
        print(f"Url:\t\t{url}")
        print()
    print("=====================================")


if __name__ == "__main__":
    # query = "hotel parking wifi 5"
    query = "bicycle non-smoking new york"

    query_tokens = tokenize(query)

    indexes = get_indexes("./data/indexer_usa.csv")
    terms = get_terms("./data/terms_ids_usa.csv")
    boolean_indexes = boolean_search(query_tokens, terms, indexes, 'AND')
    docs_score = search(query_tokens, terms, boolean_indexes, 10)
    print_results(docs_score, "./data/urls_ids_usa.csv", "./data/extracted_usa.csv")
