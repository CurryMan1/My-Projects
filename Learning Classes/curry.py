class LotteryBall:
    def __init__(self, red_balls, blue_balls, green_balls):
        self.red_balls = red_balls
        self.blue_balls = blue_balls
        self.green_balls = green_balls
        self.total_balls = red_balls + blue_balls + green_balls

    def probability(self, ball_colour):
        mylist = ['red', 'blue', 'green']
        if ball_colour.lower() not in mylist:
            raise AttributeError(f"'{ball_colour}' isn't a ball colour.")
        elif ball_colour.lower() == 'red':
            return self.red_balls/self.total_balls
        elif ball_colour.lower() == 'blue':
            return self.blue_balls/self.total_balls
        else:
            return self.green_balls/self.total_balls
ball = LotteryBall(red_balls=0, blue_balls=24, green_balls=76)
print(ball.probability('blue'))