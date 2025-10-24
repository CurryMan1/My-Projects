import random
from src.constants import OPTIONS


class ResultsGenerator:
    def __init__(self, questions, answers):
        self.questions = questions
        self.answers = answers

        self.results = []

    def generate(self):
        for i in range(self.answers):
            self.results.append([])
            for j in range(self.guesses):
                self.results[i].append(random.choice(OPTIONS))

    def get(self):
        return self.results
