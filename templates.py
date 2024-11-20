final_fields = [
    'id', 'name', 'address', # address if set, else location
    'state', 'about', 'about_wiki', 'review_name', 'review_stars', 'review_count', 
    'property_amenities', # add parking
    'room_features', 'room_types', 'good_to_know',
    'categories', # split by ;
    'date_opened', # date_opened / opening_date / built
    'date_closed', # date_closed / closing_date
    'rooms', # rooms / number_of_rooms
    'developer', 'architect', 'owner', 'floors', 'website', 'hotel_stars'
]

extracted_fields = [
    'id', 'name', 'address', 'about', 'review_name', 'review_stars', 'review_count', 
    'property_amenities', 'room_features', 'room_types', 'good_to_know'
]

wiki_fields = [
    'title', 'categories', 'about', 'name', 'location', 'address', 'date_opened', 'opening_date', 'built', 'date_closed', 'closing_date', 
    'rooms', 'number_of_rooms', 'developer', 'architect', 'owner', 'floors', 'website', 'parking', 'stars'
]