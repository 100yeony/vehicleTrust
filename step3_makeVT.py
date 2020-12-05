# UR = 4
# NT = 2

def make_VT(UR, NT) :
    cnt=0
    while cnt<10:
        LT = (UR*NT)**(1/2)
        print('LT,',LT)
        # 기하 평균을 구하는 방법 1
        ar = [1, 5, 9]
        mul = 1
        for item in ar:
            mul = mul*item
        GM = mul ** (1/len(ar))
        print("기하 평균 =", GM)

        GT = 2

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
        print('cnt', cnt)
    return VT, print(' ******** VT is', VT, '********')



# make_VT(UR,NT)
