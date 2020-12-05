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
0:﻿발생년
1:발생년월일시(ㅇ)
2:주야
3:요일
4:사망자수
5:부상자수
6:중상자수
7:경상자수
8:부상신고자수
9:발생지시도(ㅇ)
10:발생지시군구(ㅇ)
11:사고유형_대분류
12:사고유형_중분류
13:사고유형
14:가해자법규위반(ㅇ)
15:도로형태_대분류
16:도로형태
17:가해자_당사자종별
18:피해자_당사자종별
19:발생위치X_UTMK
20:발생위치Y_UTMK
21:경도(ㅇ)
22:위도(ㅇ)
'''

'''
[성능평가 step1]
VT를 구하는 함수에 따라 차량 별 VT를 구함.
차량 10대의 VT를 구하고
임계치에 따라 malicious하다고 분류하고 그 중 malicious가 얼마나 나타났는지 정답 셋과 결과 셋을 비교함.

이거를 네트워크만/소셜만/네트워크&소셜 3가지로 VT를 산출하는 알고리즘을 돌림.
각각 malicious 탐지율을 수치화하고 차트로 생성.

[성능평가 step2]
precision정확도, recall재현율, F-measure
가중치를 달리 주면서 자체 성능평가 a=0.1일때, a=0.2일때 등.
--------------------------------------------------------------------------------------------------
성능평가 4가지 표 나오기.

1. 기존 기법과의 비교
1.1. 차량 간 네트워크 패킷 교환만 이루어지는 경우
1.2. 차량 간 소셜 행위만 이루어지는 경우
1.3. 차량 간 패킷 교환과 소셜 행위가 모두 이루어지는 경우

2. 악의적인 차량 탐지
거짓된 정보를 생성하는 악의적인 차량을 몇 개 만들어놓고 알고리즘에 따라 차량 신뢰도가 낮게 계산되는지 확인
--------------------------------------------------------------------------------------------------
2가지 차트 만들기
1.
x축 : 차량 수
y축 : 정확도
꺾은선 그래프 3개(네트워크&소셜, 소셜, 네트워크)
설명 : 평균적인 VT 비교???

2.
x축 : 차량 수
y축 : 악의적인 차량 탐지율
꺾은선 그래프 3개(네트워크&소셜, 소셜, 네트워크)
설명 : 악의적인 데이터를 생성하는 차량 3대,4대, 5대를 설정해놓고
몇대를 탐지하는지 탐지율을 찾기

