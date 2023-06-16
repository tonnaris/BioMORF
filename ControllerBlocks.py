import matplotlib.pyplot as plt
import numpy as np

def tanh(a):
    return (np.exp(2 * a) - 1) / (np.exp(2 * a) + 1)

class CPG:
    def __init__(self):
        self.outputH1 = 0.001
        self.outputH2 = 0.001
        self.activityH1 = 0.0
        self.activityH2 = 0.0

        self.WeightH1_H1 = 1.2
        self.WeightH2_H2 = 1.2
        self.WeightH1_H2 = -0.2
        self.WeightH2_H1 = 0.2

        self.set_frequency()
        self.outH1history = []
        self.outH2history = []

    def set_frequency(self, sigma=0.02 * np.pi):
        a = 1.01 * np.array([[np.cos(sigma), np.sin(sigma)], [-np.sin(sigma), np.cos(sigma)]])

        self.WeightH1_H1 = a[0, 0]
        self.WeightH2_H2 = a[1, 1]
        self.WeightH1_H2 = a[0, 1]
        self.WeightH2_H1 = a[1, 0]

    def update_history(self):
        if len(self.outH2history) > 100:
            self.outH2history.pop(0)
            self.outH1history.pop(0)

        self.outH1history.append(self.outputH1)
        self.outH2history.append(self.outputH2)

    def update(self):
        activityH1 = self.WeightH1_H1 * self.outputH1 + self.WeightH1_H2 * self.outputH2
        activityH2 = self.WeightH2_H2 * self.outputH2 + self.WeightH2_H1 * self.outputH1
        self.outputH1 = tanh(activityH1)
        self.outputH2 = tanh(activityH2)

        self.update_history()

        return self.outputH1, self.outputH2
