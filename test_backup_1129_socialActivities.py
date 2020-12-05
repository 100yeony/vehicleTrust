import random
from pprint import pprint
from collections import OrderedDict
import time
from scipy.linalg import norm
import math
import json
# import pickle
from datetime import datetime
from matplotlib import pyplot as plt
import os
import numpy as np
# import sklearn.metrics as metrics
import numbers



def txt2list() :
    lists = []
    file = open('event_08_tab.txt', 'r')
    while True :
        line = file.readline().rstrip("\n")
        if line :
            line = line.split('\t')
            lists.append(line)
        else :
            break
    return lists


def make_real_Vdata(real_data):
    real_data_list = list()
    for i in real_data:
        real_data_list.append(i[14])
    return real_data_list


def change_VDI(v_info, data):
    # time_ = time.asctime(time.localtime(time.time()))  # Tue Nov 17 02:35:17 2020
    time_ = time.time() #1605548386.34553
    v_info['VDI']['createdData']['contents'] = data
    v_info['VDI']['createdData']['createdTime'] = time_

    sc = v_info['social_activities']['scoring']
    sh = v_info['social_activities']['sharing']
    v_info['VDI']['createdData']['score'] = sc*sh
    return v_info

def change_VDI_receivedData(v_info, data):
    # time_ = time.asctime(time.localtime(time.time()))  # Tue Nov 17 02:35:17 2020
    time_ = time.time() #1605548386.34553
    v_info['VDI']['receivedData']['contents'] = data
    v_info['VDI']['receivedData']['createdTime'] = time_
    v_info['VDI']['receivedData']['score'] = v_info['social_activities']['scoring']
    return v_info

def change_VTI(v_info, VT):
    if v_info['vid'] != '4' :
        ignoring = v_info['social_activities']['ignoring']
        score = v_info['VDI']['createdData']['score']
        time_temp = v_info['VDI']['createdData']['createdTime']
        createdTime = time_temp
        time_ = time.time()
        DR = 1/ignoring
        # print('=======>',score,createdTime, score*createdTime)
        # print(type(score), type(time_), time_)
        mul = score*time_
        # print(mul, type(mul))
        # DR = 1/ignoring + sum(list(score*time_))/len(list(score*time_))
    else:
        DR = 0
    AS = v_info['social_activities']['scoring'] + v_info['social_activities']['sharing']
    UR = norm(DR+AS)

    CF = 3  # of packets forwarded / avg number of packets observed at neighbors
    distanceij = 10
    connectivity = math.exp(-distanceij)
    NT = AS*connectivity*CF

    VT_updateTime = 0
    PVT = 0

    v_info['VTI']['DR'] = round(DR,2)
    v_info['VTI']['AS'] = round(AS,2)
    v_info['VTI']['NT'] = round(NT,2)
    v_info['VTI']['UR'] = round(UR,2)
    v_info['VTI']['VT'] = VT
    v_info['VTI']['connectivity'] = connectivity
    v_info['VTI']['CF'] = CF
    v_info['VTI']['VT_updateTime'] = VT_updateTime
    v_info['VTI']['PVT'] = PVT
    return v_info


def change_RTI(v_info, data):
    # original_data의 위치부분 가져오는 코드 짜기 : 21:경도(ㅇ) 22:위도(ㅇ)
    landom_num = [random.randint(1,3234) for i in range(2)]
    position = []
    for i in landom_num:
        position = [data[i][21], data[i][22]]
    # print('===>', position)
    v_info['RTI'][0]['position'] = position
    v_info['RTI'][0]['updateTime'] = time.asctime(time.localtime(time.time()))  # Tue Nov 17 02:35:17 2020
    v_info['RTI'][0]['vid'] = v_info['vid']
    v_info['RTI'][0]['VT'] = v_info['VTI']['VT']
    return v_info



