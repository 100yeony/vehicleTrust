import pandas as pd
import geopandas as gpd  # Import geopandas
import fiona #공간데이터를 딕셔너리 형태 등으로 접근할 수 있는 라이브러리
# import warnings
# warnings.filterwarnings(action='ignore') #경고 메시지 무시
# from IPython.display import display #print가 아닌 display()로 연속 출력
# from IPython.display import HTML #출력 결과를 HTML로 생성
# CCTV CSV 로딩
df_cctv = pd.read_xlsx('./1.xlsx', encoding="EUC-KR"    )
df_cctv.head()



def RSU(longitude, latitude, v1, v2):
    #여러 차량의 VTI를 수집하고 기하평균? 가중평균
    '''
    RSU는 input으로 들어오는 v의 모든 정보를 append하여 저장시키고
    GPS 데이터를 2차원 형태로 그려서 클러스터링 해야 함
    그리고 클러스터링 별로 전역 신뢰도 값을 주어야 함
    '''

    # latitude = [] #위도(뒤)
    # longitude = [] #경도(앞)

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

    try:
        for i in v1_temp[0]:
            gps = v1_temp[0]['GPS'].split(',')
            latitude.append(float(gps[1]))
            longitude.append(float(gps[0]))

        for i in v2_temp[0]:
            gps = v2_temp[0]['GPS'].split(',')
            latitude.append(float(gps[1]))
            longitude.append(float(gps[0]))
    except:
            print('error')


    return longitude, latitude


# long, lat = set(longitude), set(latitude)
#
# long_min, long_max = min(long), max(long)
# lat_min, lat_max = min(lat), max(lat)
#
# print(long_min, long_max)
# print(lat_min, lat_max)
