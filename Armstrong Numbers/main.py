num = str(input("Enter a number"))
sum = 0

for i in range(len(num)):
    sum += int(num[i]) ** len(num)

if sum == int(num):
    print("The number IS an armstrong number")
else:
    print("The number ISN'T an armstrong number")