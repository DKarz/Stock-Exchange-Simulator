from time import strftime
from time import gmtime
import data
from datetime import datetime
import time
import sqlite3
import random
import client
import requests
from bs4 import BeautifulSoup


def buyOrder(ordertype, product, amount, price):
    output = " Buy {}\n {}    Amount: {}    Cost: {}"
    return output.format(product,ordertype, str(amount), str(price))


def sellOrder(ordertype, product, amount, price):
    output = " Sell {}\n {} Amount: {} Cost: {}"
    return output.format(product,ordertype, str(amount), str(price))

def Order(req, ordertype, product, amount, price):
    output = " {} {}\n {} Amount: {} Cost: {}"
    return output.format(req, product,ordertype, amount, price)

import csv
def addToHis(action, ordertype, product, amount, price):
    with open("userHistory.csv", "a") as file:
        write = csv.writer(file)
        write.writerow([action, ordertype, product, amount, price])

def clearHis():
    with open("userHistory.csv", "w") as file:
        pass

def getGeom(str):
    j = str.find(",")
    str = str[j:]
    j = str.find(",")
    str = str[j + 1:]
    j = str.find(",")
    str = str[j + 2:-1]
    nums = str.split(", ")
    return (int(nums[0]),int(nums[1]))

def barInfo():
    timeNow = str(time.strftime("%H:%M:%S   %b %d %Y")) + "          "
    balanceNow = str(round(data.balance[0], 3))+" "+data.balance[1] + "         "
    return timeNow + balanceNow + data.username + "         "


def getId(text):
    ind1 = text.find("id:")
    ind2 = text.find(";")
    return text[ind1+4: ind2]

def getPrice(text):
    ind = text.find("Cost:")
    return text[ind+6:]

def getAmt(text):
    ind = text.find("Amount:")
    ind1 = text.find("Cost:")
    #print(text[ind+8: ind1-1])
    return text[ind+8: ind1-1]

def getTime(time_):
    return datetime.utcfromtimestamp(float(time_)).strftime("%H:%M:%S %d-%m")


def sec_to_time(sec):
    # t1 = strftime("%H:%M", gmtime(sec[0]))
    # t2 = strftime("%H:%M", gmtime(sec[1]))

    t1 = datetime.fromtimestamp(sec[0]).strftime("%H:%M")
    t2 = datetime.fromtimestamp(sec[1]).strftime("%H:%M")
    #print("sec", t1, t2)
    return t1 +" - "+ t2

def getOrder():
    try:
        if data.goLocal:
            raise Exception                              ####
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()

        output = client.exe('SELECT * FROM orders')
    except:
        #print("EXCEPTION OCCURRED: Local database is used instead ")
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()

        c.execute('SELECT * FROM orders')
        output = c.fetchall()

    # for el in data:
    #     print(el)
    return output


def findOrder(product = None, type = None, request = None, amount = None, price = None):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    if product != "":
        c.execute("SELECT * FROM orders WHERE product='{}'".format(product))
    elif product == "":
        c.execute('SELECT * FROM orders')
    elif type =="all" and request == "all" and amount == "" and price == "":
        c.execute("SELECT * FROM orders WHERE product='{}'".format(product))
    elif type != "all" and request != "all" and amount == "" and price == "":
        c.execute("SELECT * FROM orders WHERE product='{}' AND type='{}' AND request='{}'".format(product, type, request))
    elif type !="all" and request != "all" and amount != "" and price != "":
        t = "SELECT * FROM orders WHERE product='{}' AND type='{}' AND request='{}' AND amount='{}' AND price='{}'"
        t=t.format(product, type, request, amount, price)
        c.execute(t)
    else:
        c.execute('SELECT * FROM orders')

    data = c.fetchall()
    return data

def getNews():
    #print("Start updating")
    obj = []
    temp = []
    i = 0
    while len(obj) == 0:
        i += 1
        base_url = "https://www.msn.com/en-us/money/markets"
        r = requests.get(base_url)
        soap = BeautifulSoup(r.content, features="html.parser")
        obj = soap.select("h3")
    # print(obj)

    for el in obj[1:]:
        t = str(el)
        t = t.replace('<h3>', "")
        t = t.replace('</h3>', "")
        temp.append(t)

    obj = temp
    data.news = obj
    #print("News are updated")
    #print(data.news)


