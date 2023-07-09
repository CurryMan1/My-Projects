num1 = int(input("Number 1:"))
num2 = int(input("Number 2:"))
hcf = 0

if num1 > num2:
    for i in range(num2):
        if num1 % (i+1) == 0 and num2 % (i+1) == 0:
            hcf = i+1
if num2 > num1:
    for i in range(num1):
        if num1 % (i+1) == 0 and num2 % (i+1) == 0:
            hcf = i+1
print("the highest common factor is " + str(hcf))