import random
from src.constants import OPTIONS


class ResultsGenerator:
    def __init__(self, answers, guesses):
        self.answers = answers
        self.guesses = guesses

        self.results = {}

    def generate(self):
        for i in range(self.answers):
            self.results[i+1] = []
            for j in range(self.guesses):
                self.results[i+1].append(random.choice(OPTIONS))
        #print(self.results)

    def get(self):
        return self.results
