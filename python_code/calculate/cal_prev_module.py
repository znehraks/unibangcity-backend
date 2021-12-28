
def cal_prev(Q3Answer, Q4Answer, Q5Answer):
    weights = [
        {"code": "T1", "w1": 50, "w2": 10, "w3": 5, "w4": 20, "w5": 15},
        {"code": "T2", "w1": 15, "w2": 50, "w3": 5, "w4": 20, "w5": 10},
        {"code": "T3", "w1": 5, "w2": 5, "w3": 65, "w4": 20, "w5": 5},
        {"code": "T4", "w1": 20, "w2": 10, "w3": 10, "w4": 50, "w5": 10},
        {"code": "T5", "w1": 15, "w2": 10, "w3": 5, "w4": 20, "w5": 50}, ]
    default_Q3_weight = 0.5
    default_Q4_weight = 0.3
    default_Q5_weight = 0.2
    sum_w1 = 0
    sum_w2 = 0
    sum_w3 = 0
    sum_w4 = 0
    sum_w5 = 0
    for i in weights:
        if i["code"] == Q3Answer:
            sum_w1 += default_Q3_weight * i["w1"]
            sum_w2 += default_Q3_weight * i["w2"]
            sum_w3 += default_Q3_weight * i["w3"]
            sum_w4 += default_Q3_weight * i["w4"]
            sum_w5 += default_Q3_weight * i["w5"]
        elif i["code"] == Q4Answer:
            sum_w1 += default_Q4_weight * i["w1"]
            sum_w2 += default_Q4_weight * i["w2"]
            sum_w3 += default_Q4_weight * i["w3"]
            sum_w4 += default_Q4_weight * i["w4"]
            sum_w5 += default_Q4_weight * i["w5"]
        elif i["code"] == Q5Answer:
            sum_w1 += default_Q5_weight * i["w1"]
            sum_w2 += default_Q5_weight * i["w2"]
            sum_w3 += default_Q5_weight * i["w3"]
            sum_w4 += default_Q5_weight * i["w4"]
            sum_w5 += default_Q5_weight * i["w5"]
    return (sum_w1, sum_w2, sum_w3, sum_w4, sum_w5)
