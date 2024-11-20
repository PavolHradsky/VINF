import os
import re

from templates import final_fields, extracted_fields, wiki_fields

BASE_DIR = "data/wiki"

with open("data/extracted_usa.csv", "r") as extracted:
    data = extracted.readlines()[1:]
    data = [x.replace('\u2028', '') for x in data]
    data = [x.split('\t') for x in data]
    names = [x[1].replace("&amp;", "&") for x in data]


states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
    "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
    "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
    "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

state_mapping = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", 
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", 
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", 
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", 
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", 
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", 
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", 
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", 
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", 
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", 
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", 
    "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", 
    "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}

def get_state_from_address(address):
    for state in states:
        if state.lower() in str(address).lower():
            if len(state) > 2:
                return state
            return state_mapping[state]
    return ""

def get_number(str):
    if not str:
        return ""
    finds = re.findall(r'[\d]+[.,\d]+', str)
    if not finds:
        return ""
    result = finds[0].replace(",", "")
    return result

last_id = int(data[-1][0])
next_id = last_id + 1

result_list = []

with open(f"data/wiki.csv", "r") as wikifile:
    wikidata = wikifile.readlines()
    wikidata = [x.replace('\n', '') for x in wikidata]
    wikidata = [x.split('\t') for x in wikidata]
    for doc in wikidata:
        if doc[0].startswith("[[Category"):
            continue
        if len(doc) < len(wiki_fields):
            doc += [''] * (len(wiki_fields) - len(doc))
        if doc[0] in names:
            extracted_doc = data[names.index(doc[0])]
            # print(doc[0])
            result_list.append([
                extracted_doc[extracted_fields.index('id')], 
                extracted_doc[extracted_fields.index('name')], 
                extracted_doc[extracted_fields.index('address')], 
                get_state_from_address(extracted_doc[extracted_fields.index('address')]), 
                extracted_doc[extracted_fields.index('about')], 
                doc[wiki_fields.index('about')],
                extracted_doc[extracted_fields.index('review_name')], 
                get_number(extracted_doc[extracted_fields.index('review_stars')]), 
                get_number(extracted_doc[extracted_fields.index('review_count')]), 
                extracted_doc[extracted_fields.index('property_amenities')] + ' ' + doc[wiki_fields.index('parking')], 
                extracted_doc[extracted_fields.index('room_features')], 
                extracted_doc[extracted_fields.index('room_types')], 
                extracted_doc[extracted_fields.index('good_to_know')].strip(),
                doc[wiki_fields.index('categories')],
                doc[wiki_fields.index('date_opened')] if doc[wiki_fields.index('date_opened')] else doc[wiki_fields.index('opening_date')] if doc[wiki_fields.index('opening_date')] else doc[wiki_fields.index('built')],
                doc[wiki_fields.index('date_closed')] if doc[wiki_fields.index('date_closed')] else doc[wiki_fields.index('closing_date')],
                get_number(doc[wiki_fields.index('rooms')]) if doc[wiki_fields.index('rooms')] else get_number(doc[wiki_fields.index('number_of_rooms')]), 
                doc[wiki_fields.index('developer')],
                doc[wiki_fields.index('architect')],
                doc[wiki_fields.index('owner')],
                get_number(doc[wiki_fields.index('floors')]),
                doc[wiki_fields.index('website')],
                doc[wiki_fields.index('stars')],
            ])
            del data[names.index(doc[0])]
            continue
        result_list.append([
            next_id, 
            doc[wiki_fields.index('title')] if doc[wiki_fields.index('title')] else doc[wiki_fields.index('name')],
            doc[wiki_fields.index('location')] if doc[wiki_fields.index('location')] else doc[wiki_fields.index('address')],
            get_state_from_address(doc[wiki_fields.index('location')]) if doc[wiki_fields.index('location')] else get_state_from_address(doc[wiki_fields.index('address')]),
            '', 
            doc[wiki_fields.index('about')],
            '',
            '',
            '',
            doc[wiki_fields.index('parking')],
            '',
            '',
            '',
            doc[wiki_fields.index('categories')],
            doc[wiki_fields.index('date_opened')] if doc[wiki_fields.index('date_opened')] else doc[wiki_fields.index('opening_date')] if doc[wiki_fields.index('opening_date')] else doc[wiki_fields.index('built')],
            doc[wiki_fields.index('date_closed')] if doc[wiki_fields.index('date_closed')] else doc[wiki_fields.index('closing_date')],
            get_number(doc[wiki_fields.index('rooms')]) if doc[wiki_fields.index('rooms')] else get_number(doc[wiki_fields.index('number_of_rooms')]), 
            doc[wiki_fields.index('developer')],
            doc[wiki_fields.index('architect')],
            doc[wiki_fields.index('owner')],
            get_number(doc[wiki_fields.index('floors')]),
            doc[wiki_fields.index('website')],
            get_number(doc[wiki_fields.index('stars')]),
        ])
        next_id += 1
    for extracted_doc in data:
        result_list.append([
            extracted_doc[extracted_fields.index('id')], 
            extracted_doc[extracted_fields.index('name')], 
            extracted_doc[extracted_fields.index('address')], 
            get_state_from_address(extracted_doc[extracted_fields.index('address')]), 
            extracted_doc[extracted_fields.index('about')], 
            '',
            extracted_doc[extracted_fields.index('review_name')], 
            get_number(extracted_doc[extracted_fields.index('review_stars')]), 
            get_number(extracted_doc[extracted_fields.index('review_count')]), 
            extracted_doc[extracted_fields.index('property_amenities')], 
            extracted_doc[extracted_fields.index('room_features')], 
            extracted_doc[extracted_fields.index('room_types')], 
            extracted_doc[extracted_fields.index('good_to_know')].strip(),
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ])

result_list = sorted(result_list, key=lambda x: int(x[0]))

with open('data/extracted_all.csv', 'w+') as f:
    for line in result_list:
        f.write('\t'.join([str(x) for x in line]) + '\n')