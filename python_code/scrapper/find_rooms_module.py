from scrapper.scrapper_module import dabang_item_scrapper


def find_rooms(top5):
    for i in top5:
        rooms_id, rooms_type, rooms_lat, rooms_lon, rooms_price_title, rooms_selling_type, rooms_img_url_01, rooms_desc, rooms_desc2, rooms_hash_tags_count, rooms_hash_tags = dabang_item_scrapper(
            i["code"], 1)
        i["rooms_id"] = rooms_id
        i["rooms_type"] = rooms_type
        i["rooms_location_lat"] = rooms_lat
        i["rooms_location_lon"] = rooms_lon
        i["rooms_price_title"] = rooms_price_title
        i["rooms_selling_type"] = rooms_selling_type
        i["rooms_img_url_01"] = rooms_img_url_01
        i["rooms_desc"] = rooms_desc
        i["rooms_desc2"] = rooms_desc2
        i["rooms_hash_tags_count"] = rooms_hash_tags_count
        i["rooms_hash_tags"] = rooms_hash_tags
    return top5
