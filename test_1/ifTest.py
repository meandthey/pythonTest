a = 100
b = 1

if a > b :
    print("a")
else : 
    print("b")

if a>b:
    print('a')
else:
    print('b')

for i in range(1, 6):
    print(i)

numbers = [3, 7, 12, 19, 21, 24]

for num in numbers:
    if num > 10:  # 10보다 큰 숫자만 출력
        print(num)

for i in range(1, 11):  # 1부터 10까지 반복
    if i % 2 == 0:  # 짝수인지 확인
        print(f"{i}는 짝수입니다.")
    else:  # 홀수일 경우
        print(f"{i}는 홀수입니다.")



for i in range(1, 11):  # 1부터 10까지 반복
    if i % 2 == 0:  # 짝수인지 확인
        print(f"{i}는 짝수입니다.")
    else:  # 올바른 들여쓰기
        print(f"{i}는 홀수입니다.")
