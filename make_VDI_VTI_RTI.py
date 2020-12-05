import pprint
from collections import OrderedDict

'''
VDI : 차량이 생성한 데이터, 차량이 수집한 다른 차량의 데이터, 데이터 신뢰도, 데이터 생성 시간, 차량 식별자, 데이터 내용(하루가 지난 데이터는 삭제)
VTI : 데이터 신뢰성, 활동점수, 네트워크 신뢰도, 사용자 평판, 연결성, 차량 신뢰도 갱신 시간, 과거 차량 신뢰도
RTI : 차량 식별자, 차량 신뢰도, 차량 위치정보, 차량 신뢰도 갱신 시간 (가중평균처리)


일단 딕셔너리로 만들기, 그 안에 리스트 넣기
'''

class RTI:
    def setData(self, vid, VT, v_position, VT_updateTime):
        self.vid = vid
        self.VT = VT
        self.v_position = v_position
        self.VT_updateTime = VT_updateTime

    def printData(self):
        test=dict({
            'vid':self.vid,
            'VT':self.VT,
            'v_position':self.v_position,
            'VT_updateTime':self.VT_updateTime
            })
        pprint.pprint(test, width=20, indent=2)

    def __init__(self):
        print('\n', 'RTI 객체')

    def make_Vposition(origin_data):
        # original_data의 위치부분 가져오는 코드 짜기 : 21:경도(ㅇ) 22:위도(ㅇ)
        # 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])
        # origin_data
        Vposition = [origin_data[1][21], original_data[1][22]]
        return print('Vposition : ', Vposition)
        # Vposition = []
        # for i in origin_data :
        #     Vposition.append(origin_data[i][1]+'에 '+origin_data[i][9]+' '+origin_data[i][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])



class VDI:
    def setData(self, vid, VT, data, creationTime, received_data):
        self.vid = vid
        self.VT = VT
        self.data = data
        self.creationTime = creationTime
        self.received_data = received_data

    def printData(self):
        test=dict({
            'vid':self.vid,
            'VT':self.VT,
            'data':self.data,
            'creationTime':self.creationTime,
            'received_data':self.received_data
            })
        pprint.pprint(test, width=20, indent=2)

    def __init__(self):
        print('\n', 'VDI 객체')



class VTI:
    def setData(self, vid, VT, DR, AS, NT, UR, connectivity, VT_updateTime, PVT):
        self.vid = vid
        self.VT = VT
        self.DR = DR
        self.AS = AS
        self.NT = NT
        self.UR = UR
        self.connectivity = connectivity
        self.VT_updateTime = VT_updateTime
        self.PVT = PVT

    def printData(self):
        test=OrderedDict({
            'vid':self.vid,
            'VT':self.VT,
            'DR':self.DR,
            'AS':self.AS,
            'NT':self.NT,
            'UR':self.UR,
            'connectivity':self.connectivity,
            'VT_updateTime':self.VT_updateTime,
            'PVT':self.PVT
            })
        pprint.pprint(test, width=100, indent=2)

    def __init__(self):
        print('\n', 'VTI 객체')
