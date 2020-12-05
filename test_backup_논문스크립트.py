import random
from pprint import pprint
from collections import OrderedDict
import time
from scipy.linalg import norm
import math

'''
VDI : 차량이 생성한 데이터, 차량이 수집한 다른 차량의 데이터, 데이터 신뢰도, 데이터 생성 시간, 차량 식별자, 데이터 내용(하루가 지난 데이터는 삭제)
VTI : 데이터 신뢰성, 활동점수, 네트워크 신뢰도, 사용자 평판, 연결성, 차량 신뢰도 갱신 시간, 과거 차량 신뢰도
RTI : 차량 식별자, 차량 신뢰도, 차량 위치정보, 차량 신뢰도 갱신 시간 (가중평균처리)

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

def csv2list() :
    lists = []
    file = open('도로교통공단_교통사고 정보_20200714.csv', 'r', encoding='UTF8')
    while True :
        line = file.readline().rstrip("\n")
        if line :
            line = line.split(",")
            lists.append(line)
        else :
            break
    return lists



def make_random_Vdata(origin_data):
    landom_num = [random.randint(1,3234) for i in range(3)]
    for i in landom_num :
        Vdata_list = list()
        Vdata_list.append(origin_data[i][1]+'에 '+origin_data[i][9]+' '+origin_data[i][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])

    return Vdata_list



def make_malicious_Vdata(origin_data):
    landom_num = [random.randint(1,3234) for i in range(3)]
    for i in landom_num :
        Vdata_list = list()
        Vmal_data_list = list()
        j = i+1
        k = j+1
        Vdata_list.append(origin_data[i][1]+'에 '+origin_data[i][9]+' '+origin_data[i][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])
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





def social_activities(v_info):
    # 전역변수로 vinfo를 선언하고 data는 make data함수에서 채우고, datascore는 social activity함수에서 채우기?

    ######### fix data score !!


    SC=0
    IG=0
    SH=0

    #graph??? edge관계를 만들어야하나....어렵네...스트림처리해야하나?

    #v1 info를 가지고 scoring을 변경해주기!

    num_response = 10
    num_received_data = 5
    num_not_used_data = 2
    num_redistributed_data = 1

    SC = num_response/num_received_data
    IG = num_not_used_data/num_received_data
    SH = num_redistributed_data/num_received_data

    temp = vehicle_data[0]
    print(temp['dataScore'])


    return v_info



# def make_DR_AS(SC, IG, SH) :
#     AS = GS + S
#     # sum함수가 적용되려면  iterable 해야함 : list, tuple
#     # sum([1,2,3,4,5])
#     #DR = 1/I + sum(Datascore*creationTime)/n
#     DR = 1/I + sum(list(Datascore*creationTime))/length(list(Datascore*creationTime))
#     return AS, DR




def dissemination_RSU():
    #일단은 랜덤함수 쓰고
    #VDI랑 VTI를 구현해서 RTI를 만들기
    #그 값을 계속 변형할 수 있도록 main을 짜기. 알고리즘에 따라
    # VDI - VTI - VT - RTI



    return RTI



def change_VDI(v_info, data):
    time_ = time.asctime(time.localtime(time.time()))
    v_info['VDI']['createdData']['contents'] = data
    v_info['VDI']['createdData']['createdTime'] = time_
    v_info['VDI']['receivedData']['contents'] = data
    v_info['VDI']['receivedData']['createdTime'] = time_
    return v_info

def change_VTI(v_info):

    if v_info['vid'] != '4' :
        DR = v_info['VDI']['createdData']['score']
    else:
        DR = 0
    AS = 4
    UR = norm(DR+AS)

    CF = 3 # CF  = # of packets forwarded / avg number of packets observed at neighbors
    distanceij = 10
    connectivity = math.exp(-distanceij)
    NT = AS*connectivity*CF

    VT = 7
    VT_updateTime = 0
    PVT = 0

    v_info['VTI']['DR'] = DR
    v_info['VTI']['AS'] = AS
    v_info['VTI']['NT'] = NT
    v_info['VTI']['UR'] = UR
    v_info['VTI']['VT'] = VT
    v_info['VTI']['connectivity'] = connectivity
    v_info['VTI']['VT_updateTime'] = VT_updateTime
    v_info['VTI']['PVT'] = PVT
    return v_info



def change_RTI(v_info, data):
    # original_data의 위치부분 가져오는 코드 짜기 : 21:경도(ㅇ) 22:위도(ㅇ)
    landom_num = [random.randint(1,3234) for i in range(2)]
    position = []
    for i in landom_num:
        position = [data[i][21], data[i][22]]
    v_info['RTI']['position'] = position
    v_info['RTI']['updateTime'] = position
    v_info['RTI']['VT'] = v_info['VTI']['VT']
    return v_info






def make_VT_algorithm(v_info) :
    UR = v_info['VTI']['UR']
    NT = v_info['VTI']['NT']
    cnt=0
    while cnt<10:
        LT = (UR*NT)**(1/2)
        # print('LT,',LT)
        # 기하 평균을 구하는 방법 1
        ar = [1, 5, 9]
        mul = 1
        for item in ar:
            mul = mul*item
        GM = mul ** (1/len(ar))
        # print("기하 평균 =", GM)

        GT = 2

        if GT is None:
            RecentVT = (LT+a*GT)/2
        else:
            RecentVT = LT

        PVT = RecentVT
        d = 0.4
        VT = d*PVT+(1-d)*RecentVT
        v_info['VTI']['VT'] = VT


        # if cnt == 3:
        #         break
        cnt += 1
        # print('cnt', cnt)
    return v_info
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


# car position(차량 위치정보) : car id, car position
# created data(생성한 데이터) : car id, data content, creation time, data type
# received data(수집한 데이터) : car id, data content, creation time, data type, data score, scored time, scored car id, total score, number of scored car
# car trust(차량 신뢰도) : car id, car trust, recent car trust, past car trust, local trust, global trust, network trust, user reputation, connectivity

# VDI : 차량이 생성한 데이터, 차량이 수집한 다른 차량의 데이터, 데이터 신뢰도, 데이터 생성 시간, 차량 식별자, 데이터 내용(하루가 지난 데이터는 삭제)
# VTI : 데이터 신뢰성, 활동점수, 네트워크 신뢰도, 사용자 평판, 연결성, 차량 신뢰도 갱신 시간, 과거 차량 신뢰도
# RTI : 차량 식별자, 차량 신뢰도, 차량 위치정보, 차량 신뢰도 갱신 시간 (가중평균처리)
#
#
# data에 들어갈 내용 : 날짜, 위치(위도, 경도), 내용

original_data = csv2list()

for i in range(1,11) :
    vehicle_info = {
    'vid':f'{i}',
    'VDI':{
        'createdData':{'contents':[], 'score':0,'createdTime':0},
        'receivedData':{'contents':[], 'score':0,'createdTime':0}},
    'VTI':{'DR':0,'AS':0,'NT':0,'UR':0, 'VT':0, 'connectivity':0, 'VT_updateTime':0, 'PVT':0},
    'RTI':{'position':0, 'updateTime':0, 'VT':0}}

    Vdata = make_random_Vdata(original_data)
    if(i == 4):
        Vdata = make_malicious_Vdata(original_data)

    vehicle = change_VDI(vehicle_info, Vdata)
    vehicle1 = change_VTI(vehicle)
    vehicle2 = change_RTI(vehicle1, original_data)
    vt = make_VT_algorithm(vehicle2)
    pprint(OrderedDict(vt), width=150, indent=1)
