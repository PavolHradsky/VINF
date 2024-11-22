import lucene
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.document import IntPoint, FloatPoint
import readline
import re

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)

def range_query(field, q, type_point):
    tmp_q = q[q.index(field+":[")+len(field)+2:]
    tmp_q = tmp_q[:tmp_q.index("]")]
    min = tmp_q.split(" TO ")[0]
    max = tmp_q.split(" TO ")[1]
    if type_point == "int":
        range_q = IntPoint.newRangeQuery(field, int(min), int(max))
    else:
        range_q = FloatPoint.newRangeQuery(field, float(min), float(max))

    return range_q

directory = FSDirectory.open(Paths.get("pylucene_index"))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = EnglishAnalyzer()
# Hotels in New York (state)
while True:
    boolean_query = BooleanQuery.Builder()
    q = input("Query: ")
    if q == '':
        break
    field = "review_stars"
    if field+":[" in q and "TO" in q:
        boolean_query.add(range_query(field, q, 'float'), BooleanClause.Occur.MUST)  
        q = re.sub(field+r"\:\[.*?\]", "", q)
    field = "review_count"
    if field+":[" in q and "TO" in q:
        boolean_query.add(range_query(field, q, 'int'), BooleanClause.Occur.MUST)  
        q = re.sub(field+r"\:\[.*?\]", "", q)
    field = "rooms"
    if field+":[" in q and "TO" in q:
        boolean_query.add(range_query(field, q, 'int'), BooleanClause.Occur.MUST)  
        q = re.sub(field+r"\:\[.*?\]", "", q)
    field = "floors"
    if field+":[" in q and "TO" in q:
        boolean_query.add(range_query(field, q, 'float'), BooleanClause.Occur.MUST)  
        q = re.sub(field+r"\:\[.*?\]", "", q)
    field = "hotel_stars"
    if field+":[" in q and "TO" in q:
        boolean_query.add(range_query(field, q, 'float'), BooleanClause.Occur.MUST)  
        q = re.sub(field+r"\:\[.*?\]", "", q)

    if q.strip():
        boolean_query.add(QueryParser("all_fields", analyzer).parse(q), BooleanClause.Occur.MUST)
        

    # query = QueryParser("all_fields", analyzer).parse(q)
    # # boolean_query.add(query, BooleanClause.Occur.SHOULD)
    print('=========================================================')
    print('=========================================================')

    scoreDocs = searcher.search(boolean_query.build(), 10).scoreDocs
    print("%s total matching documents." % len(scoreDocs))
    for scoreDoc in scoreDocs:
        doc = searcher.storedFields().document(scoreDoc.doc)
        print('------------------------------------')
        print('\033[1m', 'score:', '\033[0m', round(scoreDoc.score, 2))
        print('\033[1m', 'name:', '\033[0m', doc.get("name"))
        print('\033[1m', 'state:', '\033[0m', doc.get("state"))
        print('\033[1m', 'address:', '\033[0m', doc.get("address"))
        print('\033[1m', 'about:', '\033[0m', doc.get("about")[0:200] if doc.get("about") else doc.get("about_wiki")[0:200])
        print('\033[1m', 'review_name:', '\033[0m', doc.get("review_name"))
        print('\033[1m', 'review_count:', '\033[0m', doc.get("review_count"))
        print('\033[1m', 'review_stars:', '\033[0m', doc.get("review_stars"))
        print('\033[1m', 'rooms:', '\033[0m', doc.get("rooms"))
        print('\033[1m', 'floors:', '\033[0m', doc.get("floors"))

