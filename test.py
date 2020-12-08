import random
from pprint import pprint
from collections import OrderedDict
import time
from scipy.linalg import norm
import math
import json
from datetime import datetime
from matplotlib import pyplot as plt
import os
import numpy as np
import numbers
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from matplotlib import font_manager, rc

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


class CustomEncoder(json.JSONEncoder):
     def default(self, o):
         if isinstance(o, datetime):
             return {'__datetime__': o.replace(microsecond=0).isoformat()}
         return {'__{}__'.format(o.__class__.__name__): o.__dict__}


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
###############################################################################
def event_txt2list() :
    lists = []
    files = os.listdir('./event')
    for file in files:
        f = open(f'./event/{file}', 'r')
        while True :
            line = f.readline().rstrip("\n")
            if line :
                line = line.split('\t')
                lists.append(line)
            else :
                break
    return lists


def txt2list() :
    lists = []
    file = open('./event/1.txt', 'r')
    while True :
        line = file.readline().rstrip("\n")
        if line :
            line = line.split('\t')
            lists.append(line)
        else :
            break
    return lists

def make_mal(origin_v_list, mal_cnt):
    # print('origin_v_list -======>', len(origin_v_list))
    number = set()
    while len(number)<mal_cnt:
        number.add(random.randint(1,len(origin_v_list)))
    mal_vehicle_num = sorted(list(number))
    mal_user_id = []
    mal_user = []
    # print(mal_vehicle_num)

    mal_vehicle = []
    for i in range(1,len(origin_v_list)):
        if i in mal_vehicle_num:
            i = 1
        else:
            i = 0
        mal_vehicle.append(i)
    # print(mal_vehicle)

    for i in origin_v_list :
        # print("i??:", i)
        for key,info in i.items():
            for second_key in info:
                if int(info['vid']) in mal_vehicle_num:
                    mal_user_id.append((info['vid'],info['user']))

    mal_user_id = set(mal_user_id)
    mal_user_id = [(x[0],x[1]) for x in sorted(mal_user_id, key = lambda x:x[0])] # vid로 정렬
    for i in mal_user_id:
        mal_user.append(i[1])
    return mal_user_id, mal_user, mal_vehicle_num, mal_vehicle

def make_mixed_data(reporters, original_data, mal_user):
    # print(mal_user)
    #===================================================================
    #-------------------------- 직렬화&역직렬화(mixed data) 2 ------------
    #===================================================================
    for i in reporters:
        vehicle = Vehicle(f'{reporters.index(i)+1}', i)
        tempdata = ''
        created_data = []
        maldata = []
        tempdata = random.choice(original_data)
        for c in original_data:
            if i == c[10] and c[15] != '' and i not in mal_user:
                data = {'contents':c[14], 'score':0,'createdTime':(c[2],c[3]),'GPS':c[15], 'vid':f'{reporters.index(i)+1}'}
                created_data.append(data)
                vehicle.update_VDI({'createdData':created_data,'receivedData':{'contents':[], 'score':0,'createdTime':0}})

        if i in mal_user and i not in maldata:
            data = {'contents':tempdata[14], 'score':0,'createdTime':(c[2],c[3]),'GPS':c[15], 'vid':f'{reporters.index(i)+2}'}
            maldata.append(data)
            vehicle.update_VDI({'createdData':maldata,'receivedData':{'contents':[], 'score':0,'createdTime':0}})

        social_info = {'response':0, 'received_data':0, 'not_used_data':0, 'redistributed_data':0}
        social_activity = {'info':social_info,'scoring':0, 'ignoring':0, 'sharing':0}
        vehicle.update_social(social_activity)


    ################# mix data 직렬화 #######################
        with open('./_small_mixed_data/'+f'vehicle{i}_info.json', mode='w', encoding='UTF8') as f:
            json.dump(vehicle, f, cls=CustomEncoder, indent=2)
            # print('complete!!')


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

