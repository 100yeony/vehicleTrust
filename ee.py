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
'''
0:(기본키)
1:접수번호
2:접수일o
3:시간o
4:방송시간
5:전송
6:중요o
7:방송o
8:DLS
9:제보유형
10:제보자o
11:TYPE
12:제보처
13:접수자o
14:내용o
15:GPS(포인트 집합)o
'''


def csv2list() :
    lists = []
    file = open('event_08.csv', 'r', encoding='UTF8')
    while True :
        line = file.readline().rstrip("\n")
        if line :
            line = line.split(",")
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
    def __init__(self, vid):
        self.vid = vid
        self.social_activities = {'info':{},'scoring':0, 'ignoring':0, 'sharing':0}
        self.VDI = {'createdData':{'contents':[], 'score':0,'createdTime':0},'receivedData':{'contents':[], 'score':0,'createdTime':0}}
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
    print('user:', user)
    # print(real_data[13][13])
    for i in real_data:
        v_info = {}
        v_info['date'] = i[2]
        v_info['contents'] = i[14]
        v_info['GPS'] = i[15]
        if i[13] == user:
            v_info['user'] = i[13]
    return v_info



###############################  main start ####################################

original_data = csv2list()
# print(original_data)
del(original_data[0]) # delete 1 row

#==========================사용자 정제=========================
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

print('==> reporters_origin:', len(reporters_origin))
print(reporters_origin)
print('==> reporters :', len(reporters))
print(reporters)
print('==> filtered_reporter:', len(filtered_reporter), filtered_reporter)

for i in reporters:
    # set vehicle user! 객체로! vehicle클래스를 이용해서 객체 생성할 것. 그럼 i의 개수만큼나오겟지
#==========================사용자 정제=========================
