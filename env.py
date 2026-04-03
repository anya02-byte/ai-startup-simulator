import random

class StartupEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.money = 100
        self.product = 0
        self.team = 1
        return (self.money, self.product, self.team)

    def step(self, action):
        reward = 0

        if action == "hire":
            self.team += 1
            self.money -= 10
            reward = 5

        elif action == "develop":
            self.product += 1
            self.money -= 15
            reward = 10

        elif action == "marketing":
            self.money += 20
            reward = 8

        elif action == "save":
            self.money += 5
            reward = 2

        elif action == "loan":
            self.money += 30
            reward = -5

        done = False
        if self.money <= 0:
            done = True

        return (self.money, self.product, self.team), reward, done