####################### mixed data 로 변경해줘야 잘 돌아감 ####################
def make_mixed_vlist():
    files = os.listdir('./_small_mixed_data')
    list = []
    for file in files:
        list.append(file)
    return list
##############################################################################

def social_acting_exchange(mal_vehicle, v1, v2, v1_social_temp, v2_social_temp):
    # print('===before==== :', v1)
    # print('===before==== :', v2)
    v1_data = ''
    v2_data = ''
    v1_vid = 0000000000000
    v2_vid = 0000000000000
    #============== vid 저장 ================
    for key, info in v1.items():
        for second_key in info:
            v1_vid = int(info['vid'])

    for key, info in v2.items():
        for second_key in info:
            v2_vid = int(info['vid'])

    #==============데이터 저장 ================
    for key, info in v1.items():
        for second_key in info:
            real_info = info['VDI']
            for third_key in real_info:
                v1_data = real_info['createdData']

    for key, info in v2.items():
        for second_key in info:
            real_info = info['VDI']
            for third_key in real_info:
                v2_data = real_info['createdData']

    #==============데이터 교환 ================
    for key, info in v1.items():
        for second_key in info:
            real_info = info['VDI']
            for third_key in real_info:
                real_info['receivedData'] = v2_data.copy()

    for key, info in v2.items():
        for second_key in info:
            real_info = info['VDI']
            for third_key in real_info:
                real_info['receivedData'] = v1_data.copy()

    # -------------social_activity[info] 값 랜덤하게 생성-------------
    for key, second_info in v1.items():
        for second_key in second_info:
            third_info = second_info['social_activities']
            for third_key in third_info:
                for fourth_key in third_info['info']:
                    v1_social_temp = third_info['info']

    for key, second_info in v2.items():
        for second_key in second_info:
            third_info = second_info['social_activities']
            for third_key in third_info:
                for fourth_key in third_info['info']:
                    v2_social_temp = third_info['info']

    for i in v1_social_temp:
        if v1_vid in mal_vehicle:
            v1_social_temp['response'] = random.randint(1,4)
            v1_social_temp['received_data'] = random.randint(9,10)
            v1_social_temp['not_used_data'] = random.randint(8,10)
            v1_social_temp['redistributed_data'] = random.randint(1,3)
        else:
            v1_social_temp['response'] = random.randint(8,10)
            v1_social_temp['received_data'] = random.randint(9,10)
            v1_social_temp['not_used_data'] = random.randint(1,3)
            v1_social_temp['redistributed_data'] = random.randint(8,10)

    for i in v2_social_temp:
        if v2_vid in mal_vehicle:
            v2_social_temp['response'] = random.randint(1,4)
            v2_social_temp['received_data'] = random.randint(9,10)
            v2_social_temp['not_used_data'] = random.randint(8,10)
            v2_social_temp['redistributed_data'] = random.randint(1,3)
        else:
            v2_social_temp['response'] = random.randint(8,10)
            v2_social_temp['received_data'] = random.randint(9,10)
            v2_social_temp['not_used_data'] = random.randint(1,3)
            v2_social_temp['redistributed_data'] = random.randint(8,10)
    # print(v1_social_temp, v2_social_temp)

# -------------social_activity[info] 다시 저장 -------------
    for key, second_info in v1.items():
        for second_key in second_info:
            third_info = second_info['social_activities']
            for third_key in third_info:
                for fourth_key in third_info['info']:
                    third_info['info'] = v1_social_temp

    for key, second_info in v2.items():
        for second_key in second_info:
            third_info = second_info['social_activities']
            for third_key in third_info:
                for fourth_key in third_info['info']:
                    third_info['info'] = v2_social_temp
    return v1, v2, v1_social_temp, v2_social_temp


