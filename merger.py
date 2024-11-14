import os

BASE_DIR = "data/wiki"

with open("data/extracted_usa.csv", "r") as extracted:
    data = extracted.readlines()[1:]
    data = [x.split('\t') for x in data]
    names = [x[1].replace("&amp;", "&") for x in data]

last_id = int(data[-1][0])
next_id = last_id + 1

extracted_fields = [
    'id', 'name', 'address', 'about', 'review_name', 'review_stars', 'review_count', 
    'property_amenities', 'room_features', 'room_types', 'good_to_know'
]

wiki_fields = [
    'title', 'categories', 'about', 'name', 'location', 'address', 'date_opened', 'opening_date', 'built', 'date_closed', 'closing_date', 
    'rooms', 'number_of_rooms', 'developer', 'architect', 'owner', 'floors', 'website', 'parking', 'stars'
]

final_fields = [
    'id', 'name', 'address', # address if set, else location
    'about', 'about_wiki', 'review_name', 'review_stars', 'review_count', 
    'property_amenities', # add parking
    'room_features', 'room_types', 'good_to_know',
    'categories', # split by ;
    'date_opened', # date_opened / opening_date
    'built', 'date_closed', # date_closed / closing_date
    'rooms', # rooms / number_of_rooms
    'developer', 'architect', 'owner', 'floors', 'website', 'hotel_stars'
]

result_list = []

with open(f"data/wiki.csv", "r") as wikifile:
    wikidata = wikifile.readlines()
    wikidata = [x.replace('\n', '') for x in wikidata]
    wikidata = [x.split('\t') for x in wikidata]
    for doc in wikidata:
        if doc[0] in names:
            extracted_doc = data[names.index(doc[0])]
            print(doc[0])
            result_list.append([
                extracted_doc[extracted_fields.index('id')], 
                extracted_doc[extracted_fields.index('name')], 
                extracted_doc[extracted_fields.index('address')], 
                extracted_doc[extracted_fields.index('about')], 
                doc[wiki_fields.index('about')],
                extracted_doc[extracted_fields.index('review_name')], 
                extracted_doc[extracted_fields.index('review_stars')], 
                extracted_doc[extracted_fields.index('review_count')], 
                extracted_doc[extracted_fields.index('property_amenities')], 
                extracted_doc[extracted_fields.index('room_features')], 
                extracted_doc[extracted_fields.index('room_types')], 
                extracted_doc[extracted_fields.index('good_to_know')],
                # ...continue with doc
            ])
            continue