'''

def csv2list() :
    lists = []
    # file = open('도로교통공단_교통사고 정보_20200714.csv', 'r', encoding='UTF8')
    file = open('event_08.csv', 'r', encoding='UTF8')
    while True :
        line = file.readline().rstrip("\n")
        if line :
            line = line.split(",")
            lists.append(line)
        else :
            break
    return lists

'''
THIS WORK IS MAKING ARTIFICIAL DATA
'''
def make_random_Vdata(origin_data):
    landom_num = [random.randint(1,3234) for i in range(3)]
    for i in landom_num :
        idx = i
        Vdata_list = list()
        Vdata_list.append(origin_data[i][1]+'에 '+origin_data[i][9]+' '+origin_data[i][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])
    return Vdata_list, idx


def make_malicious_Vdata(origin_data, idx):
    # landom_num = [random.randint(1,3234) for i in range(3)]
    # for i in landom_num :
    #     Vdata_list = list()
    #     Vmal_data_list = list()
    #     j = i+1
    #     k = j+1
    #     Vdata_list.append(origin_data[i][1]+'에 '+origin_data[i][9]+' '+origin_data[i][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])
    #     Vmal_data_list.append(origin_data[i][1]+'에 '+origin_data[j][9]+' '+origin_data[k][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])

    landom_num = [random.randint(1,3234) for i in range(3)]
    for i in landom_num :
        Vdata_list = list()
        Vmal_data_list = list()
        j = idx+1
        k = idx+1
        Vdata_list.append(origin_data[idx][1]+'에 '+origin_data[idx][9]+' '+origin_data[idx][10]+'에서 '+origin_data[idx][14]+' 사고발생. 위치는 경도 '+origin_data[idx][21]+', 위도 '+origin_data[idx][22])
        Vmal_data_list.append(origin_data[i][1]+'에 '+origin_data[j][9]+' '+origin_data[k][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])

    # print('True data ===>', Vdata_list,'\n', 'False data ===>', Vmal_data_list )
    return 'true', Vdata_list, 'false', Vmal_data_list








def make_packet(origin_packet):
    #packet에 들어가는거 찾아보기 !!...

    # v1_packet=''
    # v2_packet=''
    # v3_packet=''

    v1_packet={'vid':1, 'packet':'?'}
    return print(v1_packet)





def dissemination_RSU(v_info):
    #일단은 랜덤함수 쓰고
    #VDI랑 VTI를 구현해서 RTI를 만들기
    #그 값을 계속 변형할 수 있도록 main을 짜기. 알고리즘에 따라
    # VDI - VTI - VT - RTI

    vid = v_info['RTI'][0]['vid']
    VT = v_info['RTI'][0]['VT']
    position = v_info['RTI'][0]['position']
    update_time = v_info['RTI'][0]['updateTime']

    temp_dict = {'vid':vid, 'VT':VT, 'position':position, 'updateTime':update_time}
    v_info['RTI'].append(temp_dict)
    return v_info



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


def make_VT_algorithm(v_info) :
    UR = v_info['VTI']['UR']
    NT = v_info['VTI']['NT']
    cnt=0

    while cnt<10:
        LT = (UR*NT)**(1/2)
        # print('LT,',LT)

        temp_arr = []
        for i in range(0,len(v_info['RTI'])):
            temp = v_info['RTI'][i]
            temp_arr.append(temp['VT'])
        # print('=====temp_arr:', temp_arr)

        mul = 1
        for item in temp_arr:
            mul = mul*item
        GT = mul ** (1/len(temp_arr))
        # print("기하 평균 =", GT)
        if GT is None:
            RecentVT = (LT+a*GT)/2
        else:
            RecentVT = LT

        PVT = RecentVT
        d = 0.4
        VT = d*PVT+(1-d)*RecentVT

        # if cnt == 3:
        #         break
        cnt += 1
        # print('cnt', cnt)
    return round(VT,2)


def accuracy():
    accuracy = []
    return accuracy

def find_malicious_vehicle():
    #100대 중 malicious 5대를 설정 -> vid를 체크해야 함. 랜덤으로 부여 ->  malicious_vlist를 생성
    #algorithm을 수행한 후 VTI에 기록된 vt를 체크함. 100대의 vt를 sort 한 뒤 낮은 순으로 5대를 필터링하여 find_malicious_list를 만듦
    #malicious_vlist와 find_malicious_list를 비교하여 정답셋과 일치하는 find가 몇 개인지 정확도를 판단

    accuracy = 0

    return accuracy






def make_chart():
    num_vehicle = [1, 2, 3, 4, 5, 6]
    net_and_social = [12, 12, 10, 14, 22, 24]
    net = [14, 15, 15, 22, 21, 12]
    social = [24, 4, 15, 13, 2, 21]
    plt.plot(num_vehicle, net_and_social, color='red', marker='*')
    plt.plot(num_vehicle, net, color='green',  marker='o')
    plt.plot(num_vehicle, social, color='blue',  marker='s')
    plt.legend(['network&social', 'network', 'social'])
    plt.xlabel('number of malicious vehicle')
    plt.ylabel('detection ratio')
    plt.title('Detection ratio by number of malicious vehicles')
    plt.show()

    chart = 0
    return chart

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

# http://hyeonjae-blog.logdown.com/posts/776615-python-getitem-len
def social_activities(v_info):
    v_info = pickle.loads(v_info)
    print('===============>in social:', v_info, type(v_info))
    print(v_info.social_activities)
    num_response = random.randint(1,30)
    num_received_data = random.randint(1,30)
    num_not_used_data = random.randint(1,30)
    num_redistributed_data = random.randint(1,30)
    social_info = [('response:', num_response), ('received data:',num_received_data), ('not used data:', num_not_used_data), ('redistributed data:',num_redistributed_data)]
    # print('===> response:', num_response, 'received data:',num_received_data, 'not used data:', num_not_used_data, 'redistributed data:',num_redistributed_data)
    # v_info['social_activities']['info'] = social_info
    # v_info['social_activities']['scoring'] = round(num_response/num_received_data,2)
    # v_info['social_activities']['ignoring'] = round(num_not_used_data/num_received_data,2)
    # v_info['social_activities']['sharing'] = round(num_redistributed_data/num_received_data,2)


    # v_info.social_activities['info'] = social_info
    temp1 = v_info.social_activities
    print(temp1, type(temp1))
    temp1['info'] = social_info
    # v_info['social_activities']['scoring'] = round(num_response/num_received_data,2)
    # v_info['social_activities']['ignoring'] = round(num_not_used_data/num_received_data,2)
    # v_info['social_activities']['sharing'] = round(num_redistributed_data/num_received_data,2)
    return v_info


class CustomEncoder(json.JSONEncoder):
     def default(self, o):
         if isinstance(o, datetime):
             return {'__datetime__': o.replace(microsecond=0).isoformat()}
         return {'__{}__'.format(o.__class__.__name__): o.__dict__}
###############################  main start ####################################
#VT 알고리즘에 넣고 계속 돌아가는 프로그램을 생성 .. VT는 계속 갱신됨.. 결과 파일을 어케 만들지는 생각해보기
#RTI에는 RSU의 모든 데이터가 반영되어 있어야 함. 현재로서는 10대의 차량 정보를 수집했다고 가정
#메인에서 데이터와 데이터 생성 지역 및 시간을 다르게 설정해서 malicious하다고 판단
# 시간을 가짜로 생성하는데 사고 발생 시간+랜덤으로 생성???
#아니면 시간에 따라서 비슷한 날짜일 때 비슷한 시간대로?

# vehicle_info : vid, VDI, VTI, RTI
# VDI: (createdData,score,createdTime), (receivedData, score, receivedTime)
# VTI: VT, DR, AS, NT, UR, connectivity, VT_updateTime, PVT
# RTI: VT, v_position, VT_updateTime

# VDI : 차량이 생성한 데이터, 차량이 수집한 다른 차량의 데이터, 데이터 신뢰도, 데이터 생성 시간, 차량 식별자, 데이터 내용(하루가 지난 데이터는 삭제)
# VTI : 데이터 신뢰성, 활동점수, 네트워크 신뢰도, 사용자 평판, 연결성, 차량 신뢰도 갱신 시간, 과거 차량 신뢰도
# RTI : 차량 식별자, 차량 신뢰도, 차량 위치정보, 차량 신뢰도 갱신 시간 (가중평균처리)

# data에 들어갈 내용 : 날짜, 위치(위도, 경도), 내용

original_data = csv2list()
print(original_data)
'''
mal_vehicle = [7,8]
total_vehicle = 10
#랜덤 초이스 함수 써서 mal_vehicle을 리스트로 생성할 것. 그리고 해당 리스트를 반복하면서 값을 가짜로 넣어줄 것.
find_mal_vehicle = []

