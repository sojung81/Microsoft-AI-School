# 1~10까지의 합계 구하기
#hap = 0 #변수 선언
#for i in range(1, 11): #1~10까지 반복
#    hap += i #hap = hap + i
#print("합계:", hap) #합계 출력



#for i in range(1, 11):
#    if i % 2 == 0:
#        hap += i
#print("1~10까지의 짝수 합계:", hap) #1~10까지의 짝수 합계 출력



#for i in range (0,11,2):
#    hap += i
#print("1~10까지의 짝수 합계:", hap) #1~10까지의 짝수 합계 출력



#def myhap(max): #함수선언
#    hap = 0 #변수 선언
#    for i in range(1, max+1): #1~max까지 반복
#        hap += i #hap = hap + i
#    return hap #합계 반환

#hap = myhap(10) #함수 호출
#print("1~10까지의 합계:", hap) #합계 출력



#def myhap(max): #함수선언
#    hap = 0 #변수 선언
#    for i in range(1, max+1, 2): #1~max까지 반복
#        hap += i #hap = hap + i
#    return hap #합계 반환

#hap = myhap(100) #함수 호출
#print("1~100까지의 홀수 합계:", hap) #합계 출력



# #배열 - 리스트, 튜플
# array = [1, 2, 3, 4, 5] #리스트 선언
# print(array) #리스트 출력

# for value in array: #리스트 반복
#     print(value) #리스트 값 출력

# print(type(array)) #리스트 타입 출력

# array = (1, 2, 3, 4, 5) #튜플 선언
# print(array) #튜플 출력

# for value in array: #튜플 반복
#     print(value) #튜플 값 출력

# print(type(array)) #튜플 타입 출력

# array2 = [[1, 2, 3], [4, 5, 6]] #2차원 리스트 선언
# print(array2) #2차원 리스트 출력
# print(array2[0]) #2차원 리스트 값 출력
# print(array2[1]) #2차원 리스트 값 출력
# print(array2[0][0]) #2차원 리스트 값 출력
# print(array2[0][1]) #2차원 리스트 값 출력
# print(array2[0][2]) #2차원 리스트 값 출력
# print(array2[1][0]) #2차원 리스트 값 출력
# print(array2[1][1]) #2차원 리스트 값 출력
# print(array2[1][2]) #2차원 리스트 값 출력

# array2 = ((1, 2, 3), (4, 5, 6)) #2차원 튜플 선언
# print(array2) #2차원 튜플 출력

# print(array2[0]) #2차원 튜플 값 출력
# print(array2[1]) #2차원 튜플 값 출력
# print(array2[0][0]) #2차원 튜플 값 출력
# print(array2[0][1]) #2차원 튜플 값 출력
# print(array2[0][2]) #2차원 튜플 값 출력
# print(array2[1][0]) #2차원 튜플 값 출력
# print(array2[1][1]) #2차원 튜플 값 출력
# print(array2[1][2]) #2차원 튜플 값 출력




#딕셔너리 클래스 사용하기

# animal = {"TIGER": "호랑이", "DOG": "강아지", "CAT": "고양이"} #딕셔너리 선언
# print(animal) #딕셔너리 출력

# print(animal["TIGER"]) #딕셔너리 값 출력
# print(animal["DOG"]) #딕셔너리 값 출력
# print(animal["CAT"]) #딕셔너리 값 출력

# item = 'CAT' #변수 선언

# if item in animal: #딕셔너리 키 값 확인
#     print('CAT이 animal에 있습니다.') #딕셔너리 키 값이 있으면 출력

# item = 'FISH' #변수 선언

# if item not in animal: #딕셔너리 키 값 확인
#     print('FISH가 animal에 없습니다.') #딕셔너리 키 값이 없으면 출력



# # 삼각형 출력하기
# class Star:

#     def __init__(self, line): #생성자 선언
#         self._line = line

#     def set(self, line): #setter 선언
#         self._line = line

#     def get(self): #getter 선언
#         return self._line

#     def printStar(self): #별 출력 메소드 선언
#         for i in range(1, self._line + 1): #1~line까지 반복
#             for j in range(0, i): #0~i까지 반복
#                 print("*", end="") #별 출력
#             print("\n", end="") #줄바꿈

# star = Star(5) #객체 생성
# star.set(5) #setter 호출
# star.printStar() #별 출력 메소드 호출



#클래스 상속 구현
#부모클래스
class Animal:

    __legs = 4

    def __init__(self): #생성자 선언
        Animal.__legs = 4

    #걷는다.
    def walk(self):
        print("걷는다.")

    #달린다.
    def run(self):
        print("달린다.")

    #먹는다.
    def eat(self):
        print("먹는다.")

    #소리를 내다.
    def makeasound(self):
        print("소리를 내다.")

    #다리의 수
    def printLegs(self):
        print("다리의 수:", Animal.__legs)


# #자식클래스
# class Dog(Animal):
#     def play(self):
#         print("강아지가 놀고 있습니다.")

#     #소리를 내다.
#     def md(self):
#         print("멍멍akeasoun")

# class Cat(Animal):
#     def play(self):
#         print("고양이가 놀고 있습니다.")

#     #소리를 내다.
#     def makeasound(self):
#         print("야옹")

# class Pomeranian(Dog):
#     def play(self):
#         print("포메라니안이 놀고 있습니다.")

#     #소리를 내다.
#     def makeasound(self):
#         print("왈왈")

# animal = Animal() #부모클래스 객체 생성
# animal.walk() #부모클래스 메소드 호출
# animal.run() #부모클래스 메소드 호출
# animal.eat() #부모클래스 메소드 호출
# animal.makeasound() #부모클래스 메소드 호출
# animal.printLegs() #부모클래스 메소드 호출

# dog = Dog() #자식클래스 객체 생성
# dog.makeasound
# dog.play() #자식클래스 메소드 호출

# cat = Cat() #자식클래스 객체 생성
# cat.makeasound() #자식클래스 메소드 호출
# cat.play() #자식클래스 메소드 호출

# #pomeranian 객체를 생성
# pomeranian = Pomeranian() #자식클래스 객체 생성
# pomeranian.makeasound() #자식클래스 메소드 호출
# pomeranian.play() #자식클래스 메소드 호출