class Vehicle:
    def __init__(self, vid, user):
        self.vid = vid
        self.user = user
        self.social_activities = {'info':{},'scoring':0, 'ignoring':0, 'sharing':0}
        # self.VDI = {'createdData':[{'contents':[], 'score':0,'createdTime':0,'GPS':0}],'receivedData':[{'contents':[], 'score':0,'createdTime':0,'GPS':0}]}
        self.VDI = {'createdData':[],'receivedData':[]}
        self.VTI = {'DR':0,'AS':0,'NT':0,'UR':0, 'VT':0, 'connectivity':0, 'CF':0,'VT_updateTime':0, 'PVT':0}
        self.RTI = []

    def update_social(self, social):
        self.social_activities = social
        # print('update social activities')


    def update_VDI(self, VDI):
        self.VDI = VDI
        # print('update VDI')

    def update_VTI(self, VTI):
        self.VTI = VTI
        # print('update VTI')

    def put_RTI(self, RTI):
        self.RTI.append(RTI)
        # print('append RTI')

    def printVehicle(self):
        vehicle_info = dict({
            'vid':self.vid,
            'user':self.user,
            'social_activities':self.social_activities,
            'VDI':self.VDI,
            'VTI':self.VTI,
            'RTI':self.RTI
            })
        return pprint(vehicle_info, width=100, indent=2)

    def __getitem__(self, item):
        return self.info[item]


class CustomEncoder(json.JSONEncoder):
     def default(self, o):
         if isinstance(o, datetime):
             return {'__datetime__': o.replace(microsecond=0).isoformat()}
         return {'__{}__'.format(o.__class__.__name__): o.__dict__}


def make_real_vehicleInfo(real_data, user):
    # print('user:', user)
    # print(real_data[13][13])
    for i in real_data:
        v_info = {}
        v_info['date'] = i[2]
        v_info['contents'] = i[14]
        v_info['GPS'] = i[15]
        if i[13] == user:
            v_info['user'] = i[13]
    return v_info


# def find_malicious_vehicle(dir):
#     files = os.listdir(dir)
#     for file in files:
#         full_file = os.path.join(dir, file)
#         with open('./data/'+file, 'rb') as f:
#             d = json.load(f)
#             for key,info in d.items():
#                 for nested_key in info:
#                     # print(info.items()) # (key, value)
#                     # print('===> [INFO]', nested_key + ':', info[nested_key])
#                     if int(info['vid']) in mal_vehicle:
#                         find_mal.append(int(info['vid']))
#     return find_mal



def make_performance(target,find):
    accuracy = np.mean(np.equal(target,find))
    right = np.sum(target * find == 1)
    precision = right / np.sum(find)
    recall = right / np.sum(target)
    f1 = 2 * precision*recall/(precision+recall)
    # print('==============================')
    # print('accuracy :',accuracy)
    # print('precision :', precision)
    # print('recall :', recall)
    # print('f1 :', f1)
    # print('==============================')


def make_chart(target, find):
    mal_v_num = [1, 2, 3, 4, 5, 6]
    net_and_social = [12, 12, 10, 14, 22, 24]
    net = [14, 15, 15, 22, 21, 12]
    social = [24, 4, 15, 13, 2, 21]
    plt.plot(mal_v_num, net_and_social, color='red', marker='*')
    plt.plot(mal_v_num, net, color='green',  marker='o')
    plt.plot(mal_v_num, social, color='blue',  marker='s')
    plt.legend(['network&social', 'network', 'social'])
    plt.xlabel('number of malicious vehicle')
    plt.ylabel('detection ratio')
    plt.title('Detection ratio by number of malicious vehicles')
    plt.show()

    chart = 0
    return chart


def fix_data(original_data):
    list = []
    for i in original_data:
        # i는 row
        temp = i[15]
        temp = temp[1:-2]    # 정제 : "36.56521844404542,127.43064572770757/" -> 36.56521844404542,127.43064572770757
        temp = temp.split('/') # 위도,경도가 한 세트!
        idx = original_data.index(i)
        # print('===>',original_data[idx][15])
        original_data[idx][15] = temp[0]
        # GPS가 없는 데이터를 삭제 : 8000 -> 5164개
        if i[15] != '':
            list.append(i)
    return list


