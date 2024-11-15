import lucene
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause
from org.apache.lucene.queryparser.classic import QueryParser

from templates import final_fields

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)

directory = FSDirectory.open(Paths.get("pylucene_index"))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = EnglishAnalyzer()
# query = QueryParser("about", analyzer).parse("Hotels in New York (state)")
boolean_query = BooleanQuery.Builder()

for field in ["name", "about", "about_wiki"]:
    query_parser = QueryParser(field, analyzer)  # Create a QueryParser for each field
    query = query_parser.parse("Hotels in new york")
    boolean_query.add(query, BooleanClause.Occur.SHOULD) 

scoreDocs = searcher.search(query, 50).scoreDocs
print("%s total matching documents." % len(scoreDocs))
for scoreDoc in scoreDocs:
    doc = searcher.storedFields().document(scoreDoc.doc)
    print('score:', round(scoreDoc.score, 2))
    print('name:', doc.get("name"))