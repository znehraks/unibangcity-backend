from operator import itemgetter
cwd = "python_code/data/"
# 매물 수로 난도 가중치를 구함(나온 refined_items의 count가 많은 것 순으로 높은 점수를 매겨서 등수 별로 순차적인 가중치를 정함
# 예. 매물이 총 50개이면 1위 100점, 2위 98점, 3위 96점 ... 50위 0점)


def cal_T5(refined_residence):
    sorted_count_list = sorted(
        refined_residence, key=itemgetter('count'), reverse=True)

    # 최종결과를 담을 리스트 생성
    res = []

    len_sorted_count_list = len(sorted_count_list)

    # T4최종 가중치 추산을 위한 계산작업
    for index, i in enumerate(sorted_count_list):
        res.append({"code": i["code"], "count": i["count"],
                    "T5_weight": 100*(1/len_sorted_count_list)*(len_sorted_count_list-index)})
    return res
