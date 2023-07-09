a = ""
p = str(input("enter a phrase"))
for i in range(len(p)):
    a += p[-(i+1)]
print(a)