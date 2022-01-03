import io
import sys
from calculate.cal_prev_module import cal_prev
from scrapper.get_residence_address_module import get_residence_address
from scrapper.find_rooms_module import find_rooms

from calculate.cal_T1_module import cal_T1
from calculate.cal_T2_module import cal_T2
from calculate.cal_T3_module import cal_T3
from calculate.cal_T4_module import cal_T4
from calculate.cal_T5_module import cal_T5
from calculate.cal_final_weight_module import cal_final_weight
from calculate.filter_top5_module import filter_top5

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


# 이 Top에 포함되는 항목의 구체적인 정보 서술 및 시각화 => 는 아마 프론트에서
# 지도에 마크로 표시해주는 방법도 좋으리라 생각함 + 매물 및 동네의 추가 정보까지 제공 => 는 아마 프론트에서

##################################################
# 얻어온 매물리스트에서 다방에서 한 번더 request를 보낸뒤 해당 매물 동그라미에서 가장 가까운 매물정보를 여러개 얻어옴
###################################################

univ_name = sys.argv[1]
univ_lon = float(sys.argv[2])
univ_lat = float(sys.argv[3])
limit_dist = float(sys.argv[4])
first_weight = sys.argv[5]
second_weight = sys.argv[6]
third_weight = sys.argv[7]
w1, w2, w3, w4, w5 = cal_prev(first_weight, second_weight, third_weight)

# univ_name = "숙명여자대학교"
# univ_lon = 126.9645778
# univ_lat = 37.5459469
# limit_dist = 846
# first_weight = "T1"
# second_weight = "T2"
# third_weight = "T3"
# w1 = "30.5"
# w2 = "21"
# w3 = "17"
# w4 = "20"
# w5 = "11.5"

refined_residence = get_residence_address(univ_lat, univ_lon)
T1 = cal_T1(refined_residence, univ_lon, univ_lat, limit_dist)

T2 = cal_T2(T1)
T3 = cal_T3(T1)
T4 = cal_T4(T1)
T5 = cal_T5(T1)
total = cal_final_weight(T1, T2, T3, T4, T5, w1, w2, w3, w4, w5,
                         first_weight,
                         second_weight,
                         third_weight)
top5 = filter_top5(total)
top5_with_rooms = find_rooms(top5)
# top5_with_rooms = json.dumps(top5_with_rooms)

print(top5_with_rooms)
