from math import *
import scipy.stats as stats
import numpy as np
import numpy.linalg as la
import random



class PointToPointDemo(object):
    def __init__(self, conversion = 1, numofAttena = 1, type = 0):
        self.channelMode = Channel(numofAttena, type)
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
            self.channelMode.random()
        return sumRecord / times


class Channel(object):
    def __init__(self, numofAttena = 1, type = 0):
        self.distance = 5
        self.alpha = 3  ## Path loss exp factor.
        self.numofAttena = numofAttena
        self.type = type
        if numofAttena == 1:
            if not type:
                self.smallScale = stats.rayleigh.rvs() ## small scale fade
            else:
                self.smallScale = stats.rice.rvs()
        else:
            if not type:
                self.smallScale = stats.rayleigh.rvs((numofAttena, 1))
                _, tmp, _ = la.svd(self.smallScale)
                self.smallScale = tmp[0]
            else:
                self.smallScale = stats.rice.rvs((numofAttena, 1))
                _, tmp, _ = la.svd(self.smallScale)
                self.smallScale = tmp[0]

        self.noise = 10 ** (-7)
        self.np = -40

    ## set attributes manually
    def setChannel(self, type):
        self.type = type
        if self.numofAttena == 1:
            if not type:
                self.smallScale = stats.rayleigh.rvs() ## small scale fade
            else:
                self.smallScale = stats.rice.rvs()
        else:
            if not type:
                self.smallScale = stats.rayleigh.rvs((self.numofAttena, 1))
                _, tmp, _ = la.svd(self.smallScale)
                self.smallScale = tmp[0]
            else:
                self.smallScale = stats.rice.rvs((self.numofAttena, 1))
                _, tmp, _ = la.svd(self.smallScale)
                self.smallScale = tmp[0]


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
        self.setChannel(self.type)

    def getGamma(self):
        return self.distance ** (-self.alpha * 2) * self.smallScale ** 2 / self.noise


if __name__ == "__main__":
    PtP = PointToPointDemo(0.5)
    print PtP.getThroughput()