for i in range(1, total_vehicle+1) :
    vehicle = Vehicle(f'{i}')
    if i in mal_vehicle:
        print('+-----------------------------------------------+')
        print('          ',f'malicious vehicle {i} info', '                ')
        print('+-----------------------------------------------+')
    else:
        print('+-----------------------------------------------+')
        print('                ',f'vehicle {i} info', '                ')
        print('+-----------------------------------------------+')

    Vdata, idx = make_random_Vdata(original_data)
    maldata = make_malicious_Vdata(original_data, idx)
    # maldata = json.dumps(maldata.__dict__)

    if i in mal_vehicle:
        vehicle.update_VDI({'createdData':{'contents':[maldata], 'score':0,'createdTime':0},'receivedData':{'contents':[], 'score':0,'createdTime':0}})

    elif i == 9:
        #social 행위 하는 함수 호출하고 리턴 값을 받기?!
        vehicle.update_social({'info':{},'scoring':0, 'ignoring':0, 'sharing':3})
        vehicle.update_VDI({'createdData':{'contents':[Vdata], 'score':0,'createdTime':0},'receivedData':{'contents':[], 'score':0,'createdTime':0}})
        vehicle.update_VTI({'DR':3,'AS':0,'NT':0,'UR':0, 'VT':0, 'connectivity':0, 'CF':0,'VT_updateTime':0, 'PVT':0})

    elif i == 10:
        # dissemination_RSU 함수 호출하고 리턴 값을 받기?!
        vehicle.update_VDI({'createdData':{'contents':[Vdata], 'score':0,'createdTime':0},'receivedData':{'contents':[], 'score':0,'createdTime':0}})
        vehicle.update_VTI({'DR':3,'AS':0,'NT':0,'UR':0, 'VT':0, 'connectivity':0, 'CF':0,'VT_updateTime':0, 'PVT':0})
        vehicle.put_RTI({'vid':1, 'VT':1,'position':[], 'updateTime':0})
        vehicle.put_RTI({'vid':2, 'VT':2,'position':[], 'updateTime':0})

    else:
        vehicle.update_VDI({'createdData':{'contents':[Vdata], 'score':0,'createdTime':0},'receivedData':{'contents':[], 'score':0,'createdTime':0}})
        vehicle.update_VTI({'DR':3,'AS':0,'NT':0,'UR':0, 'VT':0, 'connectivity':0, 'CF':0,'VT_updateTime':0, 'PVT':0})



    vehicle.printVehicle()

    with open('./data/'+f'vehicle{i}_info.json', mode='w', encoding='UTF8') as f:
        json.dump(vehicle, f, cls=CustomEncoder, indent=2)
        print('complete!!')

    with open('./data/'+f'vehicle{i}_info.json', 'rb') as f:
        data = json.load(f)
        print(data)
        #dict 접근하는 함수
        # print(data.vid)

