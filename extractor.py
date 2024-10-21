import os
import re


def get_data_with_regex(html: str, regex: str) -> str:
    str = re.findall(regex, html)
    str = str[0] if len(str) else ""
    return str


def extract_data(urls_ids_path: str, extracted_path: str):
    with open(urls_ids_path, "w+") as urls_ids:
        with open(extracted_path, "w+") as extracted:
            urls_ids.write("id\turl\n")
            extracted.write("id\tname\taddress\tabout\treview_name\treview_stars\treview_count\tproperty_amenities\troom_features\troom_types\tgood_to_know\n")
            for i, file in enumerate(files):
                with open(f"{BASE_URL}/{file}", "r") as f:
                    html = f.read()

                    url = get_data_with_regex(html, r"<link rel=\"canonical\" href=\"(.*?)\">")
                    print(url)

                    name = get_data_with_regex(html, r"<h1 id=\"HEADING\"[^\>]*>(.*?)</h1>")

                    address = get_data_with_regex(html, r"<div class=\"fgplF\">.*?<div class=\"FhOgt H3 f u fRLPH\"><span class=\".*?<span class=\"biGQs _P pZUbB KxBGd\">(.*?)</span>")

                    about = get_data_with_regex(html, r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"fIrGe _T\"[^>]*>(.*?)</div>")
                    about = re.sub(r"<[^>]*>", " ", about)
                    about = re.sub(r"  +", " ", about)
                    about = about.strip()

                    review_name = get_data_with_regex(html, r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<div class=\"PtOPK\">(.*?)</div>")

                    review_stars = get_data_with_regex(html, r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<span class=\"kJyXc P\">(.*?)</span>")

                    review_count = get_data_with_regex(html, r"<div [^>]*id=\"ABOUT_TAB\">.*?<div class=\"dGsKv Xe f P\">.*?<span class=\"biGQs _P pZUbB KxBGd\">(.*?)</span>")
                    review_count = re.sub(r"<!-- -->", "", review_count)

                    property_amenities = get_data_with_regex(html, r">Property amenities(.*?)(?:<div><button|<div></div>)")
                    property_amenities = re.sub(r"<[^>]*>", " ", property_amenities)
                    property_amenities = re.sub(r"  +", " ", property_amenities)
                    property_amenities = property_amenities.strip()

                    room_features = get_data_with_regex(html, r">Room features(.*?)(?:<div><button|<div></div>)")
                    room_features = re.sub(r"<[^>]*>", " ", room_features)
                    room_features = re.sub(r"  +", " ", room_features)
                    room_features = room_features.strip()

                    room_types = get_data_with_regex(html, r">Room types(.*?)(?:<div><button|<div></div>)")
                    room_types = re.sub(r"<[^>]*>", " ", room_types)
                    room_types = re.sub(r"  +", " ", room_types)
                    room_types = room_types.strip()

                    good_to_know = get_data_with_regex(html, r">Good to know(.*?)(?:<div class=\"idxbK\">.*?</div>)")
                    good_to_know = re.sub(r"<div class=\"biGQs _P pZUbB KxBGd\">.*?</div>", " ", good_to_know)
                    good_to_know = re.sub(r"<[^>]*>", " ", good_to_know)
                    good_to_know = re.sub(r"  +", " ", good_to_know)
                    good_to_know = good_to_know.strip()

                    urls_ids.write(f"{i}\t{url}\n")
                    extracted.write(f"{i}\t{name}\t{address}\t{about}\t{review_name}\t{review_stars}\t{review_count}\t{property_amenities}\t{room_features}\t{room_types}\t{good_to_know}\n")


if __name__ == "__main__":
    BASE_URL = "./data/htmls_usa"
    files = os.listdir(BASE_URL)
    extract_data("./data/urls_ids_usa.csv", "./data/extracted_usa.csv")