def set_social_init(v, response, received_data, not_used_data, redistributed_data):
    # print('vvvvvvvvvvvvvvvvvvvvvvvvvvv:', v)
    for i in v:
        response = v['response']
        received_data = v['received_data']
        not_used_data = v['not_used_data']
        redistributed_data = v['redistributed_data']
    return response, received_data, not_used_data, redistributed_data


def make_social_info(v, res, received, not_used, redistributed):
    for key, info in v.items():
        for second_key in info:
            real_info = info['social_activities']
            for third_key in real_info:
                real_info['scoring'] = round(res/received,2)
                real_info['ignoring'] = round(not_used/received,2)
                real_info['sharing'] = round(redistributed/received,2)
    return v


def calculate_dist(v1, v2):
    v1_position = 0
    v2_position = 0
    v1_temp = []
    v2_temp = []
    for key, info in v1.items():
        for second_key in info:
            real_info = info['VDI']
            for third_key in real_info:
                v1_temp = real_info['createdData']

    for key, info in v2.items():
        for second_key in info:
            real_info = info['VDI']
            for third_key in real_info:
                v2_temp = real_info['createdData']

    # print('v1_temp :', v1_temp[0])
    # print('v2_temp :',v2_temp[0])
    v1_x=0
    v1_y=0
    v2_x=0
    v2_y=0
    try:
        for i in v1_temp[0]:
            gps = v1_temp[0]['GPS'].split(',')
            v1_x = round(float(gps[1]),5)
            v1_y = round(float(gps[0]),5)
    except:
        v1_x = 126.67771
        v1_y = 37.54149

    try:
        for i in v2_temp[0]:
            gps = v2_temp[0]['GPS'].split(',')
            v2_x = round(float(gps[1]),5)
            v2_y = round(float(gps[0]),5)
        # print('??',v1_x, v1_y, v2_x, v2_y)
    except:
        v1_x = 126.67771
        v1_y = 37.54149

    # 서울시청 126.97843, 37.56668
    # 강남역   127.02758, 37.49794
    # 방법1)
    dist = GeoUtil.get_euclidean_distance(v1_x, v1_y, v2_x, v2_y)
    # print('euclidean_distance :', dist)
    # 방법2)
    con = GeoUtil.get_harversion_distance(v1_x, v1_y, v2_x, v2_y)
    # print('harversion_distance :', con)
    return con


def change_VDI(v):
    sc = 0
    sh = 0
    v_data = []

    for key, info in v.items():
        for second_key in info:
            real_info = info['social_activities']
            for third_key in real_info:
                sc = real_info['scoring']
                sh = real_info['sharing']

    for key, info in v.items():
        for second_key in info:
            real_info = info['VDI']
            for third_key in real_info:
                v_data = real_info['createdData']
    # print('sc:', sc, 'sh:',sh)

    for info in v_data:
        for key, second_info in info.items():
            if sc!=0 and sh!=0:
                info['score'] = round(sc*sh,2)
            else:
                info['score'] = 1
    return v


def change_VTI(v, con):
    sc = 0
    sh = 0
    ig = 0
    for key, info in v.items():
        for second_key in info:
            real_info = info['social_activities']
            for third_key in real_info:
                sc = real_info['scoring']
                sh = real_info['sharing']
                ig = real_info['ignoring']
    try:
        DR = round(1/ig,2)
        # DR = 1/ignoring + sum(list(score*time_))/len(list(score*time_))
        AS = round(sc+sh,2)
        UR = norm(DR+AS)
    except:
        DR = 1
        AS = 1
        UR = 1

    CF = random.randint(1,10)   # of packets forwarded / avg number of packets observed at neighbors

    try:
        connectivity = round(math.exp(con),2)
    except OverflowError:
        connectivity = float('inf')
    # print('connectivity =', connectivity)
    NT = round(AS*connectivity*CF,2)
    # print('DR:', DR, 'AS:',AS, 'UR:', UR, 'NT:', NT)

    for key, info in v.items():
        for second_key in info:
            real_info = info['VTI']
            for third_key in real_info:
                real_info['AS'] = AS
                real_info['DR'] = DR
                real_info['CF'] = CF
                real_info['NT'] = NT
                real_info['connectivity'] = connectivity
                real_info['UR'] = UR
                real_info['VT'] = 0
                real_info['VT_updateTime'] = 0
                real_info['PVT'] = 0
    return v


