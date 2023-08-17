from datetime import date

daysoftheweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

y = int(input("What year were you born in? (YYYY)"))
m = int(input("What month were you born in? (MM)"))
d = int(input("What day of that month were you born in? (DD)"))

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
def find_birthweekday(born):
    print(str(date.today() - born).split(maxsplit = 1))
    diff = int(str(date.today() - born).split(maxsplit = 1)[0])+1
    print(diff)
    diff = (diff % 7)
    print(diff)
    return daysoftheweek[(diff)]

print(f'You are {str(calculate_age(date(y, m, d)))} years old.')
print(f'You were born on a {daysoftheweek[date(y, m, d).weekday()]}.')
print(f'You were born on a {find_birthweekday(date(y, m, d))}.')