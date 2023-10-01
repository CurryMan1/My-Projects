class Player:
    position = 100, 100
    name = 'Hardhik'
    def __init__(self):
        self.position = 30, 30

p = Player()

print(p.position)
p.position = 10
print(p.position)