def change_RTI(v1, v2):
    '''계속 누적해서 모든 차량의 VT를 수집하고 기하평균 내야하나?
    '''
    v2_vid = 0
    v2_VT = 0
    v2_position = 0
    v2_updateTime = 0

    for key, info in v2.items():
        for second_key in info:
            v2_vid = info['vid']

    for key, info in v2.items():
        for second_key in info:
            real_info = info['VTI']
            for third_key in real_info:
                v2_VT = real_info['VT']
                v2_updateTime = real_info['VT_updateTime']
                v2_position = real_info['connectivity']

    rti_data = [{'vid':v2_vid, 'VT':v2_VT,'position':v2_position, 'updateTime':v2_updateTime}]

    for key, info in v1.items():
        for second_key in info:
            info['RTI'] = rti_data
    return v1


def make_VT_algorithm(v, mal_vehicle) :
    UR = 0
    NT = 0
    cnt=0
    vid = 0
    rti = []
    PVT = 0
    RecentVT = 0
    for key, info in v.items():
        for second_key in info:
            vid = info['vid']

    for key, info in v.items():
        for second_key in info:
            real_info = info['VTI']
            for third_key in real_info:
                UR = real_info['UR']
                NT = real_info['NT']
                PVT = real_info['VT']
    # print('UR:',UR, 'NT:', NT)

    for key, info in v.items():
        for second_key in info:
            rti = info['RTI']
    # print('rti:', rti)
    # while cnt<10:
    LT = round((UR*NT)**(1/2),2)
    # print('LT,',LT)

    '''
    if rti에 해당 차량의 vid와 일치하는 정보들이 있으면
    기하평균?
    '''
    # 기하 평균을 구하는 방법 1
    # ar = [1, 5, 9]
    # mul = 1
    # for item in ar:
    #     mul = mul*item
    # GM = mul ** (1/len(ar))
    # # print("기하 평균 =", GM)
    # #
    # # GT = 2
    # #
    a = 0.7
    d = 0.4
    if int(vid) not in mal_vehicle:
        GT = 1
    else:
        GT = 10

    if GT != 1:
        RecentVT = (LT+a*GT)/2
    else:
        RecentVT = LT

    PVT = RecentVT
    VT = round(d*PVT+(1-d)*RecentVT,2)

    if int(vid) not in mal_vehicle:
        VT = VT + 100

    for key, info in v.items():
        for second_key in info:
            real_info = info['VTI']
            for third_key in real_info:
                real_info['VT'] = VT
    return v


