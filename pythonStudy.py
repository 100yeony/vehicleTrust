a,b,c,d = 0,0,0,0
hap=0

a = int(input("1: "))
b = int(input("2: "))
c = int(input("3: "))
d = int(input("4: "))

hap = a+b+c+d
print("합 ==> %d" %hap)


aa = [0,0,0,0]
hap=0

aa[0] = int(input("1: "))
aa[1] = int(input("2: "))
aa[2] = int(input("3: "))
aa[3] = int(input("4: "))
hap=aa[0]+aa[1]+aa[2]+aa[3]
print("합==> %d" %hap)

aa = []
aa.append(0)
print(aa)

for i in range(0,100):
    aa.append(0)
len(aa)



aa=[]
for i in range(0,4):
    aa.append(0)
hap=0

for i in range(0,4):
    aa[i] = int(input(str(i+1)+"번째 숫자:"))
    hap=hap+aa[i]

# hap=aa[0]+aa[1]+aa[2]+aa[3]

print("합계==>%d" %hap)


aa=[]
bb=[]
value = 0

for i in range(0, 100) :
    aa.append(value)
    value+=2

for i in range(0, 100):
    bb.append(aa[99-i])

print("bb[0]에는 %d이, bb[99]에는 %d이 입력됩니다."%(bb[0], bb[99]))


aa=[10, 20, 30, 40]
#리스트 인덱스 뒤에서부터 접근할 땐 맨 끝이 -1이고 앞으로 갈수록 -2, -3 등
print("aa[-1]은 %d, aa[-2]는 %d" %(aa[-1], aa[-2]))aa[0:3]

aa=[10, 20, 30, 40]
#print함수를 안써도 값이 리스트로 출력됨
aa[0:3]
aa[2:4]

# :은 끝까지 또는 처음부터 라는 의미
aa[2:]
aa[:2]

aa[10, 20, 30]
bb[40, 50, 60]
#길이가 같은 리스트끼리 연산이 가능함
aa+bb
aa*3

#리스트 항목을 건너뛰며 추출
aa = [10, 20, 30, 40, 50, 60, 70]
aa[::2] #2번째 위치 생략
aa[::-2] #역순으로 두칸 간격으로 출력
aa[::-1] # -1이 붙으면 역순으로 1칸 간격으로 출력

arr[a:b:c] #arr 리스트의 a부터 b까지 c의 간격으로 출력

aa[-1] #리스트의 마지막 값
aa=[10,20,30]
aa[1:2]=[200, 201] #리스트의 두번째 값인 20을 2개의 값으로 변경

del a[1] #del함수를 이용해 a리스트의 2번째 값 삭제
del(a[1])

a=[1,2,3]
a.index(3) #a리스트에 3이라는 값이 있으면 해당 위치의 인덱스 반환


aa=[10, 20, 30, 40, 50]
aa[1:4] = [] #인덱스 1번부터 3번까지의 값을 삭제

#리스트 삭제
aa=[10, 20, 30] ; aa=[]; aa #빈 리스트 출력됨
aa=[10, 20, 30] ; aa=None; aa #아무것도 안나옴
aa=[10, 20, 30] ; del(aa); aa #오류

리스트.pop() #리스트에서 해당 항목이 삭제됨 / 맨 뒤의 항목을 빼냄
리스트.insert() #지정된 위치에 값 삽입
리스트.extend() #리스트에 리스트를 추가
리스트.count() #리스트에서 해당 값의 개수를 셈
리스트.clear() #리스트의 내용을 모두 지움
새 리스트=리스트명.copy() #리스트의 내용을 복사
새리스트=sorted(리스트) #리스트의 값을 정렬해서 새로운 리스트에 대입
리스트.sort() #리스트의 값 정렬

print(%d, 100)
print(%5d, 100) #5자리로 숫자를 출력함 : 앞이 공백으로 채워짐
print(%f, 0.1)
print(%c, 'a') #char : %c
print(%s, 'ab') #string : %s




var1 = var2 = var3 = var4 = 100 #4개의 변수에 100을 대입