def getRandUnix():
    t = random.random()
    return float(time.time())*t


def log_text_format(text):
    output = "At " + time.strftime("%H:%M:%S %b %d %Y") + "\n"
    output += "From " + data.username + " " + data.userid + "\n"
    output += "Text:\n" + text + "\n\n\n"
    return output


def fill_demo():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    # c.execute("INSERT INTO orders VALUES({}, 'Mike1', 'Limit', 'sell', 'Bitcoin', 10, 9, 111)".format(getRandUnix()))
    # c.execute("INSERT INTO orders VALUES({}, 'Mike2', 'Limit', 'buy', 'Hsecoin', 1, 9, 112)".format(getRandUnix()))
    # c.execute("INSERT INTO orders VALUES({}, 'Mike3', 'Limit', 'sell', 'Pony', 7, 7, 113)".format(getRandUnix()))
    # c.execute("INSERT INTO orders VALUES({}, 'Mike4', 'Limit', 'buy', 'Witchers coin', 7, 9, 114)".format(getRandUnix()))
    # c.execute("INSERT INTO orders VALUES({}, 'Mike5', 'Limit', 'sell', 'Bread', 10, 1, 115)".format(getRandUnix()))
    # c.execute("INSERT INTO orders VALUES({}, 'Mike6', 'Limit', 'buy', 'Cola', 5, 9, 116)".format(getRandUnix()))
    c.execute("INSERT INTO orders VALUES({}, 'Mike7', 'Limit', 'buy', 'Pepsi', 12, 1, 11)".format(getRandUnix()))
    c.execute("INSERT INTO orders VALUES({}, 'Mike8', 'Limit', 'sell', 'Cookies', 15, 4, 12)".format(getRandUnix()))
    c.execute("INSERT INTO orders VALUES({}, 'Mike9', 'Limit', 'sell', 'Pies', 3, 9, 119)".format(getRandUnix()))
    c.execute("INSERT INTO orders VALUES({}, 'Mike10', 'Limit', 'sell', 'Milk', 10, 8, 1110)".format(getRandUnix()))
    conn.commit()


def resOut(arr):
    resTxt = f"""Buy request ID: {arr[0]}\nSell request ID: {arr[1]}\nBuyer ID: {arr[2]}\nSeller ID {arr[3]}\nAmount: {arr[4]}\nTotal: {arr[5]}"""
    return resTxt


def putPersonalData():
    with open("personalData.csv", "w") as file:
        write = csv.writer(file)
        write.writerow([data.username,
                        data.userid,
                        data.password,
                        data.balance[0],
                        data.balance[1],
                        ])

def getXY(rett):
    X = []
    Y = []
    for i in range(len(rett)):
        X.insert(i, getTime(rett[i][1]))
        Y.insert(i, rett[i][0])

    return (X, Y)


def merger(data1):
    prices = {}
    for el in data1:
        if el[-1] != float(data.userid):
            if el[-2] not in prices:
                prices[el[-2]] = [0, el]
            prices[el[-2]][0] += el[-3]
    return prices

def getPersonalData():
    with open("personalData.csv", "r") as file:
        csv_reader = csv.reader(file, delimiter=',')
        persdata = []
        for row in csv_reader:
            persdata = row
            break
        data.username = persdata[0]
        data.userid = persdata[1]
        data.password = persdata[2]
        data.balance = (float(persdata[3]), persdata[4])


def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True


# conn = sqlite3.connect('C:\coding\projServer\orders.db') # HERE SHOULD BE PATH TO DB
# c = conn.cursor()
# c.execute("CREATE TABLE IF NOT EXISTS orders(reqid REAL, name TEXT, type TEXT, request TEXT, product TEXT, amount REAL, price REAL, uid REAL)")
# #c.execute("INSERT INTO orders VALUES(17, 'Meee', 'Limit', 'sell', 'pony', 11, 11, 69420)")
# #fill_demo()
# c.execute('SELECT * FROM orders')
# data1 = c.fetchall()
# num = 0
# for el in data1:
#     num+=1
#     print(el)
# print(str(num) + " elements")



getPersonalData()          # VERY IMPORTANT LINE !!!!! NEVER DELETE