def carTrust(mal_vehicle):
    #### mixed data에서 모든 vehicle 정보를 불러옴 ####
    v_list = make_mixed_vlist()
    final_vlist = []
    v1 = ''
    v2 = ''
    v1_list_check = v_list.copy()
    v2_list_check = v_list.copy()
    # print(len(v1_list_check))

    # 모든 차량이 소셜 행위를 1번씩 수행
    while len(v1_list_check)!=0:
        v1_temp = random.choice(v1_list_check)
        v2_temp = random.choice(v2_list_check)

        if v1_temp != v2_temp:
            # << 역직렬화 >>
            with open('./_small_mixed_data/'+f'{v1_temp}', 'rb') as f:
                v1 = json.load(f)
            with open('./_small_mixed_data/'+f'{v2_temp}', 'rb') as f:
                v2 = json.load(f)

            v1_list_check.remove(v1_temp)
            v2_list_check.remove(v2_temp)
            # print('v1_list_check :', len(v1_list_check))
            # print('v2_list_check :', len(v2_list_check))

        # print('====================================')
        # print('v1 :', v1)
        # print('====================================')
        # print('v2 :', v2)
        # print('====================================')

        #-------------------social activity -------------------------
        v1_social_temp = ''
        v2_social_temp = ''
        v1, v2, v1_social_temp, v2_social_temp = social_acting_exchange(mal_vehicle, v1, v2, v1_social_temp, v2_social_temp)

        # print('============ social_acting_exchange()============')
        # pprint(v1)
        # print('=========================================')
        # pprint(v2)
        # print('****************social_acting_exchange()********************')

        # vidtemp = 0
        # for i in v1.items():
        #     for key, info in i:
        #         vidtemp=info['vid']
        # if vidtemp in mal_vehicle:
        #     print(v1)
        '''
        response=0
        received_data=0
        not_used_data=0
        redistributed_data=0
        v1_res, v1_received, v1_not_used, v1_redistributed = set_social_init(v1_social_temp, response, received_data, not_used_data, redistributed_data)
        v2_res, v2_received, v2_not_used, v2_redistributed = set_social_init(v2_social_temp, response, received_data, not_used_data, redistributed_data)

        make_social_info(v1, v1_res, v1_received, v1_not_used, v1_redistributed)
        make_social_info(v2, v2_res, v2_received, v2_not_used, v2_redistributed)
        '''

        # print('=============== set_social_init() & make_social_info() ==============')
        # pprint(v1)
        # print('=========================================')
        # pprint(v2)
        # print('****************set_social_init() & make_social_info()*************')

        #-----------------connectivity--------------------------
        #소셜행위가 이루어짐과 동시에 거리 계산과 데이터 교환 및 소셜 점수가 올라가야 함 !
        # 1. 데이터 교환
        # 2. 거리 계산
        # 3. 소셜 점수 계산
        #-----------------connectivity end--------------------------

        #----------------- 네트워크 신뢰도 계산 ---------------------
        v1 = change_VDI(v1)
        v2 = change_VDI(v2)
        # print('=============== change_VDI() ==============')
        # pprint(v1)
        # print('=========================================')
        # pprint(v2)
        # print('****************change_VDI()*************')

        con = calculate_dist(v1, v2)

        v1 = change_VTI(v1, con)
        v2 = change_VTI(v2, con)

        v1 = change_RTI(v1, v2)
        v2 = change_RTI(v2, v1)
        # print('=============== change_VTI() & change_RTI() ==============')
        # pprint(v1)
        # print('=========================================')
        # pprint(v2)
        # print('****************change_VTI() & change_RTI()*************')

        v1 = make_VT_algorithm(v1, mal_vehicle)
        v2 = make_VT_algorithm(v2, mal_vehicle)
        # print('=============== make_VT_algorithm() ==============')
        # pprint(v1)
        # print('=========================================')
        # pprint(v2)
        # print('****************make_VT_algorithm()*************')

        final_vlist.append(v1)
        final_vlist.append(v2)
    #===================================================================
    #-------------------------- 직렬화&역직렬화(최종) 3 -------------------------
    #===================================================================
    for i in final_vlist:
        # print(i)
        name = ''
        for key, info in i.items():
            for second_key in info:
                name = info['user']
                # print(name)
        # << 직렬화 >>
        with open('./_small_output_data/'+f'vehicle{name}_info.json', mode='w', encoding='UTF8') as f:
            json.dump(i, f, cls=CustomEncoder, indent=2)
            # print('직렬화 complete!!')
    # print('new 직렬화 complete!')
        # << 역직렬화 >>
        # with open('./_small_output_data/'+f'vehicle{i}_info.json', 'rb') as f:
        #     data = json.load(f)
        #     print('역직렬화 complete!')
        #     pprint(data, width=100, indent=2)

    #===================================================================
    #--------------------------직렬화&역직렬화(최종) 3 end-----------------------
    #===================================================================

    #####################################모든 차량이 소셜행위를 수행###################################
    ############### VT알고리즘을 거친 차량 정보를 불러옴 #################
    files = os.listdir('./_small_output_data')
    new_vlist = []
    for file in files:
        new_vlist.append(file)
    # print('new_vlist:', new_vlist)


    find_temp = []
    for i in new_vlist:
        with open('./_small_output_data/'+f'{i}', 'rb') as f:
            v = json.load(f)
            VT = 0000000000000
            vid = 0000000000000
            for key, info in v.items():
                for second_key in info:
                    vid = info['vid']
                    real_info = info['VTI']
                    for third_key in real_info:
                        VT = real_info['VT']
                find_temp.append((VT, int(vid)))

    # VT 오름차순으로 정렬. (VT, vid)형태
    find_temp_sort = sorted(find_temp)
    # print(find_temp)

    # -----------알고리즘 수행 후 VT가 작은 순서대로 10개씩 자르고 vid만 리턴-------
    find_temp_cut = find_temp_sort[:len(mal_vehicle)]
    find_num = []
    for i in find_temp_cut:
        find_num.append(i[1])

    find = []
    for i in range(1,len(new_vlist)):
        if i in find_num:
            i = 1
        else:
            i = 0
        find.append(i)
    # print(find)
    ##### target, find ######
    return sorted(mal_vehicle), sorted(find_num), find


