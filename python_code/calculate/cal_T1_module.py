from operator import itemgetter
from haversine import haversine
# 나온 매물 리스트들 좌표로 각각의 lgeo를 인덱스로 하여
# 그 lego의 lat, lon을 이용한 거리이용 가중치를 모두 구함
# 학교 좌표와 해당 매물과의 거리를 모두 구하여(맨하탄거리) 1위부터 꼴찌까지 가중치를 구함(이전에, Q2의 최대거리에서 필터링하여 해당 거리를 벗어나는 좌표에 있는 항목은 이 단계에서 걸러냄)


def cal_T1(refined_residence, univ_lon, univ_lat, limit_dist):
    limit_dist = float(limit_dist)
    # 직선거리로 이루어진 배열 생성 후 저장
    loc = []
    # abs(i["lat"]-univ_lat)+abs(i["lon"]-univ_lon)
    for i in refined_residence:
        loc.append({"code": i["code"], "dist": haversine(
            (i["lat"], i["lon"]), (univ_lat, univ_lon), unit='m'), "lat": i["lat"], "lon": i["lon"],
            "count": i["count"]})
    # 가까운 순으로 정렬
    sorted_loc = sorted(
        loc, key=itemgetter('dist'))

    # limit_dist를 벗어나는 매물 제거
    sorted_loc_filtered = []
    for index, i in enumerate(sorted_loc):
        if sorted_loc[index]["dist"] <= limit_dist:
            sorted_loc_filtered.append(i)
        else:
            break

    # 직선거리로 서열을 매겨 총 개수로 나눈 후 100점 만점(1위) 부터 0점까지(꼴찌) 1위부터 높은 점수로 배열함
    # ex.총 매물이 50일 경우, 1위가 100점, 2위가 98점, 3위가 96점 ... 50위가 0점 (동률에 대한 고려는 추후에 함)
    res = []
    len_sorted_loc_filtered = len(sorted_loc_filtered)
    # print(len_sorted_taxicab_geom)
    for index, i in enumerate(sorted_loc_filtered):
        res.append({"code": i["code"],
                    "count": i["count"], "dist": i["dist"], "lat": i["lat"], "lon": i["lon"],
                    "T1_weight": 100*(1/len_sorted_loc_filtered)*(len_sorted_loc_filtered-index)})
    return res

# 각 매물에서 해당 구에 속한 지하철역중 가장 가까운 것의 거리를 가중치로 매겨서 그것 역시 1위부터 꼴찌까지 가중치로 매김
