import lucene
from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, StringField, TextField, Field, IntPoint, FloatPoint, StoredField

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
        doc.add(StringField("id", line[final_fields.index("id")], Field.Store.NO))
        doc.add(TextField("name", line[final_fields.index("name")], Field.Store.YES))
        doc.add(TextField("address", line[final_fields.index("address")], Field.Store.YES))
        doc.add(StringField("state", line[final_fields.index("state")], Field.Store.YES))
        doc.add(TextField("about", line[final_fields.index("about")], Field.Store.YES))
        doc.add(TextField("about_wiki", line[final_fields.index("about_wiki")], Field.Store.YES))
        doc.add(StringField("review_name", line[final_fields.index("review_name")], Field.Store.YES))
        # doc.add(FloatPoint("review_stars", float(line[final_fields.index("review_stars")]) if line[final_fields.index("review_stars")].strip() else -1.0))
        # doc.add(StoredField("review_stars_stored", float(line[final_fields.index("review_stars")]) if line[final_fields.index("review_stars")].strip() else -1.0))
        # doc.add(IntPoint("review_count", int(line[final_fields.index("review_count")]) if line[final_fields.index("review_count")].strip() else -1))
        # doc.add(StoredField("review_count_stored", int(line[final_fields.index("review_count")]) if line[final_fields.index("review_count")].strip() else -1))
        if line[final_fields.index("review_stars")].strip(): doc.add(FloatPoint("review_stars", float(line[final_fields.index("review_stars")])))
        if line[final_fields.index("review_stars")].strip(): doc.add(StoredField("review_stars", float(line[final_fields.index("review_stars")])))
        if line[final_fields.index("review_count")].strip(): doc.add(IntPoint("review_count", int(line[final_fields.index("review_count")])))
        if line[final_fields.index("review_count")].strip(): doc.add(StoredField("review_count", int(line[final_fields.index("review_count")])))
        doc.add(TextField("property_amenities", line[final_fields.index("property_amenities")], Field.Store.NO))
        doc.add(TextField("room_features", line[final_fields.index("room_features")], Field.Store.NO))
        doc.add(TextField("room_types", line[final_fields.index("room_types")], Field.Store.NO))
        doc.add(TextField("good_to_know", line[final_fields.index("good_to_know")], Field.Store.NO))
        for category in line[final_fields.index("categories")].split(";"):
            doc.add(StringField("categories", category, Field.Store.NO))
        doc.add(TextField("date_opened", line[final_fields.index("date_opened")], Field.Store.NO))
        doc.add(TextField("date_closed", line[final_fields.index("date_closed")], Field.Store.NO))
        if line[final_fields.index("rooms")].strip(): doc.add(IntPoint("rooms", int(line[final_fields.index("rooms")])))
        if line[final_fields.index("rooms")].strip(): doc.add(StoredField("rooms", int(line[final_fields.index("rooms")])))
        doc.add(StringField("developer", line[final_fields.index("developer")], Field.Store.NO))
        doc.add(StringField("architect", line[final_fields.index("architect")], Field.Store.NO))
        doc.add(StringField("owner", line[final_fields.index("owner")], Field.Store.NO))
        if line[final_fields.index("floors")].strip(): doc.add(FloatPoint("floors", float(line[final_fields.index("floors")])))
        if line[final_fields.index("floors")].strip(): doc.add(StoredField("floors", float(line[final_fields.index("floors")])))
        doc.add(StoredField("website", line[final_fields.index("website")]))
        if line[final_fields.index("hotel_stars")].strip(): doc.add(FloatPoint("hotel_stars", float(line[final_fields.index("hotel_stars")])))

        doc.add(TextField("all_fields", " ".join(line), Field.Store.NO))

        writer.addDocument(doc)

writer.commit()
writer.close()

directory.close()

print("Indexing complete.")