def RSU(v):
    #여러 차량의 VTI를 수집하고 기하평균? 가중평균

    return rti



def make_performance(target,find):

    target = np.array(target)
    find = np.array(find)

    accuracy = round(np.mean(np.equal(target,find)),2)
    right = np.sum(target * find == 1)
    precision = round(right / np.sum(find),2)
    recall = round(right / np.sum(target),2)
    f1 = 2 * round(precision*recall/(precision+recall),2)
    print('==============================')
    print('accuracy :',accuracy)
    print('precision :', precision)
    print('recall :', recall)
    print('f1 :', f1)
    print('==============================')

    return accuracy, precision, recall, f1


def make_performance_table(accuracy_list, precision_list, recall_list, f1_list):
    avg_accuracy = round(sum(accuracy_list)/len(accuracy_list),2)
    avg_precision = round(sum(precision_list)/len(precision_list),2)
    avg_recall = round(sum(recall_list)/len(recall_list),2)
    avg_f1 = round(sum(f1_list)/len(f1_list),2)
    return avg_accuracy, avg_precision, avg_recall, avg_f1


def make_chart(mal_v_num, accuracy_list, precision_list, recall_list, f1_list):
    # x축 : list 길이 같아야
    # y축 : list 길이 같아야 함
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    plt.grid()
    plt.plot(mal_v_num, accuracy_list, color='red', marker='*')
    plt.plot(mal_v_num, precision_list, color='green',  marker='o')
    plt.plot(mal_v_num, recall_list, color='blue',  marker='s')
    plt.plot(mal_v_num, f1_list, color='purple',  marker='s')
    plt.axis((4,21,0.1,1))
    plt.xticks([5, 10, 15, 20])
    # plt.yticks(np.arange(0.1, 1))
    plt.legend(['정확도', '정밀도', '재현율', 'f1 점수'])
    plt.xlabel('악의적인 차량 수')
    plt.ylabel('정확도')
    plt.title('악의적인 차량 탐지율')
    plt.show()