class GeoUtil:
    """
    Geographical Utils
    """
    @staticmethod
    def degree2radius(degree):
        return degree * (math.pi/180)

    @staticmethod
    def get_harversion_distance(x1, y1, x2, y2, round_decimal_digits=5):
        """
        경위도 (x1,y1)과 (x2,y2) 점의 거리를 반환
        Harversion Formula 이용하여 2개의 경위도간 거래를 구함(단위:Km)
        """
        if x1 is None or y1 is None or x2 is None or y2 is None:
            return None
        assert isinstance(x1, numbers.Number) and -180 <= x1 and x1 <= 180
        assert isinstance(y1, numbers.Number) and  -90 <= y1 and y1 <=  90
        assert isinstance(x2, numbers.Number) and -180 <= x2 and x2 <= 180
        assert isinstance(y2, numbers.Number) and  -90 <= y2 and y2 <=  90

        R = 6371 # 지구의 반경(단위: km)
        dLon = GeoUtil.degree2radius(x2-x1)
        dLat = GeoUtil.degree2radius(y2-y1)

        a = math.sin(dLat/2) * math.sin(dLat/2) \
            + (math.cos(GeoUtil.degree2radius(y1)) \
              *math.cos(GeoUtil.degree2radius(y2)) \
              *math.sin(dLon/2) * math.sin(dLon/2))
        b = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return round(R * b, round_decimal_digits)

    @staticmethod
    def get_euclidean_distance(x1, y1, x2, y2, round_decimal_digits=5):
        """
        유클리안 Formula 이용하여 (x1,y1)과 (x2,y2) 점의 거리를 반환
        """
        if x1 is None or y1 is None or x2 is None or y2 is None:
            return None
        assert isinstance(x1, numbers.Number) and -180 <= x1 and x1 <= 180
        assert isinstance(y1, numbers.Number) and  -90 <= y1 and y1 <=  90
        assert isinstance(x2, numbers.Number) and -180 <= x2 and x2 <= 180
        assert isinstance(y2, numbers.Number) and  -90 <= y2 and y2 <=  90

        dLon = abs(x2-x1) # 경도 차이
        if dLon >= 180:   # 반대편으로 갈 수 있는 경우
            dLon -= 360   # 반대편 각을 구한다
        dLat = y2-y1      # 위도 차이
        return round(math.sqrt(pow(dLon,2)+pow(dLat,2)),round_decimal_digits)


###############################  main start ####################################
original_data = txt2list()
del(original_data[0]) # delete 1 row
# print(original_data)

# ------ GPS 집합을 한개의 위도,경도 세트만 남기고 수정 ---------
original_data = fix_data(original_data)

#===================================================================
#--------------------------사용자 정제 start-------------------------
#===================================================================
reporters_origin = []
reporters = []
for i in original_data :
    reporters_origin.append(i[10])
    # 사람이 제보한 경우만 필터링하면 데이터가 8000 -> 3021개로 줄어듦
    # reporters_origin : 137
    # reporters : 126명 (필터링 후)
    # filtered reporter : 11개, {'교통정보센터', '원미가스충전소', '시화주유소', '청도1주유소', '송내지구대', '정보상황실', '애청자', '대명군경합동검문소', '서해가스충전소', '트위터', '그린주유소'}
    if len(i[10])<=3 and i[10]!='애청자' and i[10]!='트위터':
        reporters.append(i[10])

reporters_origin = set(reporters_origin)
reporters = set(reporters)
filtered_reporter = reporters_origin - reporters

# print('==> reporters_origin:', len(reporters_origin)) # 103개(기관포함)
# print(reporters_origin)
# print('==> reporters :', len(reporters)) # 96명
# print(reporters)
# print('==> filtered_reporter:', len(filtered_reporter), filtered_reporter)

reporters = list(reporters)

