'''
oasis 크롤링 코드 개발
수동으로 논문 다운받는 순서 기록

논문검색 - '기본검색'에서 키워드를 하나씩 입력 - '전체 다운로드' - 제목 또는 발행년도,페이지 묶은 key로 <csv 중복제거?? - glob 모듈> - 논문키워드분석 - KCD8, MeSH, KCD

(감기|급성코카타르|Nasalcatarrh,acute|감염성비인두염NOS|InfectivenasopharyngitisNOS|비인두염NOS|NasopharyngitisNOS|급성비염|Acuterhinitis|감염성비염|Infectiverhinitis)


광동탕



("급성 비인두염[감기]"|"Acute nasopharyngitis[common cold]"|코감기(급성)|"Coryza (acute)"|"급성 코카타르"|"Nasal catarrh, acute"|"감염성 비인두염 NOS"|"Infective nasopharyngitis NOS"|"비인두염 NOS"|"Nasopharyngitis NOS"|"급성 비염"|"Acute rhinitis"|"감염성 비염"|"Infective rhinitis")


감기|"급성 비인두염[감기]"|Acute nasopharyngitis[common cold]|코감기(급성)|Coryza (acute)|"급성 코카타르"|Nasal catarrh, acute|"감염성 비인두염 NOS"|Infective nasopharyngitis NOS|"비인두염 NOS"|Nasopharyngitis NOS|"급성 비염"|Acute rhinitis|"감염성 비염"|Infective rhinitis

(감기|"급성 비인두염[감기]")
'''
## parser.py
import requests
from bs4 import BeautifulSoup
import json
import os

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('https://beomi.github.io/beomi.github.io_old/')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
my_titles = soup.select(
    'h3 > a'
    )

data = {}

for title in my_titles:
    data[title.text] = title.get('href')

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)
