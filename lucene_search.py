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

directory = FSDirectory.open(Paths.get("pylucene_index"))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = EnglishAnalyzer()
# Hotels in New York (state)
while True:
    # boolean_query = BooleanQuery.Builder()
    q = input("Query: ")
    if q == '':
        break
    # if "[" in q:
    #     res = re.findall(r"(AND )?([a-z_]+):\[([0-9]+) TO ([0-9]+)\]( AND)?", q)
    #     if res:
    #         is_and, field, min, max, is_and2 = res[0]
    #         range_query = IntPoint.newRangeQuery(field, min, max)
    #         boolean_query.add(range_query, BooleanClause.Occur.MUST if is_and or is_and2 else BooleanClause.Occur.SHOULD)

    query = QueryParser("all_fields", analyzer).parse(q)
    # boolean_query.add(query, BooleanClause.Occur.SHOULD)
    print('=========================================================')
    print('=========================================================')

    scoreDocs = searcher.search(query, 10).scoreDocs
    print("%s total matching documents." % len(scoreDocs))
    for scoreDoc in scoreDocs:
        doc = searcher.storedFields().document(scoreDoc.doc)
        print('------------------------------------')
        print('\033[1m', 'score:', '\033[0m', round(scoreDoc.score, 2))
        print('\033[1m', 'name:', '\033[0m', doc.get("name"))
        print('\033[1m', 'state:', '\033[0m', doc.get("state"))
        print('\033[1m', 'address:', '\033[0m', doc.get("address"))
        # print('\033[1m', 'about:', '\033[0m', doc.get("about")[0:200] if doc.get("about") else doc.get("about_wiki")[0:200])
        # print('\033[1m', 'review_name:', '\033[0m', doc.get("review_name"))
        # print('\033[1m', 'review_count:', '\033[0m', doc.get("review_count"))
        # print('\033[1m', 'review_stars:', '\033[0m', doc.get("review_stars"))
        # print('\033[1m', 'rooms:', '\033[0m', doc.get("rooms"))
        # print('\033[1m', 'floors:', '\033[0m', doc.get("floors"))
        # print('\033[1m', 'hotel_stars:', '\033[0m', doc.get("hotel_stars"))