v1 = ''

with open('./data/vehicle1_info.json', 'rb') as f:
    v1 = json.load(f)
    print(v1)
    #dict 접근하는 함수
print('v1===>', v1)
'''
    #VDI랑 VTI를 바꾸는 함수 change_VDI, change_VTI 에서 나온 결과를 update_VDI, update_VTI로 전달해주면 될듯?
    #글로벌하게 객체 만들고 바꾸고싶은데..for문 안에서 말고.. 이렇게 하면 모든 차량이 항상 같은 값을 갖게 됨
    #차량 간에 독립적으로 굴러가는 환경 만들기


    # v1 = json.dumps(vehicle.__dict__)
    # v1 = json.dumps(vehicle, indent=4)
    # print('v1====>', v1)
    # temp = pickle.dumps(social_activities(v1))
    # print('???????', pickle.loads(temp))

    # v1 = pickle.dumps(vehicle, protocol=3)
    # print('v1====>', v1)
    # temp = pickle.dumps(social_activities(v1))
    # print('???????', pickle.loads(temp))



    # vehicle = change_VDI(temp, Vdata)
    # print('is it changed received data?')
    # vehicle = change_VDI_receivedData(temp, Vdata)
    # print(vehicle)
    #
    # # vehicle1 = change_VTI(vehicle)
    # vehicle2 = change_RTI(vehicle, original_data)
    # vehicle_rsu = dissemination_RSU(vehicle2)
    # # print('====>', vehicle_rsu)
    # vt = make_VT_algorithm(vehicle_rsu)
    # # print('vt=======>', vt)
    # vehicle_algorithm = change_VTI(vehicle, vt)
    # # pprint(OrderedDict(vehicle_algorithm), width=150, indent=1)
    # # # -------------------------------------------------------------



# for i in range(1,11) :
#     vehicle_info = {
#     'vid':f'{i}',
#     'social_activities':{'info':{},'scoring':0, 'ignoring':0, 'sharing':0},
#     'VDI':{
#         'createdData':{'contents':[], 'score':0,'createdTime':0},
#         'receivedData':{'contents':[], 'score':0,'createdTime':0}},
#     'VTI':{'DR':0,'AS':0,'NT':0,'UR':0, 'VT':0, 'connectivity':0, 'CF':0,'VT_updateTime':0, 'PVT':0},
#     'RTI':[{'vid':0, 'VT':0,'position':[], 'updateTime':0}]}
#
#     Vdata, idx = make_random_Vdata(original_data)
#     # Vdata2, idx = make_random_Vdata(original_data)
#     # Vdata = ''
#     if(i == 4):
#         Vdata = make_malicious_Vdata(original_data, idx)
#     # print(Vdata)
#     temp = social_activities(vehicle_info)
#     vehicle = change_VDI(temp, Vdata)
#     print('is it changed received data?')
#     vehicle = change_VDI_receivedData(temp, Vdata)
#     print(vehicle)
#
#     # vehicle1 = change_VTI(vehicle)
#     vehicle2 = change_RTI(vehicle, original_data)
#     vehicle_rsu = dissemination_RSU(vehicle2)
#     # print('====>', vehicle_rsu)
#     vt = make_VT_algorithm(vehicle_rsu)
#     # print('vt=======>', vt)
#     vehicle_algorithm = change_VTI(vehicle, vt)
#     # pprint(OrderedDict(vehicle_algorithm), width=150, indent=1)
