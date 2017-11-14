from math import *
import scipy.stats as stats
import numpy as np
import random



class PointToPointDemo(object):
    def __init__(self, conversion = 1):
        self.channelMode = Channel()
        self.conversion = conversion

    def setConversion(self, conversion):
        self.conversion = conversion

    def getThroughput(self):
        gamma = self.channelMode.getGamma() * self.conversion
        return log(1 + gamma)

    def getAvgThroughput(self, times):
        sumRecord = 0.0
        for i in xrange(times):
            sumRecord += self.getThroughput()
            self.channelMode.randomRayleigh()
        return sumRecord / times


class Channel(object):
    def __init__(self):
        self.distance = 5
        self.alpha = 3  ## Path loss exp factor.
        self.smallScale = stats.rayleigh.rvs() ## small scale fade
        self.noise = 10 ** (-7)
        self.np = -40

    ## set attributes manually
    def setDistance(self, distance):
        self.distance = distance

    def setAlpha(self, alpha):
        self.alpha = alpha

    def setSmallScale(self, smallScale):
        self.smallScale = smallScale

    def setNoise(self, noise):
        self.np = 40
        self.noise = 10 ** (noise / 10 - 3)

    ## use random attributes
    def random(self):
        self.distance = random.randint(0, 10)
        self.alpha = 3
        self.smallScale = stats.rayleigh.rvs()
        self.noise = 10 ** (-7)

    def randomRayleigh(self):
        self.smallScale = stats.rayleigh.rvs()

    def getGamma(self):
        return self.distance ** (-self.alpha * 2) * self.smallScale ** 2 / self.noise


if __name__ == "__main__":
    PtP = PointToPointDemo(0.5)
    print PtP.getThroughput()