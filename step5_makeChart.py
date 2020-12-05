from matplotlib import pyplot as plt

# plt.plot([1,2,3], [1,4,9])
# plt.plot([2,3,4],[5,6,7])
# plt.xlabel('Sequence')
# plt.ylabel('Time(secs)')
# plt.title('Experiment Result')
# plt.legend(['Mouse', 'Cat'])
# plt.show()
#
#
#
# y = [5, 3, 7, 10, 9, 5, 3.5, 8]
# x = range(len(y))
# plt.bar(x, y, width=0.7, color="blue")
# plt.show()

'''
# Dashed:
plt.plot(x_values, y_values, linestyle='--')
# Dotted:
plt.plot(x_values, y_values, linestyle=':')
# No line:
plt.plot(x_values, y_values, linestyle='')


# A circle:
plt.plot(x_values, y_values, marker='o')
# A square:
plt.plot(x_values, y_values, marker='s')
# A star:
plt.plot(x_values, y_values, marker='*')
'''

num_vehicle = [1, 2, 3, 4, 5, 6]
net_and_social = [12, 12, 10, 14, 22, 24]
net = [14, 15, 15, 22, 21, 12]
social = [24, 4, 15, 13, 2, 21]
plt.plot(num_vehicle, net_and_social, color='red', marker='*')
plt.plot(num_vehicle, net, color='green',  marker='o')
plt.plot(num_vehicle, social, color='blue',  marker='s')
plt.legend(['network&social', 'network', 'social'])
plt.xlabel('number of vehicle')
plt.ylabel('accuracy ratio')
plt.title('Accuracy ratio by number of vehicles')
plt.show()



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


'''
1. 데이터 전처리가 문제지..


2. 성능평가 step1까지 나오면 SUMO로 돌려보기





[성능평가 step1]
VT를 구하는 함수에 따라 차량 별 VT를 구함.
차량 10대의 VT를 구하고
임계치에 따라 malicious하다고 분류하고 그 중 malicious가 얼마나 나타났는지 정답 셋과 결과 셋을 비교함.

이거를 네트워크만/소셜만/네트워크&소셜 3가지로 VT를 산출하는 알고리즘을 돌림.
각각 malicious 탐지율을 수치화하고 차트로 생성.


[성능평가 step2]
precision정확도, recall재현율, F-measure
가중치를 달리 주면서 자체 성능평가 a=0.1일때, a=0.2일때 등.



성능평가 4가지 표 나오기.

1. 기존 기법과의 비교
1.1. 차량 간 네트워크 패킷 교환만 이루어지는 경우
1.2. 차량 간 소셜 행위만 이루어지는 경우
1.3. 차량 간 패킷 교환과 소셜 행위가 모두 이루어지는 경우

2. 악의적인 차량 탐지
거짓된 정보를 생성하는 악의적인 차량을 몇 개 만들어놓고 알고리즘에 따라 차량 신뢰도가 낮게 계산되는지 확인




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
