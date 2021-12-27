# TOP5 골라서 이 주변 정보들 가져옴

def filter_top5(total):
    # 5개 추려서 위도, 경도 가져옴
    top5 = []
    for index, i in enumerate(total):
        if index == 5:
            break
        top5.append(i)
    # 그 위도,경도로 주변 근린시설 정보까지 조합하여 반환

    return top5
