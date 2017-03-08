__author__ = "Michael J. Pitcher"


class Event:

    def __init__(self, probability):
        self.probability = probability
        self.total = 0

    def get_rate(self):
        return self.probability * self.total