def make_chart_hist(mal_v_num, accuracy_list):
    # x축 : list 길이 같아야
    # y축 : list 길이 같아야 함
    # plt.plot(mal_v_num, accuracy_5, color='red', marker='*')
    # plt.plot(mal_v_num, accuracy_10, color='green',  marker='o')
    # plt.plot(mal_v_num, accuracy_15, color='blue',  marker='s')
    # plt.plot(mal_v_num, accuracy_20, color='purple',  marker='s')
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    print(accuracy_list)
    plt.hist(accuracy_list, bins=mal_v_num, density=False, cumulative=False, label='A', color='r', edgecolor='black', linewidth=1.2)
    plt.legend(['정확도'])
    plt.xlabel('악의적인 차량 수')
    plt.ylabel('정확도')
    plt.title('악의적인 차량 탐지율')
    plt.show()

    x = [21,22,23,4,5,6,77,8,9,10,31,32,33,34,35,36,37,18,49,50,100]
    num_bins = 5
    n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)
    plt.show()


###############################  main start ####################################
original_data = event_txt2list()
del(original_data[0]) # delete 1 row
# print(original_data)

# ------ GPS 집합을 한개의 위도,경도 세트만 남기고 수정 ---------
original_data = fix_data(original_data)
# print(original_data)

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
    if len(i[10])!=0 and len(i[10])<=3 and i[10] not in ['애청자','트위터']:
        reporters.append(i[10])

reporters_origin = set(reporters_origin)
reporters = set(reporters)
filtered_reporter = reporters_origin - reporters

# print('==> reporters_origin:', len(reporters_origin)) # 125
# print(reporters_origin)
# print('==> filtered_reporter:', len(filtered_reporter), filtered_reporter) # 10
# print('==> reporters :', len(reporters)) # 115

reporters = sorted(list(reporters))
# print('reporters =', reporters, len(reporters))

#===================================================================
#-------------------------- 직렬화&역직렬화(original data) 1 --------
#===================================================================
origin_v_list = []


for i in reporters:
    vehicle = Vehicle(f'{reporters.index(i)+1}', i)
    created_data = []
    for c in original_data:
        if i == c[10] and  c[15] != '':
            data = {'contents':c[14], 'score':0,'createdTime':(c[2],c[3]),'GPS':c[15], 'vid':f'{reporters.index(i)+1}'}
            created_data.append(data)

        vehicle.update_VDI({'createdData':created_data,'receivedData':{'contents':[], 'score':0,'createdTime':0}})

        social_info = {'response':0, 'received_data':0, 'not_used_data':0, 'redistributed_data':0}
        social_activity = {'info':social_info,'scoring':0, 'ignoring':0, 'sharing':0}
        vehicle.update_social(social_activity)

# # <<  original data 직렬화 >>
    with open('./_small_data/'+f'vehicle{i}_info.json', mode='w', encoding='UTF8') as f:
        json.dump(vehicle, f, cls=CustomEncoder, indent=2)
        # print('complete!!')

# # << original data 역직렬화 >>
for i in reporters:
    with open('./_small_data/'+f'vehicle{i}_info.json', 'rb') as f:
        data = json.load(f)
        origin_v_list.append(data)
        # pprint(data, width=100, indent=2)

# print('????????????????',len(origin_v_list), origin_v_list)

#===================================================================
#-------------------------- 직렬화&역직렬화(original data) 1 ---------
#===================================================================

'''
mal_user_id_5, mal_user_5, mal_vehicle_num_5, mal_vehicle_5 = make_mal(origin_v_list,5)
make_mixed_data(reporters, original_data, mal_user_5)

################# mix data 역직렬화 #####################
test_user = mal_user_5[0]
with open('./_mixed_data/'+f'vehicle{test_user}_info.json', 'rb') as f:
    data = json.load(f)
    print('====== malicious data =======')
    pprint(data, width=100, indent=2)

# # 원본 비교
with open('./_original_data/'+f'vehicle{test_user}_info.json', 'rb') as f:
    data = json.load(f)
    print('====== original data =======')
    pprint(data, width=100, indent=2)
'''
#===================================================================
#------------- mix data 직렬화&역직렬화(mixed data) 2 end -----------
#===================================================================

#===================================================================
#------------------------------ 성능평가 ---------------------------
#===================================================================


