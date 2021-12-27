import csv
from operator import itemgetter
cwd = "python_code/data/"


def cal_T4(refined_residence):
    # 범죄율 csv 불러옴
    crime = open(f'{cwd}crime_refined.csv', 'r', encoding='utf8')
    crime_r = csv.reader(crime)
    crime_r_list = list(crime_r)
    # 중간결과 담을 리스트
    crime_list = []

    # 매물리스트를 outer에 지하철리스트를 inner에 두고 각 매물에서 모든 구 와의 거리를 계산하여
    # 가장 가까운 구와 그 구와의 거리를 구함
    for index_r, i in enumerate(refined_residence):
        # 임시로 구와 모든매물과의 거리를 계산할 리스트
        temp = []
        for index_c, j in enumerate(crime_r_list):
            if(index_c == 0):
                continue
            temp.append(abs(i["lat"] - float(j[3])) +
                        abs(i["lon"] - float(j[4])))
            if(index_c == len(crime_r_list)-1):
                crime_list.append({"code": i["code"], "nearest": temp.index(
                    min(temp))+1, "gu_dist": min(temp)})

    crime.close()
    # 거리가 가까운 순으로 정렬함
    sorted_crime_list = sorted(
        crime_list, key=itemgetter('gu_dist'))

    # 최종결과를 담을 리스트 생성
    res = []

    len_sorted_crime_list = len(sorted_crime_list)

    # T4최종 가중치 추산을 위한 계산작업
    for index, i in enumerate(sorted_crime_list):
        res.append({"code": i["code"], "nearest": i["nearest"], "gu_dist": i["gu_dist"],
                    "T4_weight": int(crime_r_list[int(i["nearest"])][1])})
    return res
