import csv
from operator import itemgetter

cwd = "python_code/data/"

# 구 별 범죄율로 가중치 구함(위도,경도 값으로 해당 점이 어느 구에 속하는지 판별 후, 그 구의 범죄율 가중치로 정함)


def cal_T3(refined_residence):
    # 물가 csv 불러옴
    price = open(f'{cwd}price_refined.csv', 'r', encoding='utf8')
    price_r = csv.reader(price)
    price_r_list = list(price_r)
    # 중간결과 담을 리스트
    price_list = []

    # 매물리스트를 outer에 지하철리스트를 inner에 두고 각 매물에서 모든 구 와의 거리를 계산하여
    # 가장 가까운 구와 그 구와의 거리를 구함
    for index_r, i in enumerate(refined_residence):
        # 임시로 구와 모든매물과의 거리를 계산할 리스트
        temp = []
        for index_p, j in enumerate(price_r_list):
            if(index_p == 0):
                continue
            temp.append(abs(i["lat"] - float(j[5])) +
                        abs(i["lon"] - float(j[6])))
            if(index_p == len(price_r_list)-1):
                price_list.append({"code": i["code"], "nearest": temp.index(
                    min(temp))+1, "gu_dist": min(temp)})

    price.close()
    # 거리가 가까운 순으로 정렬함
    sorted_price_list = sorted(
        price_list, key=itemgetter('gu_dist'))

    # 최종결과를 담을 리스트 생성
    res = []

    len_sorted_price_list = len(sorted_price_list)

    # T3최종 가중치 추산을 위한 계산작업
    for index, i in enumerate(sorted_price_list):
        res.append({"code": i["code"], "nearest": i["nearest"], "gu_dist": i["gu_dist"],
                    "T3_weight": int(price_r_list[int(i["nearest"])][4])})
    return res