for i in reporters:
    vehicle = Vehicle(f'{reporters.index(i)}', i)

    created_data = []
    for c in original_data:
        if i == c[10]:
            # print('====>',c[15], type(c[15]))
            if c[15] != '':
                data = {'contents':c[14], 'score':0,'createdTime':(c[2],c[3]),'GPS':c[15], 'vid':f'{reporters.index(i)}'}
                created_data.append(data)
            # else:
            #     data = {'contents':c[14], 'score':0,'createdTime':(c[2],c[3]),'GPS':'None'}

            vehicle.update_VDI({'createdData':created_data,'receivedData':{'contents':[], 'score':0,'createdTime':0}})

            ###소셜행위 이루어지는 함수를 호출?###

            # social_activity = [{'contents':'test11111', 'score':0,'createdTime':0}, {'contents':'test2222222', 'score':0,'createdTime':0}]
            # social_activity = json.dumps(social_activity)
            # print('??', social_activity)
            # vehicle.update_VDI(created_data,social_activity)


            # first = 1
            # second = 2
            # con = GeoUtil.get_euclidean_distance(126.97843, 37.56668, 127.02758, 37.49794)
            # vehicle.update_VTI({'DR':0,'AS':0,'NT':0,'UR':0, 'VT':0, 'connectivity':con, 'CF':0,'VT_updateTime':0, 'PVT':0})

            # <<가데이터 넣기>>
            # !!!!!!!!!!!!!!!!!!!!!!여기를 수정하시오 ... social activities를 랜덤하게 choice? vehicle 값을 세팅해주기
            # social_info = [('response:', 0), ('received data:',0), ('not used data:', 0), ('redistributed data:',0)]
            # social_activity = {'info':social_info,'scoring':0, 'ignoring':0, 'sharing':0}
            social_info = {'response':0, 'received_data':0, 'not_used_data':0, 'redistributed_data':0}
            social_activity = {'info':social_info,'scoring':0, 'ignoring':0, 'sharing':0}

            vehicle.update_social(social_activity)

#===================================================================
#-------------------------- 직렬화&역직렬화 ---------------------------
#===================================================================
    # << 직렬화 >>
    with open('./data/'+f'vehicle{i}_info.json', mode='w', encoding='UTF8') as f:
        json.dump(vehicle, f, cls=CustomEncoder, indent=2)
        # print('complete!!')

    # << 역직렬화 >>
    with open('./data/'+f'vehicle{i}_info.json', 'rb') as f:
        data = json.load(f)
        # print(type(data))
        # pprint(data, width=100, indent=2)

#         for key,info in data.items():
#             for nested_key in info:
#                 # print(info.items()) # (key, value)
#                 # print('===> [INFO]', nested_key + ':', info[nested_key])
#                 print(info['vid'])
#                 if info['vid'] in [10,15,25,100]:
#                     print(info['vid'])
#                     find_mal.append(info[nested_key])
#                     # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
#                     # print('===> [INFO]', info)
#             # print('==================================================')
# print(find_mal)
#===================================================================
#--------------------------직렬화 end---------------------------
#===================================================================


#-----------------------find_malicious_vehicle-----------------
# mal_vehicle = [1,2,89,123,40,45,50]
mal_vehicle = sorted([random.randint(1,126) for i in range(5)])
# print('landom mal_vehicle : ', mal_vehicle)
find_mal = []

# find_mal_temp = find_malicious_vehicle('./data')
# find_mal = sorted(list(set(find_mal_temp)))
# print('mal_vehicle:', mal_vehicle)
# print('find_mal:',find_mal)
#---------------------find_malicious_vehicle end-----------------

#-----------------precision, recall, f-score-----------------
# target = np.array(mal_vehicle)
# find = np.array(find_mal)
# make_performance(target, find)
#-------------------precision, recall, f-score end -----------------






#-------------------social activity -------------------------
# 차량 간 데이터 공유 : 일단 랜덤하게?
v1 = ''
v2 = ''

def choice_vehicles(v1, v2):
    # << 역직렬화 >>
    with open('./data/'+f'vehicle김남수_info.json', 'rb') as f:
        v1 = json.load(f)
    with open('./data/'+f'vehicle김대규_info.json', 'rb') as f:
        v2 = json.load(f)
    return v1, v2

v1, v2 = choice_vehicles(v1,v2)
print('김남수 :', v1)
print('--')
print('김대규 :', v2)


