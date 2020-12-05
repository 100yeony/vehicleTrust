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
def make_vlist():
    files = os.listdir('./mixed_data')
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
            v1_social_temp['received_data'] = random.randint(1,10)
            v1_social_temp['not_used_data'] = random.randint(7,10)
            v1_social_temp['redistributed_data'] = random.randint(1,5)
        else:
            v1_social_temp['response'] = random.randint(1,10)
            v1_social_temp['received_data'] = random.randint(1,10)
            v1_social_temp['not_used_data'] = random.randint(1,3)
            v1_social_temp['redistributed_data'] = random.randint(1,10)

    for i in v2_social_temp:
        if v2_vid in mal_vehicle:
            v2_social_temp['response'] = random.randint(1,4)
            v2_social_temp['received_data'] = random.randint(1,10)
            v2_social_temp['not_used_data'] = random.randint(7,10)
            v2_social_temp['redistributed_data'] = random.randint(1,5)
        else:
            v2_social_temp['response'] = random.randint(1,10)
            v2_social_temp['received_data'] = random.randint(1,10)
            v2_social_temp['not_used_data'] = random.randint(1,3)
            v2_social_temp['redistributed_data'] = random.randint(1,10)
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
    for i in v1_temp[0]:
        gps = v1_temp[0]['GPS'].split(',')
        v1_x = round(float(gps[1]),5)
        v1_y = round(float(gps[0]),5)

    for i in v2_temp[0]:
        gps = v2_temp[0]['GPS'].split(',')
        v2_x = round(float(gps[1]),5)
        v2_y = round(float(gps[0]),5)
    # print('??',v1_x, v1_y, v2_x, v2_y)

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
    connectivity = round(math.exp(con),2)
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


def make_VT_algorithm(v) :
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

    GT = None
    if GT != None:
        RecentVT = (LT+a*GT)/2
    else:
        RecentVT = LT

    PVT = RecentVT
    VT = round(d*PVT+(1-d)*RecentVT,2)
    # print('VT:', VT)

    # # if cnt == 3:
    # #         break
    # cnt += 1
    # print('cnt', cnt)

    for key, info in v.items():
        for second_key in info:
            real_info = info['VTI']
            for third_key in real_info:
                real_info['VT'] = VT
    return v


def make_performance(target,find):
    target_set = set(target)
    find_set = set(find)

    accuracy = len(find_set.intersection(target_set)) / len(find_set)
    right = 3
    precision = 3
    recall = 3
    f1 = 3

    # accuracy = np.mean(np.equal(target,find))
    # right = np.sum(target * find == 1)
    # precision = right / np.sum(find)
    # recall = right / np.sum(target)
    # f1 = 2 * precision*recall/(precision+recall)
    print('==============================')
    print('accuracy :',accuracy)
    # print('precision :', precision)
    # print('recall :', recall)
    # print('f1 :', f1)
    print('==============================')

    return accuracy, precision, recall, f1


