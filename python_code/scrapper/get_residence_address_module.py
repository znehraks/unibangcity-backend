from scrapper.scrapper_module import dabang_scrapper


def get_residence_address(address_lat, address_lon):
    left_lon = address_lon - 0.0412
    btm_lat = address_lat - 0.0159
    right_lon = address_lon + 0.0412
    top_lat = address_lat + 0.0159

    site_json = dabang_scrapper(left_lon,
                                btm_lat,
                                right_lon,
                                top_lat)
    items = site_json["regions"]
    refined_items = []
    for i in items:
        refined_items.append({
            "code": i["code"],
            "count": i["count"],
            "lat": i["center"][1],
            "lon": i["center"][0]
        })
    return refined_items
