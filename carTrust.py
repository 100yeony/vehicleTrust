# import pandas as pd
# csv_test = pd.read_csv('도로교통공단_교통사고 정보_20200714.csv')
# # print(csv_test)
# for line in csv_test:
#     print(line)
#
# import csv
# import pandas as pd
#
#
# with open('도로교통공단_교통사고 정보_20200714.csv', 'r') as f:
#     reader = csv.reader(f)
#     data = list(reader)
# # print(data)

import math
from sklearn.preprocessing import minmax_scale
import pandas as pd
import numpy as np


def csv2list(filename) :
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

temp = csv2list("도로교통공단_교통사고 정보_20200714.csv")
print(temp)

# print(temp[1])
#행 출력 : temp[1]
#값 접근 : temp[1][1]
#리스트 행 슬라이싱 : temp[0:3] 시작이나 끝 인덱스를 생략할수있음, 인덱스에서 -1은 맨 마지막 데이터의 앞쪽
#리스트에 값 추가 : temp.append('청주')
#리스트 특정 위치에 값 추가 : temp.insert(3, '부산') 4번째 위치에 값 추가
#리스트 길이 : len(temp)


#수식 구현
# 파라미터 만드는 함수 만들기 여러개 테이블별로?
# car position(차량 위치정보) : car id, car position
# created data(생성한 데이터) : car id, data content, creation time, data type
# received data(수집한 데이터) : car id, data content, creation time, data type, data score, scored time, scored car id, total score, number of scored car
# car trust(차량 신뢰도) : car id, car trust, recent car trust, past car trust, local trust, global trust, network trust, user reputation, connectivity

def carPosition(temp) :
    # 각각의 변수의 자료구조 타입을 고민해보기!
    # print(temp)
    # temp의 열 개수를 먼저 가져오고 -> 굳이?
    # 차량은 10대만 !
    carId = ['c1', 'c2', 'c3']
    # print(len(temp))
    # for i in temp:
        # carPosition = [temp[i][21], temp[i][22]]

    # temp = list(range(10))
    # temp='c'+range(i)

    # for num in temp:
    #     carId.append('c')
    #     # carId = carId[num]
    #     # temp2 = carId.join(num)
    # print(carId)


    # for문을 돌면서 c뒤에 숫자 붙여주기!!!


    return print(carId, carPosition)

carPosition(temp[1])

# def createdData(temp) :
#     car
#
#
# def receivedData(temp) :
#
#
# def carTrust(temp) :
#

DR=0
AS=0

def make_DR_AS(DR, AS) :
    GS = # of Response / # of ReceivedData
    I = # of not used data / # of received data
    S = # of redistribution data / # of received data
    AS = GS + S
    # sum함수가 적용되려면  iterable 해야함 : list, tuple
    # sum([1,2,3,4,5])
    #DR = 1/I + sum(Datascore*creationTime)/n
    DR = 1/I + sum(list(Datascore*creationTime))/length(list(Datascore*creationTime))
    return DR, AS


def make_UR(DR, AS) :
    #사용자 평판 관련

    # 정규화를 하려면 그 전에 전처리를 해줘서 모양을 만들어야 함.
    UR = Norm(DR+AS)

    temp = array(DR+AS)
    temp_minmax_scaled = minmax_scale(temp, axis=0, copy=True)
    UR = temp_minmax_scaled

    return UR

def make_NT(AS) :
    #네트워크 신뢰성 관련
    con = math.exp(-distanceij)
    CF  = # of packets forwarded / avg number of packets observed at neighbors
    NT = AS*con*CF?
    return UR, NT






df = pd.DataFrame({'grp_col' : ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b'],
                   'val' : np.arange(10)+1,
                   'weight' : [0.0, 0.1, 0.2, 0.3, 0.4, 0.0, 0.1, 0.2, 0.3, 0.4]})
df


# group weighted average by category
grouped = df.groupby('grp_col')
weighted_avg_func = lambda g:np.average(g['val'], weights=g['weight'])
grouped.apply(weighted_avg_func)

grp_col
a    4.0
b    9.0
dtype: float64


# split
df_a = df[df['grp_col']=='a']
df_b = df[df['grp_col']=='b']


# apply
weighted_avg_a = sum((df_a['val']*df_a['weight']))/sum(df_a['weight'])
weighted_avg_b = sum((df_b['val']*df_b['weight']))/sum(df_b['weight'])


# combine
weighted_avg_ab = pd.DataFrame({'grp_col': ['a', 'b'],
                               'weighted_average': [weighted_avg_a, weighted_avg_b]})

weighted_avg_ab





def main() :
    PCT = 0
    CT = 0
    make_DR_AS(DR, AS)
    make_UR(DR, AS)
    make_NT(AS)
    while
        LT = UR*NT
        LT = (UR*NT)**(1/2)

        # 기하 평균을 구하는 방법 1
        ar = [1, 5, 9]
        mul = 1
        for item in ar:
            mul = mul*item
        GM = mul ** (1/len(ar))
        print("기하 평균 =", GM)


        GT

        if GT is !null
            RecentCT = (LT+a*GT)/2
        else
            RecentCT = LT

        PCT = RecentCT
        d = 0.4
        CT = d*PCT+(1-d)*RecentCT
    return CT





# origin_data = open('도로교통공단_교통사고 정보_20200714.csv', 'r')
# data_reader = csv.reader(origin_data)
# for line in data_reader:
    # print(line)

#일단 데이터셋을 어떤 자료구조에 넣어야 함
#데이터셋의 인자에 접근하는 코드 찾기
# 내 수식 만들기 위해 파라미터 생성(함수, 클래스)
#랜덤하게 값을 생성하는 코드 찾기
# origin_list = []
# for i in data_reader:
#     # print(i)
#     origin_list.append(i)
# origin_list.seek(0,0)
# origin_list
