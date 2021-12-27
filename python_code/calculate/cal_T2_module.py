
import csv
from operator import itemgetter

cwd = "python_code/data/"


def cal_T2(refined_residence):
    # 각각의 매물이 어느 지하철역이랑 가깝고(1개) 얼마나 가까운지 맨하탄거리로 표시
    # 지하철csv 불러옴
    subway = open(f'{cwd}subway_refined.csv',
                  'r', encoding='utf8')
    subway_r = csv.reader(subway)
    subway_r_list = list(subway_r)
    # 중간결과를 담을 subway_list 생성
    subway_list = []

    # 매물리스트를 outer에 지하철리스트를 inner에 두고 각 매물에서 모든 지하철역과의 거리를 계산하여
    # 가장 가까운 지하철 역과 그 역과의 거리를 구함
    for index_r, i in enumerate(refined_residence):
        # 임시로 매물과 모든역과의 거리를 계산할 리스트
        temp = []
        for index_s, j in enumerate(subway_r_list):
            if(index_s == 0):
                continue
            temp.append(abs(i["lat"] - float(j[7])) +
                        abs(i["lon"] - float(j[8])))
            if(index_s == len(subway_r_list)-1):
                subway_list.append({"code": i["code"], "nearest": temp.index(
                    min(temp))+1, "subway_dist": min(temp)})

    subway.close()
    # 거리가 가까운 순으로 정렬함
    sorted_subway_list = sorted(
        subway_list, key=itemgetter('subway_dist'))

    # 최종결과를 담을 리스트 생성
    res = []

    len_sorted_subway_list = len(sorted_subway_list)

    # T2최종 가중치 추산을 위한 계산작업
    for index, i in enumerate(sorted_subway_list):
        res.append({"code": i["code"], "nearest": i["nearest"], "subway_dist": i["subway_dist"],
                    "T2_weight": 100*(1/len_sorted_subway_list)*(len_sorted_subway_list-index)})
    return res

    # 맨하탄거리로 서열을 매겨 총 개수로 나눈 후 100점 만점(1위) 부터 0점까지(꼴찌) 1위부터 높은 점수로 배열함
    # ex.총 매물이 50일 경우, 1위가 100점, 2위가 98점, 3위가 96점 ... 50위가 0점 (동률에 대한 고려는 추후에 함)
