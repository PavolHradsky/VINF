import lucene
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
import readline

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)

directory = FSDirectory.open(Paths.get("pylucene_index"))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = EnglishAnalyzer()
# Hotels in New York (state)
while True:
    q = input("Query: ")
    if q == '':
        break
    query = QueryParser("all_fields", analyzer).parse(q)
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
        print('\033[1m', 'about:', '\033[0m', doc.get("about")[0:200] if doc.get("about") else doc.get("about_wiki")[0:200])
        print('\033[1m', 'review_name:', '\033[0m', doc.get("review_name"))
        print('\033[1m', 'review_count:', '\033[0m', doc.get("review_count"))
        print('\033[1m', 'review_stars:', '\033[0m', doc.get("review_stars"))
        print('\033[1m', 'rooms:', '\033[0m', doc.get("rooms"))
        print('\033[1m', 'floors:', '\033[0m', doc.get("floors"))
        print('\033[1m', 'hotel_stars:', '\033[0m', doc.get("hotel_stars"))

