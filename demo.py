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

    def setNumofAttenna(self, num):
        self.channelMode.setNumOfAntenna(num)

    def setType(self, type):
        self.channelMode.setChannel(type)

    def setAlpha(self, alpha):
        self.channelMode.setAlpha(alpha)

    def setDistance(self, d):
        self.channelMode.setDistance(d)

    def setNoise(self, noise):
        self.channelMode.setNoise(noise)

    def setSmallScale(self, ss):
        self.channelMode.setSmallScale(ss)

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
        self.r = 0
        if numofAttena == 1:
            if not type:
                self.smallScale = stats.rayleigh.rvs() ## small scale fade
                self.r = self.smallScale
            else:
                self.smallScale = stats.rice.rvs()
                self.r = self.smallScale
        else:
            if not type:
                self.smallScale = stats.rayleigh.rvs((numofAttena, 1))
                self.r = np.sum(self.smallScale)
                _, tmp, _ = la.svd(self.smallScale)
                self.smallScale = tmp[0]
            else:
                self.smallScale = stats.rice.rvs((numofAttena, 1))
                self.r = np.sum(self.smallScale)
                _, tmp, _ = la.svd(self.smallScale)
                self.smallScale = tmp[0]

        self.noise = 10 ** (-7)
        self.np = -40

    ## set attributes manually
    def setChannel(self, type):
        self.type = type
        self.ResetChannel()

    def setNumOfAntenna(self, num):
        self.numofAttena = num
        self.ResetChannel()

    def ResetChannel(self):
        if self.numofAttena == 1:
            if not type:
                self.smallScale = stats.rayleigh.rvs() ## small scale fade
            else:
                self.smallScale = stats.rice.rvs(1)
        else:
            if not type:
                self.smallScale = stats.rayleigh.rvs((self.numofAttena, 1))
                self.smallScale = np.mat(self.smallScale)
                _, tmp, _ = la.svd(self.smallScale)
                self.smallScale = tmp[0]
            else:
                self.smallScale = stats.rice.rvs(1, (self.numofAttena, 1))
                self.smallScale = np.mat(self.smallScale)
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
        self.ResetChannel()

    def getGamma(self):
        return self.distance ** (-self.alpha * 2) * self.smallScale * self.r / self.noise