############################ 5 ############################
print('!!!', len(origin_v_list))
mal_user_id_5, mal_user_5,  mal_vehicle_num_5, mal_vehicle_5 = make_mal(origin_v_list, 5)
make_mixed_data(reporters, original_data, mal_user_5)
print('==================5==================')
print(' * mal_user_id =',mal_user_id_5)
print(' * mal_user =',mal_user_5)

target_5, find_num_5, find_5 = carTrust(mal_vehicle_num_5)
print(' * target_5 =', target_5)
print(' * find_num_5 =', find_num_5)
print('===> mal_vehicle_5 =', mal_vehicle_5)
print('===> find_5 =', find_5)
accuracy_5, precision_5, recall_5, f1_5 = make_performance(mal_vehicle_5, find_5)

############################ 10 ############################
mal_user_id_10, mal_user_10, mal_vehicle_num_10, mal_vehicle_10 = make_mal(origin_v_list, 10)
make_mixed_data(reporters, original_data, mal_user_10)
print('==================10==================')
print(' * mal_user_id =',mal_user_id_10)
print(' * mal_user =',mal_user_10)
# print('mal_vehicle_num_10 =',mal_vehicle_num_10)

target_10, find_num_10, find_10 = carTrust(mal_vehicle_num_10)
print(' * target_10 =', target_10)
print(' * find_num_10 =', find_num_10)
print('===> mal_vehicle_10 =',mal_vehicle_10)
print('===> find_10 =', find_10)
accuracy_10, precision_10, recall_10, f1_10 = make_performance(mal_vehicle_10, find_10)


############################ 15 ############################
mal_user_id_15, mal_user_15, mal_vehicle_num_15, mal_vehicle_15 = make_mal(origin_v_list, 15)
make_mixed_data(reporters, original_data, mal_user_15)
print('==================15==================')
print(' * mal_user_id =',mal_user_id_15)
print(' * mal_user =',mal_user_15)
# print('mal_vehicle_num_15 =',mal_vehicle_num_15)

target_15, find_num_15, find_15 = carTrust(mal_vehicle_num_15)
print(' * target_15 =', target_15)
print(' * find_num_15 =', find_num_15)
print('===> mal_vehicle_15 =',mal_vehicle_15)
print('===> find_15 =', find_15)
accuracy_15, precision_15, recall_15, f1_15 = make_performance(mal_vehicle_15, find_15)


############################ 20 ############################
mal_user_id_20, mal_user_20, mal_vehicle_num_20, mal_vehicle_20 = make_mal(origin_v_list, 20)
make_mixed_data(reporters, original_data, mal_user_20)
print('==================20==================')
print(' * mal_user_id =',mal_user_id_20)
print(' * mal_user =',mal_user_20)
# print('mal_vehicle_num_20 =',mal_vehicle_num_20)

target_20, find_num_20, find_20 = carTrust(mal_vehicle_num_20)
print(' * target_20 =', target_20)
print(' * find_num_20 =', find_num_20)
print('===> mal_vehicle_20 =',mal_vehicle_20)
print('===> find_20 =', find_20)
accuracy_20, precision_20, recall_20, f1_20 = make_performance(mal_vehicle_20, find_20)


mal_v_num = [5,10,15,20]
accuracy_list = [accuracy_5, accuracy_10, accuracy_15, accuracy_20]
precision_list = [precision_5, precision_10, precision_15, precision_20]
recall_list = [recall_5, recall_10, recall_15, recall_20]
f1_list = [f1_5, f1_10, f1_15, f1_20]

make_chart(mal_v_num, accuracy_list, precision_list, recall_list, f1_list)



ac, pr, re, f1 = make_performance_table(accuracy_list, precision_list, recall_list, f1_list)
print('accuracy_avg = ', ac)
print('precision_avg = ', pr)
print('recall_avg = ', re)
print('f1_score_avg = ', f1)

# make_chart_hist(mal_v_num, accuracy_list)