'''
랜덤하게 v1, v2를 설정하고 social exchange를 수행
초이스 함수로 차량 결정
해당 두 차량은 데이터를 교환
이때 vinfo에 VDI 가 업데이트 됨. 리스트에 append시키기
그리고 소셜행위가 발생하면
소셜 행위 3가지 타입 중 한가지를 랜덤하게 혹은 순차적으로 선택하는데
이때 count를 올려줌. 리턴되는 count로 소셜행위 계싼
점수부여, 무시, 재배포 카운트를 올려줌. 그러니까 랜덤함수가 수행되는 것

소셜행위 랜덤 선택
데이터 교환 후
점수부여, 무시, 재배포
'''
v1_temp = ''
v2_temp = ''

def social_acting_exchange(v1, v2, v1_temp, v2_temp):
    mal2_vehicle = [14,24]
    v1_data = ''
    v2_data = ''
    v1_vid = 0
    v2_vid = 0
    #============== vid 저장 ================
    for key, info in v1.items():
        for second_key in info:
            v1_vid = info['vid']

    for key, info in v2.items():
        for second_key in info:
            v2_vid = info['vid']

    mal2_vehicle[0] = v1_vid
    print('mal2_vehicle :', mal2_vehicle, 'v1 vid : ', v1_vid, 'v2 vid :', v2_vid)

    #==============데이터 저장 ================
    for key, info in v1.items():
        for second_key in info:
            # if(second_key == 'VDI'):
            real_info = info['VDI']
            for third_key in real_info:
                v1_data = real_info['createdData']

    for key, info in v2.items():
        for second_key in info:
            # if(second_key == 'VDI'):
            real_info = info['VDI']
            for third_key in real_info:
                v2_data = real_info['createdData']

    #==============데이터 교환 ================
    for key, info in v1.items():
        for second_key in info:
            # if(second_key == 'VDI'):
            real_info = info['VDI']
            for third_key in real_info:
                real_info['receivedData'] = v2_data.copy()

    for key, info in v2.items():
        for second_key in info:
            # if(second_key == 'VDI'):
            real_info = info['VDI']
            for third_key in real_info:
                real_info['receivedData'] = v1_data.copy()

    #===========점수 부여=================
    # if v2_vid not in mal_vehicle:
    #     for key, info in v2.items():
    #         for second_key in info:
    #             real_info = info['social_activities']
    #             for third_key in real_info:
    #                 real_info['scoring'] = random.randint(6,10)
    # else:
    #     for key, info in v2.items():
    #         for second_key in info:
    #             real_info = info['social_activities']
    #             for third_key in real_info:
    #                 real_info['scoring'] = random.randint(1,5)

    # -------------social_activity[info] 값 랜덤하게 생성-------------

    for key, second_info in v1.items():
        for second_key in second_info:
            third_info = second_info['social_activities']
            for third_key in third_info:
                # print(real_info['info'])
                for fourth_key in third_info['info']:
                    v1_temp = third_info['info']

    for key, second_info in v2.items():
        for second_key in second_info:
            third_info = second_info['social_activities']
            for third_key in third_info:
                # print(real_info['info'])
                for fourth_key in third_info['info']:
                    v2_temp = third_info['info']


    for i in v1_temp:
        # print(temp['response'])
        v1_temp['response'] = random.randint(1,10)
        v1_temp['received_data'] = random.randint(1,10)
        v1_temp['not_used_data'] = random.randint(1,10)
        v1_temp['redistributed_data'] = random.randint(1,10)

    for i in v2_temp:
        # print(temp['response'])
        v2_temp['response'] = random.randint(1,10)
        v2_temp['received_data'] = random.randint(1,10)
        v2_temp['not_used_data'] = random.randint(1,10)
        v2_temp['redistributed_data'] = random.randint(1,10)

    print(v1_temp, v2_temp)

    # ------------- 소셜 점수 계산  -------------


    # for key, info in v2.items():
    #     for second_key in info:
    #         real_info = info['social_activities']
    #         for third_key in real_info:
    #             real_info['scoring'] = random.randint(6,10)




    # # -------------v1 점수부여 -------------
    # if v1_vid not in mal_vehicle:
    #     # print(v1_vid, mal2_vehicle, '?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #     for key, info in v1.items():
    #         for second_key in info:
    #             real_info = info['social_activities']
    #             for third_key in real_info:
    #                 real_info['scoring'] = random.randint(6,10)
    # else:
    #     for key, info in v1.items():
    #         for second_key in info:
    #             real_info = info['social_activities']
    #             for third_key in real_info:
    #                 real_info['scoring'] = random.randint(1,5)
    #
    # # -------------v2 점수부여 -------------
    # if v2_vid not in mal_vehicle:
    #     for key, info in v2.items():
    #         for second_key in info:
    #             real_info = info['social_activities']
    #             for third_key in real_info:
    #                 real_info['scoring'] = random.randint(6,10)
    # else:
    #     for key, info in v2.items():
    #         for second_key in info:
    #             real_info = info['social_activities']
    #             for third_key in real_info:
    #                 real_info['scoring'] = random.randint(1,5)

    # # #==============무시==================
    # for key, info in v1.items():
    #     for second_key in info:
    #         real_info = info['social_activities']
    #         for third_key in real_info:
    #             real_info['ignoring'] = random.randint(1,3)
    #
    # for key, info in v2.items():
    #     for second_key in info:
    #         real_info = info['social_activities']
    #         for third_key in real_info:
    #             real_info['ignoring'] = random.randint(1,3)
    #
    # # #=============재배포==================
    # for key, info in v1.items():
    #     for second_key in info:
    #         real_info = info['social_activities']
    #         for third_key in real_info:
    #             real_info['sharing'] = random.randint(1,5)
    #
    # for key, info in v2.items():
    #     for second_key in info:
    #         real_info = info['social_activities']
    #         for third_key in real_info:
    #             real_info['sharing'] = random.randint(1,5)


    return v1, v2, v1_temp, v2_temp