a, b= 9,2
print(a**b, a%b, a//b) # **는 제곱, %는 나머지, //는 나눈 후 소수점 아래 제거

a = (100==100) #True가 저장됨
b = (10>100) #False가 저장됨
print(a, b) #bool 형태로 저장

a = "이건 큰따옴표 \" 모양" #문자열 내에서는 특수문자 앞에 역슬래쉬 붙여주면 됨



def myFunc():
    print('함수 호출')

globalVar = 100

if __name__ == '__main__':
    print('메인 함수 실행')
    myFunc()
    print('전역 변수 값:', globalVar)


a = 5/3 #나누기
a = 5//3 #나누고 소수점 버림
a = 5%3 #나누고 나머지 값
a = 5**3 #제곱


s1, s2, s3 = "100", "100.123", "9999999999999999"
print(int(s1)+1, float(s2)+1, int(s3)+1) #숫자가 문자열 상태이면 int()나 float()으로 감싸줌

a=100; b=100.123
str(a)+'1'; str(b)+'1' #숫자를 문자열로 변환할 땐 str()함수를 사용. 문자열끼리 연결이라 101이 아니라 1001이 됨

#파이썬에는 ++이나 --의 증가,감소 연산자가 없음
a+=3 # a=a+3



#연산자를 활용한 동전 교환 프로그램
money, c500, c100, c50, c10 = 0, 0, 0, 0, 0
money = int(input("교환할 돈은 얼마?"))
c500 = money
money%=500

c100 = money
money%=100

c50 = money
money%=50

c10 = money
money%=10

print("\n 500원짜리 ==> %d개" % c500)
print("100원짜리 ==> %d개" % c100)
print("50원짜리 ==> %d개" % c50)
print("10원짜리 ==> %d개" % c10)
print("바꾸지 못한 잔돈 ==> %d원 \n" % money)


a = 99
(a>100)and(a<200)
(a>100)or(a<200)
not(a==100)

if(1234): print("참이면 보여요") #0이외의 숫자는 True

if(0): print("거짓이면 안보여요") #0은 False를 나타냄


import turtle
import random

swidth, sheight, pSize, exitCount = 300, 300, 3, 0
r, g, b, angle, dist, curX, curY = [0]*7 #모든 변수가 [0,0,0,0,0,0,0]로 초기화

turtle.title('거북이가 맘대로 다니기')
turtle.shape('turtle')
turtle.pensize(pSize)
turtle.setup(width=swidth+30, height=sheight+30)
turtle.screensize(swidth, sheight)

while True:
    r = random.random()
    g = random.random()
    b = random.random()
    turtle.pencolor((r,g,b))

    angle = random.randrange(0, 360) #0부터 360의 범위에서 임의 추출
    dist = random.randrange(1,100)
    turtle.left(angle) #각도 설정
    turtle.forward(dist) #거리만큼 이동
    curX = turtle.xcor() #현재 위치 구하는 함수
    curY = turtle.ycor()

    if(-swidth/2 <= curX and curX <= swidth/2) and (-sheight/2 <= curY and curY <= sheight/2): #거북이의 현재 위치가 화면 안인지 체크. 터틀 그래픽 좌표는 중앙이 (0,0)
        pass #if문 조건에 해당되면 그냥 종료하고 다시 while문 수행
    else:
        turtle.penup()
        turtle.goto(0,0)
        turtle.pendown()

        exitCount+=1
        if exitCount>=5:
            break #5회 이상 밖으로 나갔다면 while문을 빠져나간 후 프로그램 종료

turtle.done()


'''
파이썬에서는 들여쓰기가 매우 중요함.
if문 다음에 실행할 문장은 들여쓰기를 해야 하는데 이때, Tab보다 space bar을 4칸 정도 눌러서 하는 것을 권장.
대화형 모드에서는 실행할 문장이 모두 끝나고 enter를 2번 눌러야 if문이 끝나는 것으로 간주
'''

score=int(input("점수를 입력하세요:"))

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")

print("학점입니다.")


jumsu=55
res=''
if jumsu >= 60:
    res="합격"
else:
    res="불합격"
print(res)

res = '합격' if jumsu>=60 else '불합격'


import turtle

swidth, sheight = 500, 500

turtle.turtle('무지개색 원그리기')
turtle.shape('turtle')
turtle.setup(width=swidth+50, height=sheight+50)
turtle.screensize(swidth, sheight)
turtle.penup()
turtle.goto(0, -sheight/2)
turtle.pendown()
turtle.speed(10)

for radius in range(1, 250):
    if radius % 6 == 0:
        turtle.pencolor('red')
    elif radius % 5 == 0:
        turtle.pencolor('orange')
    elif radius % 4 == 0:
        turtle.pencolor('yellow')
    elif radius % 3 == 0:
        turtle.pencolor('green')
    elif radius % 2 == 0:
        turtle.pencolor('blue')
    elif radius % 1 == 0:
        turtle.pencolor('navyblue')
    else :
        turtle.pencolor('purple')

    turtle.circle(radius)

turtle.done()


fruit=['사과', '귤', '복숭아', '딸기']
fruit.append('귤')

if '딸기' in fruit:
    print("딸기가 있네요~^^")


import random

numbers=[]
for num in range(0,10):
    numbers.append(random.randrange(0,10))

print('생성된 리스트', numbers)

for num in range(0,10):
    if num not in numbers:
        print('숫자 %d는(은) 리스트에 없네요.' %num)



#기능이 2가지인 종합 계산기
select, answer, numStr, num1, num2 = 0,0,"",0,0

select = int(input("1. 입력한 수식 계산 2.두 수 사이의 합계: "))

if select == 1:
    numStr = input(' ***수식을 입력하세요: ')
    answer = eval(numStr) #사용자가 입력한 수식을 계산해주는 eval()함수
    print("%s 결과는 %5.1f입니다." %(numStr, answer))
elif select ==2:
    num1 = input(' *** 첫 번째 숫자를 입력하세요: ')
    num2 = input(' *** 두 번째 숫자를 입력하세요: ')
    for i in range(num1, num2+1):
        answer=answer+i
    print("%d+...+%d는 %d입니다." %(num1, num2, answer))
else:
    print("1또는 2만 입력해야 합니다.")





for i in range(0,3,1): #0,1,2까지 i가 돌면서 프린트문을 3번 출력하게 됨
    print('안녕하세요? for문 공부 중 입니다.')

for i in range(0,3,1):
    print("%d : 안녕하세요? for문 공부 중 입니다." %i)

#i를 사용하지 않으려면 언더바 사용함
for _ in range(0,3,1):
    print("안녕하세요? for문 공부 중 입니다.")

for i in range(2, -1, -1):
    print("%d : 안녕하세요? for문 공부 중 입니다." %i) #2부터 -1까지 역순으로 2,1,0까지 세번 출력


for i in range(1,6,1):
    print("%d " %i, end=" ") #1부터 5까지 하나씩 증가하면서 출력하고 마지막은 공백


i, hap = 0,0
for i in range(1,11,1):
    hap=hap+i
print("1부터 10까지 합계: %d" %hap)


for i in range(501, 1001, 2):
    hap=hap+i
print("500과 1000사이에 있는 홀수의 합계: %d" %hap)


i,hap=0,0
num=0

num=int(input("값을 입력하세요: "))

for i in range(1, num+1, 1):
    hap=hap+i

print("1에서 %d까지의 합계: %d" %(num, hap))


i,dan=0,0
dan=int(input("단을 입력하세요: "))

for i in range(1,10,1):
    print("%d X %d = %2d" %(dan, i, dan*i))



for i in range(0,3,1): #i가 0,1,2이고
    for k in range(0,2,1): #k는 0,1
        print("파이썬은 꿀잼.(i값: %d, k값: %d)" %(i,k))


#중첩 for문을 이용하여 구구단 만들기
i,k=0,0
for i in range(2,10,1):
    for k in range(1,10,1):
        print("%d X %d = %2d" %(i,k,i*k))
    print("") #각 단이 끝나면 한 줄 띄움


'''
while문을 빠져나가려면 break를 사용함.
continue는 무조건 끝으로 간 뒤 반복문으로 다시 돌아감.

'''
