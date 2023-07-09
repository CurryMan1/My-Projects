num1 = 0
num2 = 0
while num1 <= 0 or num2 <= 0:
    print("Enter positive numbers!")
    num1 = int(input("Number 1:"))
    num2 = int(input("Number 2:"))
if num1 > num2:
    f = num1
else:
    f = num2

while f % num1 != 0 or f % num2 != 0:
        f+=1
print("LCM = " + str(f))