v1, v2, v1_temp, v2_temp = social_acting_exchange(v1, v2, v1_temp, v2_temp)
# pprint(v1)
# print('--')
# pprint(v2)

response=0
received_data=0
not_used_data=0
redistributed_data=0

def set_social_info(v1_temp, response, received_data, not_used_data, redistributed_data):
    for i in v1_temp:
        response = v1_temp['response']
        received_data = v1_temp['received_data']
        not_used_data = v1_temp['not_used_data']
        redistributed_data = v1_temp['redistributed_data']
    return response, received_data, not_used_data, redistributed_data

response, received_data, not_used_data, redistributed_data = set_social_info(v1_temp, response, received_data, not_used_data, redistributed_data)
print(response, received_data, not_used_data, redistributed_data)

# v_info['social_activities']['scoring'] = round(response/received_data,2)
# v_info['social_activities']['ignoring'] = round(not_used_data/received_data,2)
# v_info['social_activities']['sharing'] = round(redistributed_data/received_data,2)


scoring = round(response/received_data,2)
ignoring = round(not_used_data/received_data,2)
sharing = round(redistributed_data/received_data,2)
print(scoring, ignoring, sharing)

#-----------------connectivity--------------------------
# 서울시청 126.97843, 37.56668
# 강남역   127.02758, 37.49794
# 방법1)
dist = GeoUtil.get_euclidean_distance(126.97843, 37.56668, 127.02758, 37.49794)
# print(dist)
# 방법2)
con = GeoUtil.get_harversion_distance(126.97843, 37.56668, 127.02758, 37.49794)
# print(con)


#소셜행위가 이루어짐과 동시에 거리 계산과 데이터 교환 및 소셜 점수가 올라가야 함 !
# 1. 데이터 교환
# 2. 거리 계산
# 3. 소셜 점수 계산

#-----------------connectivity end--------------------------


def find_malicious_vehicle(dir):
    files = os.listdir(dir)
    for file in files:
        full_file = os.path.join(dir, file)
        with open('./data/'+file, 'rb') as f:
            d = json.load(f)
            for key,info in d.items():
                for nested_key in info:
                    # print(info.items()) # (key, value)
                    # print('===> [INFO]', nested_key + ':', info[nested_key])
                    if int(info['vid']) in mal_vehicle:
                        find_mal.append(int(info['vid']))
    return find_mal
