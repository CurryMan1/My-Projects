a = input("enter first number:")
b = input("enter second number:")
def swap_val(x, y):
    x = [x, y]
    y = x[0]
    x = x[1]
    print(x, y)
swap_val(a,b)