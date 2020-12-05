import json
import pickle
import pprint




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
        print('\n', 'vehicle 객체를 새로 만들었어요~', '\n')


# import bookstore
v1 = RTI()
v1.setData(1, 2, '충북청주', '201108-22:37')
v1.printData()

#메인에서 데이터와 데이터 생성 지역 및 시간을 다르게 설정해서 malicious하다고 판단

v2 = RTI()
v2.setData(2, 4, '충북천안', '201108-22:37')
v2.printData()




# class Object:
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__,
#             sort_keys=True, indent=4)
#
# # me = Object()
# # me.name = "Onur"
# # me.age = 35
# # me.dog = Object()
# # me.dog.name = "Apollo"
#
# me = Object()
# me.v1 = Object()
# me.v1.vid = 1
# me.v1.VT = 10
# me.v1.v_position = '충북청주'
#
# v2 = Object()
# v2.v2 = Object()
# v2.v2.vid = 1
# v2.v2.VT = 10
# # v2.v2.v_position = '충북청주'
#
# print(me.toJSON())
# print(v2.toJSON())
#
# class RTI:
#     def __init__(self, vid, VT):
#         self.vid = vid,
#         self.VT = VT
#
# test = RTI(2, 3)
#
#
# with open('test.data', 'wb') as f:
#     pickle.dump(test, f)
#
#
# # 역직렬화 (Deserialization)
# with open('test.data', 'rb') as f:
#     r = pickle.load(f)
# #
# print(r)
# print("%d x %d" % (r.vid, r.VT))

#
# class Rectangle:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.area = width * height
#
#
# rect = Rectangle(10, 20)
#
# # 사각형 rect 객체를 직렬화 (Serialization)
# with open('rect.data', 'wb') as f:
#     pickle.dump(rect, f)
#
#
# # 역직렬화 (Deserialization)
# with open('rect.data', 'rb') as f:
#     r = pickle.load(f)
#
# print("%d x %d" % (r.width, r.height))


# a = dict({'vid':1, 'VT':3})
# print(type(a),a)
