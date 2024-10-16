# url
# <link rel=\"canonical\" href=\"(.*?)\">
# first group

# address
# <div class=\"fgplF\">.*?<div class=\"FhOgt H3 f u fRLPH\"><span class=\".*?<span class=\"biGQs _P pZUbB KxBGd\"(.*?)</span>
# first group

# about
# <div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"fIrGe _T\"[^>]*>(.*?)</div>
# first group

# review name
# <div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<div class=\"PtOPK\">(.*?)</div>
# first group

# review start
# <div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<span class=\"kJyXc P\">(.*?)</span>
# first group

# number of reviews (remove special characters) (4<!-- --> reviews)
# <div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<span class=\"biGQs _P pZUbB KxBGd\">(.*?)</span>
# first group

# Property amenities (need to clean from html characters)
# <div [^>]*id=\"ABOUT_TAB\">.*?<div .*?data-test-target=\"hr-about-group-property\"(.*?)(<div><button|<div></div>|<div class=\"idxbK\">.*?</div>)
# first group

# Room features (need to clean from html characters)
# <div [^>]*id=\"ABOUT_TAB\">.*?<div .*?data-test-target=\"hr-about-group-room_amenities\"(.*?)(<div><button|<div></div>|<div class=\"idxbK\">.*?</div>)
# first group

# Room types (need to clean from html characters)
# <div [^>]*id=\"ABOUT_TAB\">.*?<div .*?data-test-target=\"hr-about-group-room_types\"(.*?)(<div><button|<div></div>|<div class=\"idxbK\">.*?</div>)
# first group

# Good to know (need to clean from html characters)
# <div [^>]*id=\"ABOUT_TAB\">.*?<div .*?data-test-target=\"hr-about-group-good-to-know\"(.*?)(<div><button|<div></div>|<div class=\"idxbK\">.*?</div>)
# first group

import os
import re

BASE_URL = "./data/htmls"
files = os.listdir(BASE_URL)

for i, file in enumerate(files):
    with open(f"{BASE_URL}/{file}", "r") as f:
        html = f.read()

        url = re.findall(r"<link rel=\"canonical\" href=\"(.*?)\">", html)
        url = url[0] if len(url) else ""
        print(url)

        address = re.findall(r"<div class=\"fgplF\">.*?<div class=\"FhOgt H3 f u fRLPH\"><span class=\".*?<span class=\"biGQs _P pZUbB KxBGd\">(.*?)</span>", html)
        address = address[0] if len(address) else ""
        print(address)

        # TODO: remove html tags if some
        about = re.findall(r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"fIrGe _T\"[^>]*>(.*?)</div>", html)
        about = about[0] if len(about) else ""
        print(about)

        review_name = re.findall(r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<div class=\"PtOPK\">(.*?)</div>", html)
        review_name = review_name[0] if len(review_name) else ""
        print(review_name)

        review_stars = re.findall(r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<span class=\"kJyXc P\">(.*?)</span>", html)
        review_stars = review_stars[0] if len(review_stars) else ""
        print(review_stars)

        # TODO: remove <!-- -->
        review_count = re.findall(r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<span class=\"biGQs _P pZUbB KxBGd\">(.*?)</span>", html)
        review_count = review_count[0] if len(review_count) else ""
        print(review_count)

        # TODO: multiple spaces replace with one
        property_amenities = re.findall(r">Property amenities(.*?)(?:<div><button|<div></div>)", html)
        property_amenities = property_amenities[0] if len(property_amenities) else ""
        property_amenities = re.sub(r"<[^>]*>", " ", property_amenities)
        print(property_amenities)

        # TODO: multiple spaces replace with one
        room_features = re.findall(r">Room features(.*?)(?:<div><button|<div></div>)", html)
        room_features = room_features[0] if len(room_features) else ""
        room_features = re.sub(r"<[^>]*>", " ", room_features)
        print(room_features)

        # TODO: multiple spaces replace with one
        room_types = re.findall(r">Room types(.*?)(?:<div><button|<div></div>)", html)
        room_types = room_types[0] if len(room_types) else ""
        room_types = re.sub(r"<[^>]*>", " ", room_types)
        print(room_types)

        # TODO: multiple spaces replace with one
        good_to_know = re.findall(r">Good to know(.*?)(?:<div class=\"idxbK\">.*?</div>)", html)
        good_to_know = good_to_know[0] if len(good_to_know) else ""
        good_to_know = re.sub(r"<[^>]*>", " ", good_to_know)
        print(good_to_know)



    if i > 3:
        break