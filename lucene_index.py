import lucene
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, StringField, TextField, Field, FloatPoint, StoredField

from templates import final_fields


lucene.initVM(vmargs=['-Djava.awt.headless=true'])

index_path = "pylucene_index"
directory = FSDirectory.open(Paths.get(index_path))

analyzer = EnglishAnalyzer()
config = IndexWriterConfig(analyzer)

writer = IndexWriter(directory, config)

with open("data/extracted_all.csv", "r+") as f:
    for line in f.readlines():
        line = line.split("\t")

        doc = Document()
        doc.add(StringField("id", line[final_fields.index("id")], Field.Store.YES))
        doc.add(TextField("name", line[final_fields.index("name")], Field.Store.YES))
        doc.add(TextField("address", line[final_fields.index("address")], Field.Store.YES))
        doc.add(TextField("about", line[final_fields.index("about")], Field.Store.YES))
        doc.add(TextField("about_wiki", line[final_fields.index("about_wiki")], Field.Store.YES))
        doc.add(StringField("review_name", line[final_fields.index("review_name")], Field.Store.YES))
        doc.add(StringField("review_stars", line[final_fields.index("review_stars")], Field.Store.YES))
        doc.add(StringField("review_count", line[final_fields.index("review_count")], Field.Store.YES))
        doc.add(TextField("property_amenities", line[final_fields.index("property_amenities")], Field.Store.YES))
        doc.add(TextField("room_features", line[final_fields.index("room_features")], Field.Store.YES))
        doc.add(TextField("room_types", line[final_fields.index("room_types")], Field.Store.YES))
        doc.add(TextField("good_to_know", line[final_fields.index("good_to_know")], Field.Store.YES))
        for category in line[final_fields.index("categories")].split(";"):
            doc.add(StringField("categories", category, Field.Store.YES))
        doc.add(TextField("date_opened", line[final_fields.index("date_opened")], Field.Store.YES))
        doc.add(TextField("date_closed", line[final_fields.index("date_closed")], Field.Store.YES))
        doc.add(TextField("rooms", line[final_fields.index("rooms")], Field.Store.YES))
        doc.add(StringField("developer", line[final_fields.index("developer")], Field.Store.YES))
        doc.add(StringField("architect", line[final_fields.index("architect")], Field.Store.YES))
        doc.add(StringField("owner", line[final_fields.index("owner")], Field.Store.YES))
        doc.add(StringField("floors", line[final_fields.index("floors")], Field.Store.YES))
        doc.add(StoredField("website", line[final_fields.index("website")]))
        doc.add(StringField("hotel_stars", line[final_fields.index("hotel_stars")], Field.Store.YES))

        writer.addDocument(doc)

writer.commit()
writer.close()

directory.close()

print("Indexing complete.")