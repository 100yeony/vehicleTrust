import math
# import random
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale
# import make_RTI
from make_VDI_VTI_RTI import RTI, VTI, VDI
import make_data


'''
# car position(차량 위치정보) : car id, car position
# created data(생성한 데이터) : car id, data content, creation time, data type
# received data(수집한 데이터) : car id, data content, creation time, data type, data score, scored time, scored car id, total score, number of scored car
# car trust(차량 신뢰도) : car id, car trust, recent car trust, past car trust, local trust, global trust, network trust, user reputation, connectivity

VDI : 차량이 생성한 데이터, 차량이 수집한 다른 차량의 데이터, 데이터 신뢰도, 데이터 생성 시간, 차량 식별자, 데이터 내용(하루가 지난 데이터는 삭제)
VTI : 데이터 신뢰성, 활동점수, 네트워크 신뢰도, 사용자 평판, 연결성, 차량 신뢰도 갱신 시간, 과거 차량 신뢰도
RTI : 차량 식별자, 차량 신뢰도, 차량 위치정보, 차량 신뢰도 갱신 시간 (가중평균처리)


data에 들어갈 내용 : 날짜, 위치(위도, 경도), 내용

# 3234 row, 22 col
원본data.csv : 발생년,발생년월일시,주야,요일,사망자수,부상자수,중상자수,경상자수,부상신고자수,발생지시도,발생지시군구,사고유형_대분류,사고유형_중분류,
사고유형,가해자법규위반,도로형태_대분류,도로형태,가해자_당사자종별,피해자_당사자종별,발생위치X_UTMK,발생위치Y_UTMK,경도,위도

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

<문법>
행 출력 : origin_data[1]
값 접근 : origin_data[1][1]
리스트 행 슬라이싱 : origin_data[0:3] 시작이나 끝 인덱스를 생략할수있음, 인덱스에서 -1은 맨 마지막 데이터의 앞쪽
리스트에 값 추가 : origin_data.append('청주')
리스트 특정 위치에 값 추가 : origin_data.insert(3, '부산') 4번째 위치에 값 추가
리스트 길이 : len(origin_data)

<고려사항>
1. 차량 몇대로 설정할지 -> 일단 10대.. 이 중 malicious 2대
2. 데이터 랜덤하게 생성?
3. scoring 어떻게?



1. data(o)
2. packet
3. social activity
4. RSU / VDI / VTI (o)
5. 성능평가 차트

'''




def make_packet(origin_packet):
    #packet에 들어가는거 찾아보기 !!...

    # v1_packet=''
    # v2_packet=''
    # v3_packet=''

    v1_packet={'vid':1, 'packet':'?'}

    return print(v1_packet)



# def make_DR_AS(SC, IG, SH) :
#     AS = GS + S
#     # sum함수가 적용되려면  iterable 해야함 : list, tuple
#     # sum([1,2,3,4,5])
#     #DR = 1/I + sum(Datascore*creationTime)/n
#     DR = 1/I + sum(list(Datascore*creationTime))/length(list(Datascore*creationTime))
#     return AS, DR

def social_activities(vehicle_data):
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


    return print('SC:', SC, '\nIG:', IG, '\nSH:', SH)








def dissemination_RSU():
    #일단은 랜덤함수 쓰고
    #VDI랑 VTI를 구현해서 RTI를 만들기
    #그 값을 계속 변형할 수 있도록 main을 짜기. 알고리즘에 따라
    # VDI - VTI - VT - RTI



    return RTI





###############################  main start ####################################
v1_info=''
v2_info=''
v3_info=''

data = make_data.make_data()

origin_data = data.csv2list()
# origin_packet=''
# print(origin_data)

vehicle_data = data.make_Vdata_list(v1_info, v2_info, v3_info)
# malicious_vehicle(origin_data)
# social_activities(vehicle_data)


#RTI에는 RSU의 모든 데이터가 반영되어 있어야 함. 현재로서는 3대의 차량 정보를 수집했다고 가정
#메인에서 데이터와 데이터 생성 지역 및 시간을 다르게 설정해서 malicious하다고 판단
# RTI: vid, VT, v_position, VT_updateTime
# VDI: vid, VT, data, creationTime, received_data
# VTI: vid, VT, DR, AS, NT, UR, connectivity, VT_updateTime, PVT

rti = RTI()
rti.setData(1, 2, '충북청주', '201108-22:37')
rti.printData()


vdi1 = VDI()
vdi1.setData(2, 5, 'data', '201108-22:37', 'data1')
vdi1.printData()

vti1 = VTI()
vti1.setData(2, 5, 4, 3, 5, 10, 30,'201108-22:37', 1)
vti1.printData()

# vehicle_packet = make_packet(origin_packet)
#
# social_in_vehicle = social_activities(vehicle_data, vehicle_packet)
#
#
# rsu = dissemination_RSU(social_in_vehicle)

###############################  main end  #####################################
