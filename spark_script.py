# docker exec -it spark /bin/bash 
# hadoop fs -ls ./
# wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles1.xml-p1p41242.bz2
# hadoop fs -copyFromLocal enwiki-latest-pages-articles1.xml-p1p41242.bz2 ./
# hadoop fs -ls ./
# export PYSPARK_PYTHON=python3
# pyspark --packages com.databricks:spark-xml_2.12:0.18.0
# spark-submit --packages com.databricks:spark-xml_2.12:0.18.0 spark_script.py

# hadoop fs -copyToLocal ./wiki ./wiki
# docker cp spark:/wiki ./


#     ____              __
#    / __/__  ___ _____/ /__
#   _\ \/ _ \/ _ `/ __/  `_/
#  /__ / .__/\_,_/_/ /_/\_\   version 2.4.3
#     /_/
#


from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import regexp_extract, regexp_replace, col, udf
import re

spark = SparkSession \
    .builder \
    .appName('WikiXML') \
    .getOrCreate() \

xml_schema = StructType([
    StructField('title', StringType(), False),
    StructField('revision',
        StructType([StructField('text', StringType(), False)]),
    False)
])

df = spark.read.format('com.databricks.spark.xml') \
    .option("rowTag", "page") \
    .schema(xml_schema) \
    .load("hdfs://localhost:9000/user/root/enwiki-latest-pages-articles-1.xml.bz2")
    # .load("hdfs://localhost:9000/user/root/enwiki-latest-pages-articles17.xml-p22070393p23570392.bz2")

# df.printSchema()

us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
    "New Hampshire", "New Jersey", "New Mexico", "New York", 
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"
]

pattern = r"(?i)\[\[Category:Hotels in [^\]]*(" + "|".join(us_states) + r")"

result = df.filter(df.revision.text.rlike(pattern) & ~df.title.startswith('Category:')).cache()

# filtered_df.show(5)


result = result.withColumn(
    "text", 
    regexp_replace(col("revision.text"), r'<ref[^<]*<\/ref>|<ref.*?\/>', '')
)
result = result.withColumn(
    "text", 
    regexp_replace(col("text"), r'<!--.*?-->', '')
)
result = result.withColumn(
    "text", 
    regexp_replace(col("text"), r'<br/?>', ' ')
)

def extract_all_categories(text):
    categories = re.findall('\[\[Category:(.*?)\]\]\n', text, re.DOTALL)
    return ";".join(categories).strip() if categories else None

extract_all_categories_udf = udf(extract_all_categories, StringType())
result = result.withColumn('categories', extract_all_categories_udf(col('text')))

result = result.withColumn(
    "text", 
    regexp_replace(col("text"), r'\[\[|\]\]', '')
)

result = result.withColumn('about', regexp_extract(col('text'), r"'''.*?\n", 0))
result = result.withColumn('about', regexp_replace(col('about'), r'\|', ' '))

result = result.withColumn('text', regexp_replace(col('text'), r'\{\{.*?\}\}', ' '))
# result = result.withColumn('text', regexp_replace(col('text'), r'\|', ' '))

infobox_fields = [
    'name', 'location', 'address', 'date_opened', 'opening_date', 'built', 'date_closed', 'closing_date', 
    'rooms', 'number_of_rooms', 'developer', 'architect', 'owner', 'floors', 'website', 'parking', 'stars'
]

for field in infobox_fields:
    result = result.withColumn(field, regexp_extract(col('text'), '(?s)\{\{Infobox(?:(?!\n\}\}\n).)*\| ?' + field + ' +=([^\n]*)', 1))
    result = result.withColumn(field, regexp_replace(col(field), r'\|', ' '))


result = result.drop('revision')
result = result.drop('text')

result.write \
    .mode("overwrite") \
    .option("sep", "\t") \
    .option("quote", "") \
    .csv("hdfs://localhost:9000/user/root/wiki")