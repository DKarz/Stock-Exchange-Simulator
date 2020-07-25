import sqlite3
import csv
import time
import re
import random as rnd
import numpy as np
from matplotlib import pyplot as plt
import socket
import pickle
import time
from TraderGenerator import *

# initializing

AvailableGoodsFile = open("AvailableGoods.txt", "r")
AvailableGoods = AvailableGoodsFile.read().split('\n')

for i in range(len(AvailableGoods)):
    AvailableGoods[i] = AvailableGoods[i].split('; ')

print(AvailableGoods, end='\n\n')


class ShareClass:

    def __init__(self, initer):

        # Setting factors

        self.prices = []
        self.name = initer[0]
        self.minIPO = int(initer[1])
        self.maxIPO = int(initer[2])
        self.drift = float(initer[3])
        self.defaultdrift = self.drift
        self.diffusion = float(initer[4])
        
        '''
        self.compl = 
        self.subst =  
        self.status = 
        '''

    def ModifyDrift(self):
        return 0.1 * rnd.normalvariate(0, 1) * self.defaultdrift


    def SetStartingPrice(self):
        self.prices.append(rnd.randrange(self.minIPO, self.maxIPO))
        self.avgIPO = self.prices[-1] 
        return self.prices[-1]


    def GeneratePrice(self):

        # Generating IPO

        if (len(self.prices) == 0):
            return self.SetStartingPrice()

        # Modifying price

        new_price = self.prices[-1]
        new_price = max(0, new_price + self.avgIPO * rnd.normalvariate(self.drift, self.diffusion))
        self.prices.append(new_price)

        # Modifying price dynamic

        self.drift += self.ModifyDrift()
        self.Stabilize()

        return self.prices[-1]


    def Stabilize(self):
        if (self.prices[-1] < 0.1 * self.avgIPO and self.drift < 0):
            self.drift = -self.drift

        if (self.prices[-1] > 10 * self.avgIPO and self.drift > 0):
            self.drift = -self.drift

    def GetPrice(self):
        return self.prices[-1]





class MarketClass:

    allprices = []
    curprices = []
    shares = []
    size = 0
    DELTA = 0.01

    def __init__(self, initer):
        self.shares = [ShareClass(t) for t in initer]
        self.size = len(self.shares)
        self.allprices = [[] for t in initer]

    def NewDay(self):
        self.curprices = []
        for i in range(self.size):
            self.allprices[i].append(self.shares[i].GeneratePrice())
            self.curprices.append(self.allprices[i][-1])

    def Bankruptcy(self):
        stay = [0 for i in range(self.size)]

        for i in range(self.size):
            if self.curprices[i] > self.DELTA:
                stay[i] = 1

        self.shares = [self.shares[i] for i in range(self.size) if stay[i] == 1]
        self.allprices = [self.allprices[i] for i in range(self.size) if stay[i] == 1]
        self.curprices = [self.curprices[i] for i in range(self.size) if stay[i] == 1]
        self.size = len(self.shares)


    def AddShare(self, t):
        self.shares.append(ShareClass(t))
        self.size += 1
        self.curprices.append(self.shares[-1].GeneratePrice())
        self.allprices.append([curprices[-1]])

    def Size(self):
        return self.size

    def IdByName(self, name):
        for i in range(size):
            if (shares[i].name == name):
                return i
        return -1





Market = MarketClass(AvailableGoods)
Traders = TraderClass()
Market.NewDay()

TIME = 100
deals = dict()
for i in range(len(Market.shares)):
    deals[Market.shares[i].name] = [[Market.shares[i].prices[-1]], [Market.shares[i].prices[-1]]];
maxx = 0
for j in range(1,TIME):
    Market.NewDay()
    Market.Bankruptcy()

    for i in range(len(Market.shares)):
        deals[Market.shares[i].name][0].append(deals[Market.shares[i].name][0][-1])
        deals[Market.shares[i].name][1].append(deals[Market.shares[i].name][1][-1])

    if (True):
        for i in range(30):
            res = Traders.Dummy(Market)

            if (res == 'fail'):
                continue
            #print(res)
            #print(deals[res[0]])
            maxx = max(maxx, res[2])
            if (res[1] == "buy"):
                deals[res[0]][0][-1] = res[2]
            else:
                deals[res[0]][1][-1] = res[2]
            time.sleep(0.04)
        print(Market.curprices)



days = np.linspace(1, TIME, TIME)
print("MAX:", maxx)

'''
for i in range(len(Market.shares)):
    print(Market.shares[i].prices[0])
    plt.plot(days, deals[Market.shares[i].name][0], label='buy')
    plt.plot(days, deals[Market.shares[i].name][1], label='sell')
    plt.title(Market.shares[i].name)
    plt.show()
'''

