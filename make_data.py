import random

class make_data:
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

    def setData(self, origin_data, vid, data, dataScore):
        self.origin_data = origin_data
        self.vid = vid
        self.data = data
        self.dataScore = dataScore


    def make_Vdata_list(self):
        Vdata_list = list()
        landom_num = [random.randint(1,3234) for i in range(3)]
        for i in landom_num :
            Vdata_list.append(origin_data[i][1]+'에 '+origin_data[i][9]+' '+origin_data[i][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])
        # print(Vdata_list)
        v_info = dict({
            'vid':self.vid,
            'data':self.data,
            'dataScore':self.dataScore
        })
        # v1_info = {'vid':1, 'data':Vdata_list[0], 'dataScore':10}
        # v2_info = {'vid':2, 'data':Vdata_list[1], 'dataScore':20}
        # v3_info = {'vid':3, 'data':Vdata_list[2], 'dataScore':30}
        # return print(v1_info,'\n', v2_info,'\n', v3_info), v1_info, v2_info, v3_info
        return v_info, print(v_info)



    def malicious_vehicle(origin_data):
        Vdata_list = list()
        Vmal_data_list = list()
        landom_num = [random.randint(1,3234) for i in range(3)]
        for i in landom_num :
            j = i+1
            k = j+1
            Vdata_list.append(origin_data[i][1]+'에 '+origin_data[i][9]+' '+origin_data[i][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])
            Vmal_data_list.append(origin_data[i][1]+'에 '+origin_data[j][9]+' '+origin_data[k][10]+'에서 '+origin_data[i][14]+' 사고발생. 위치는 경도 '+origin_data[i][21]+', 위도 '+origin_data[i][22])
        # print('True data ===>', Vdata_list,'\n', 'False data ===>', Vmal_data_list )

        mal_vinfo = {'vid':4, 'data':Vmal_data_list[0], 'dataScore':0}
        return print(mal_vinfo)