def carTrust(mal_vehicle):
    #### mixed data에서 모든 vehicle 정보를 불러옴 ####
    v_list = make_vlist()
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
            with open('./original_data/'+f'{v1_temp}', 'rb') as f:
                v1 = json.load(f)
            with open('./original_data/'+f'{v2_temp}', 'rb') as f:
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

        response=0
        received_data=0
        not_used_data=0
        redistributed_data=0
        v1_res, v1_received, v1_not_used, v1_redistributed = set_social_init(v1_social_temp, response, received_data, not_used_data, redistributed_data)
        v2_res, v2_received, v2_not_used, v2_redistributed = set_social_init(v2_social_temp, response, received_data, not_used_data, redistributed_data)

        make_social_info(v1, v1_res, v1_received, v1_not_used, v1_redistributed)
        make_social_info(v2, v2_res, v2_received, v2_not_used, v2_redistributed)

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

        v1 = make_VT_algorithm(v1)
        v2 = make_VT_algorithm(v2)
        # print('=============== make_VT_algorithm() ==============')
        # pprint(v1)
        # print('=========================================')
        # pprint(v2)
        # print('****************make_VT_algorithm()*************')

        final_vlist.append(v1)
        final_vlist.append(v2)
    #===================================================================
    #-------------------------- 직렬화&역직렬화 3 -------------------------
    #===================================================================
    for i in final_vlist:
        # print(i)
        name = ''
        for key, info in i.items():
            for second_key in info:
                name = info['user']
                # print(name)
        # << 직렬화 >>
        with open('./data/'+f'vehicle{name}_info.json', mode='w', encoding='UTF8') as f:
            json.dump(i, f, cls=CustomEncoder, indent=2)
            # print('직렬화 complete!!')
    # print('new 직렬화 complete!')
        # << 역직렬화 >>
        # with open('./data/'+f'vehicle{i}_info.json', 'rb') as f:
        #     data = json.load(f)
        #     print('역직렬화 complete!')
        #     pprint(data, width=100, indent=2)

    #===================================================================
    #--------------------------직렬화&역직렬화 3 end-----------------------
    #===================================================================

    #####################################모든 차량이 소셜행위를 수행###################################
    ############### VT알고리즘을 거친 차량 정보를 불러옴 #################
    files = os.listdir('./data')
    new_vlist = []
    for file in files:
        new_vlist.append(file)
    # print('new_vlist:', new_vlist)


    find_temp = []
    for i in new_vlist:
        with open('./data/'+f'{i}', 'rb') as f:
            v = json.load(f)
            VT = 0
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
    find = []
    for i in find_temp_cut:
        find.append(i[1])

    ##### target, find ######
    return sorted(mal_vehicle), sorted(find)


def RSU(v):
    #여러 차량의 VTI를 수집하고 기하평균? 가중평균

    return rti

def make_chart_4(mal_v_num, accuracy, precision, recall, f1):
    mal_v_num = mal_v_num   # x축 : list 길이 같아야
    accuracy = accuracy        # y축 : list 길이 같아야 함
    precision = precision
    recall = recall
    f1 = f1
    plt.plot(mal_v_num, accuracy, color='red', marker='*')
    plt.plot(mal_v_num, precision, color='green',  marker='o')
    plt.plot(mal_v_num, recall, color='blue',  marker='s')
    plt.plot(mal_v_num, f1, color='purple',  marker='s')
    plt.legend(['accuracy', 'precision', 'recall', 'f1'])
    plt.xlabel('number of malicious vehicle')
    plt.ylabel('performance')
    plt.title('Detection ratio by number of malicious vehicles')
    plt.show()

def make_chart_1(mal_v_num, accuracy):
    mal_v_num = mal_v_num   # x축 : list 길이 같아야
    accuracy = accuracy        # y축 : list 길이 같아야 함
    plt.plot(mal_v_num, accuracy, color='red', marker='*')
    plt.legend(['accuracy'])
    plt.xlabel('number of malicious vehicle')
    plt.ylabel('performance')
    plt.title('Detection ratio by number of malicious vehicles')
    plt.show()
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
# print('reporters', reporters)

# # #-----------------------find_malicious_vehicle-----------------
# number = set()
# while len(number)<5:
#     number.add(random.randint(1,56))
# mal_test = list(number)
# # mal_test: [5, 40, 15, 53, 31]
# print('mal_test:', mal_test)
# # #---------------------find_malicious_vehicle end-----------------
################### set original_data ###############################
# for i in reporters:
#     vehicle = Vehicle(f'{reporters.index(i)+1}', i)
#
#     created_data = []
#     for c in original_data:
#         if i == c[10]:
#             if c[15] != '':
#                 data = {'contents':c[14], 'score':0,'createdTime':(c[2],c[3]),'GPS':c[15], 'vid':f'{reporters.index(i)+1}'}
#                 created_data.append(data)
#
#             vehicle.update_VDI({'createdData':created_data,'receivedData':{'contents':[], 'score':0,'createdTime':0}})
#
#             social_info = {'response':0, 'received_data':0, 'not_used_data':0, 'redistributed_data':0}
#             social_activity = {'info':social_info,'scoring':0, 'ignoring':0, 'sharing':0}
#
#             vehicle.update_social(social_activity)
#===================================================================
#-------------------------- 직렬화&역직렬화 1 -------------------------
#===================================================================
    # # << 직렬화 >>
    # with open('./original_data/'+f'vehicle{i}_info.json', mode='w', encoding='UTF8') as f:
    #     json.dump(vehicle, f, cls=CustomEncoder, indent=2)
        # print('complete!!')

    # # << 역직렬화 >>
    # with open('./original_data/'+f'vehicle{i}_info.json', 'rb') as f:
    #     data = json.load(f)
    #     print(type(data))
    #     pprint(data, width=100, indent=2)

