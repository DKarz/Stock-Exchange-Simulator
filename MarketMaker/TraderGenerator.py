import sqlite3
import csv
import time
import re
import random as rnd
import socket
import pickle
import time
from mm_client import *


class TraderClass:

    maxorders = 10
    maxbalance = 8
    sharebalance = dict()
    allorders = dict()
    overprice = 0.01
    underprice = 0.05
    buy = 0
    sell = 0

    mintrade = 1
    maxtrade = 10
    

    def __init__(self, _mintrade = 1, _maxtrade = 10, _maxbalance = 8, _maxorders = 10):
        self.mintrade = _mintrade
        self.maxtrade = _maxtrade
        self.maxbalance = _maxbalance
        self.maxorders = _maxorders

    def GetType(self):
        types = ["buy", "sell"]
        return rnd.choice(types)

    def GetLimit(self):
        limits = ["Limit", "FillOrKill"]
        return rnd.choice(limits)


    def GenerateOrder(self, clientid, limit, type, name, amount, price):
        
        if (not name in self.sharebalance):
            self.sharebalance[name] = 0;
        if (type == "buy"):
            if (self.sharebalance[name] >= self.maxbalance):
                return "fail"
            self.sharebalance[name] += 1;
        if (type == "sell"):
            if (self.sharebalance[name] <= -self.maxbalance):
                return "fail"
            self.sharebalance[name] -= 1;

        query = ["MarketMaker " + str(clientid)] # id
        query.append(limit) # limit or FOK
        query.append(type) # buy or sell
        query.append(name) # product name
        query.append(amount) # product amount

        if (type == "buy"):
            price *= rnd.uniform(1 - self.overprice, 1 + self.underprice);
        if (type == "sell"):
            price *= rnd.uniform(1 - self.underprice, 1 + self.overprice);

        query.append(price)
        reqid = process(query, 0)
        #print(reqid)
        #print(query)

        #query.append(reqid[0])

        if (not name in self.allorders):
            self.allorders[name] = [];
        self.allorders[name].append(query);

        #while len(self.allorders[name]) > self.maxorders:
            #delete(0, self.allorders[name][-1][-1])

        return [name, type, price]


    def Dummy(self, Market, type = "any", limit = "any"):
        myid = 1

        if (type == "any"):
            type = self.GetType()
        if (limit == "any"):
            limit = self.GetLimit()

        shareid = int(rnd.randrange(0, Market.Size()))
        amount = rnd.randint(self.mintrade, self.maxtrade)
        price = Market.shares[shareid].GetPrice()
        name = Market.shares[shareid].name;

        return self.GenerateOrder(myid, limit, type, name, amount, price)



    def Greedy(self, Market, coef, type = "any", limit = "any"):
        if (coef <= 1):
            return

        myid = 2

        if (type == "any"):
            type = self.GetType()
        if (limit == "any"):
            limit = self.GetLimit()

        shareid = int(rnd.randrange(0, Market.Size()))
        amount = rnd.randint(self.mintrade, self.maxtrade)
        price = Market.shares[shareid].GetPrice() * coef
        name = Market.shares[shareid].name;

        return self.GenerateOrder(myid, limit, type, name, amount, price)


    def Charitable(self, Market, coef, type = "any", limit = "any"):
        if (coef >= 1):
            return

        myid = 3

        if (type == "any"):
            type = self.GetType()
        if (limit == "any"):
            limit = self.GetLimit()

        shareid = int(rnd.randrange(0, Market.Size()))
        amount = rnd.randint(self.mintrade, self.maxtrade)
        price = Market.shares[shareid].GetPrice() * coef
        name = Market.shares[shareid].name;

        return self.GenerateOrder(myid, limit, type, name, amount, price)


    def Oracle(self, Market, EPS = 0.005, type = "any", limit = "any"):
        myid = 4

        if (type == "any"):
            type = self.GetType()
        if (limit == "any"):
            limit = self.GetLimit()

        candidates = []

        if (type == "buy"):
            for i in range(Market.Size()):
                if (Market.shares[i].drift > EPS):
                    candidates.append(i)
        else:
            for i in range(Market.Size()):
                if (Market.shares[i].drift < -EPS):
                    candidates.append(i)

        if (len(candidates) == 0):
            return
        shareid = rnd.choice(candidates);
        amount = rnd.randint(self.mintrade, self.maxtrade)
        price = Market.shares[shareid].GetPrice()
        name = Market.shares[shareid].name;

        return self.GenerateOrder(myid, limit, type, name, amount, price)



    def Balancer(self, Market):
        myid = 5

        if (type == "any"):
            type = self.GetType()
        if (limit == "any"):
            limit = self.GetLimit()

        name = "none"
        if (type == "buy"):
            minn = 0;
            for cur in sharebalance:
                if (sharebalance[cur] < minn):
                    minn = sharebalance[cur]
                    name = cur
        else:
            maxx = 0;
            for cur in sharebalance:
                if (sharebalance[cur] > maxx):
                    maxx = sharebalance[cur]
                    name = cur

        if (name == "none"):
            return
        shareid = Market.IdByName(name);
        if (shareid == -1):
            return
        amount = rnd.randint(self.mintrade, self.maxtrade)
        price = Market.shares[shareid].GetPrice()
        name = Market.shares[shareid].name;

        return self.GenerateOrder(myid, limit, type, name, amount, price)


    def Specific(self, Market, _name):
        myid = 6

        if (type == "any"):
            type = self.GetType()
        if (limit == "any"):
            limit = self.GetLimit()

        shareid = Market.IdByName(_name);
        if (shareid == -1):
            return
        amount = rnd.randint(self.mintrade, self.maxtrade)
        price = Market.shares[shareid].GetPrice()
        name = Market.shares[shareid].name;

        return self.GenerateOrder(myid, limit, type, name, amount, price)


    
