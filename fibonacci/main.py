length = int(input("How long should the sequence be?"))
t1 = 0
t2 = 1
nextTerm = 0

for i in range(length):
    print(nextTerm)
    t1 = t2
    t2 = nextTerm
    nextTerm = t1 + t2