#===================================================================
#--------------------------직렬화&역직렬화 1 end-----------------------
#===================================================================


#===================================================================
#-------------------------- mixed data 직렬화&역직렬화 2 -------------------------
#===================================================================
v_list_ = []
# # << original data 역직렬화 >>
for i in reporters:
    with open('./original_data/'+f'vehicle{i}_info.json', 'rb') as f:
        data = json.load(f)
        v_list_.append(data)
        # pprint(data, width=100, indent=2)


number = set()
################### mal_vehicle cnt ####################
while len(number)<10:
    number.add(random.randint(1,len(v_list_)))
########################################################
#************** FIX HERE !!! ****************
mal_vehicle = list(number)
# print('mal_vehicle : ', mal_vehicle)
#********************************************

mal_user_id = []
mal_user = []
for i in v_list_ :
    # print("i??:", i)
    for key,info in i.items():
        for second_key in info:
            if int(info['vid']) in mal_vehicle:
                mal_user_id.append((info['vid'],info['user']))

#************** FIX HERE !!! ****************
mal_user_id = set(mal_user_id)
mal_user_id = [(x[0],x[1]) for x in sorted(mal_user_id, key = lambda x:x[0])] # vid로 정렬
for i in mal_user_id:
    mal_user.append(i[1])
# mal_user_id= [('4', '전인조'), ('44', '김선경'), ('9', '박평운')]
# mal_user= ['김선경', '박평운', '전인조']

#********************************************
mal_user_id = [('10', '정훈'), ('23', '정장균'), ('31', '김현덕'), ('33', '백한석'), ('34', '김남수'), ('36', '최유상'), ('53', '임종철'), ('54', '전인조'), ('58', '윤병춘'), ('9', '주영철')]
mal_user = ['정훈', '정장균', '김현덕', '백한석', '김남수', '최유상', '임종철', '전인조', '윤병춘', '주영철']
mal_vehicle = [9, 10, 23, 31, 33, 34, 36, 53, 54, 58]




'''
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
'''
################## mix data 직렬화 #######################
    # with open('./mixed_data/'+f'vehicle{i}_info.json', mode='w', encoding='UTF8') as f:
    #     json.dump(vehicle, f, cls=CustomEncoder, indent=2)
    #     # print('complete!!')

################## mix data 역직렬화 #####################
# with open('./mixed_data/'+f'vehicle이승만_info.json', 'rb') as f:
#     data = json.load(f)
#     print(type(data))
#     pprint(data, width=100, indent=2)

print('mal_user_id =',mal_user_id)
print('mal_user =',mal_user)
print('mal_vehicle =',sorted(mal_vehicle))

# target, find = carTrust(mal_vehicle)
# print('target =', target)
# print('find =', find)

target10 = [9, 10, 23, 31, 33, 34, 36, 53, 54, 58]
find10 = [6, 7, 9, 12, 16, 21, 24, 34, 52, 56]
#===================================================================
#------------------- mix data 직렬화&역직렬화 2 end -----------------
#===================================================================
# accuracy, precision, recall, f1 = make_performance(target5, find5)
accuracy, precision, recall, f1 = make_performance(target10, find10)
# accuracy, precision, recall, f1 = make_performance(target15, find15)
# accuracy, precision, recall, f1 = make_performance(target20, find20)

# a5,p5,r5,f5 = carTrust(5)
# a10,p10,r10,f10 = carTrust(10)
# a15,p15,r15,f15 = carTrust(15)
# a20,p20,r20,f20 = carTrust(20)

mal_v_num = [5,10,15,20]
# accuracy = [a5, a10, a15, a20]
# precision = [p5, p10, p15, p20]
# recall = [r5, r10, r15, r20]
# f1 = [f5, f10, f15, f20]

# accuracy = [3,4,5,6]
# precision = [2,6,7,8]
# recall = [13,22,51,43]
# f1 = [3,44,33,1]

# make_chart_4(mal_v_num, accuracy, precision, recall, f1)
# make_chart_1(mal_v_num, accuracy)
