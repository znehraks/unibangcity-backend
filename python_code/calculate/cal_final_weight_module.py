from operator import itemgetter
# 모든 매물의 점수에 가중치를 곱하여 환산한 최종 값을 구한다.


def cal_final_weight(T1, T2, T3, T4, T5, w1, w2, w3, w4, w5,
                     first_weight,
                     second_weight,
                     third_weight):
    # lgeo 별로 lgeo 순으로 정렬,
    sorted_T1 = sorted(T1, key=itemgetter('code'))
    sorted_T2 = sorted(T2, key=itemgetter('code'))
    sorted_T3 = sorted(T3, key=itemgetter('code'))
    sorted_T4 = sorted(T4, key=itemgetter('code'))
    sorted_T5 = sorted(T5, key=itemgetter('code'))

    # T1,T2,T3,T4,T5 모두 더함
    res = []
    for i in range(0, len(sorted_T1)):
        res.append({
            "code": sorted_T1[i]["code"],
            "T1": round(sorted_T1[i]["T1_weight"]*float(w1)/100),
            "T2": round(sorted_T2[i]["T2_weight"]*float(w2)/100),
            "T3": round(sorted_T3[i]["T3_weight"]*float(w3)/100),
            "T4": round(sorted_T4[i]["T4_weight"]*float(w4)/100),
            "T5": round(sorted_T5[i]["T5_weight"]*float(w5)/100),
            "total_weight": round(sorted_T1[i]["T1_weight"]*float(w1)/100 +
                                  sorted_T2[i]["T2_weight"]*float(w2)/100 +
                                  sorted_T3[i]["T3_weight"]*float(w3)/100 +
                                  sorted_T4[i]["T4_weight"]*float(w4)/100 +
                                  sorted_T5[i]["T5_weight"]*float(w5)/100),
            "lat": sorted_T1[i]["lat"],
            "lon": sorted_T1[i]["lon"],
        })
    # total 내림차순으로 sorting함
    avgs = [sum(i["T1"] for i in res)/len(res),
            sum(i["T2"]
                for i in res)/len(res),
            sum(i["T3"]
                for i in res)/len(res),
            sum(i["T4"]
                for i in res)/len(res),
            sum(i["T5"] for i in res)/len(res),
            sum(i["total_weight"] for i in res)/len(res), ]
    res_2 = []
    res_sorted = sorted(res, key=itemgetter('total_weight'), reverse=True)
    rank = 0
    for index, i in enumerate(res_sorted):
        if(i[first_weight] >= avgs[int(str(first_weight).split("T")[1])-1] or i[second_weight] >= avgs[int(str(second_weight).split("T")[1])-1] or i[third_weight] >= avgs[int(str(third_weight).split("T")[1])-1] or i["total_weight"] >= avgs[5]):
            rank += 1
            res_2.append({
                "rank": rank,
                "code": i["code"],
                "T1": i["T1"],
                "T2": i["T2"],
                "T3": i["T3"],
                "T4": i["T4"],
                "T5": i["T5"],
                "total_weight": i["total_weight"],
                "거리": i["T1"],
                "역세권": i["T2"],
                "가성비": i["T3"],
                "안전": i["T4"],
                "매물": i["T5"],
                "총점": i["total_weight"],
                "lat": i["lat"],
                "lon": i["lon"],
                "T1_avg": avgs[0],
                "T2_avg": avgs[1],
                "T3_avg": avgs[2],
                "T4_avg": avgs[3],
                "T5_avg": avgs[4],
                "total_weight_avg": avgs[5],
                "평균 거리": avgs[0],
                "평균 역세권": avgs[1],
                "평균 가성비": avgs[2],
                "평균 안전": avgs[3],
                "평균 매물": avgs[4],
                "평균 총점": avgs[5],
                "rooms_id": [],
                "rooms_type": [],
                "rooms_location_lat": [],
                "rooms_location_lon": [],
                "rooms_hash_tags_count": [],
                "rooms_hash_tags": [],
                "rooms_desc": [],
                "rooms_desc2": [],
                "rooms_img_url_01": [],
                "rooms_price_title": [],
                "rooms_selling_type": [],
            })
        else:
            continue

    return res_2
