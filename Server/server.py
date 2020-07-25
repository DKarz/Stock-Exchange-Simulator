import socket
import pickle
import sqlite3
import csv
import time
import re
import os

os.system("color a")

ENABLE_IPv4 = False

ip = input("Do you wish to use the local network? (y/n) ")
if ip == "y": ENABLE_IPv4 = True

ENABLE_OUTPUT = True

global stats
global conn, conn1
global c, s, b
global buffer
global last_delete
last_delete = time.time()
buffer = []

IP = "127.0.0.1"
if ENABLE_IPv4:
  hostname = socket.gethostname()
  IP = socket.gethostbyname(hostname)
PORT = 1234

def snd(what):
  try:
    client_socket.send(what)
  except:
    return False
  return True


def box_graph(product, buy_sell, new):
  c.execute(f"SELECT * FROM orders WHERE product = '{product}' AND request = 'buy' ORDER BY price DESC")
  try: best_ask = c.fetchall()[0][6]
  except: best_ask = 0
  if new != -69:
    if best_ask > new: best_ask = new
  c.execute(f"SELECT * FROM orders WHERE product = '{product}' AND request = 'sell' ORDER BY price ASC")
  try: best_bid = c.fetchall()[0][6]
  except: best_bid = 0
  if new != -69:
    if best_bid < new: best_bid = new
  b.execute(f"INSERT INTO box VALUES('{product}', {best_bid}, {best_ask}, {time.time()})")

def return_box_graph(product, buy_sell):
  ret = []
  for pair in start_end:
    b.execute(f"SELECT * FROM box WHERE product = '{product}' AND time >= {pair[0]} AND time <= {pair[1]}")
    ret1 = []
    for i in b.fetchall():
      ret1.append((i[1], i[2]))
    ret.append(ret1)
  return ret

def create_table():
  c.execute("CREATE TABLE IF NOT EXISTS orders(reqid REAL, name TEXT, type TEXT, request TEXT, product TEXT, amount REAL, price REAL, uid REAL)")

def stars_table():
  st.execute("CREATE TABLE IF NOT EXISTS stars(login TEXT, what TEXT)")

def debts_table():
  d.execute("CREATE TABLE IF NOT EXISTS debts(login TEXT, debt REAL, id REAL, uid REAL)")

def a_debts_table():
  ad.execute("CREATE TABLE IF NOT EXISTS a_debts(asset TEXT, debt REAL, id REAL, uid REAL)")

def history_table():
  h.execute("CREATE TABLE IF NOT EXISTS history(login TEXT, product TEXT, amount REAL, price REAL, type TEXT)")

def stats_table():
  s.execute("CREATE TABLE IF NOT EXISTS stats (product TEXT, price REAL, time REAL, type TEXT)")

def create_table_users():
  u.execute("CREATE TABLE IF NOT EXISTS users(id REAL, login TEXT, password TEXT, balance REAL)")

def box_table():
  b.execute("CREATE TABLE IF NOT EXISTS box(product TEXT, best_bid REAL, best_ask REAL, time REAL)")

def assets_table():
  a.execute("CREATE TABLE IF NOT EXISTS assets(uid REAL, product TEXT, amount REAL)")

def send_many(num, li):
  snd(pickle.dumps(num))
  for i in range(num):
    if not rec(client_socket): return False
    go = li[i]
    se = pickle.dumps(go)
    if not snd(se): break

def send_many_box(num, li):
  snd(pickle.dumps(num))
  for i in range(num):
    if not rec(client_socket): return False
    snd(pickle.dumps(len(li[i])))
    for j in range(len(li[i])):
      if not rec(client_socket): return False
      go = li[i][j]
      se = pickle.dumps(go)
      if not snd(se): break

def return_history(login):
  h.execute(f"SELECT * FROM history WHERE login = '{login}'")
  return h.fetchall()

def get_stars(login, password):
  if not find(login, password):
    return [False]
  st.execute(f"SELECT * FROM stars WHERE login = '{login}'")
  ret = []
  for i in st.fetchall():
    ret.append(i[1])
  return ret

def add_star(what, login, password):
  if not find(login, password):
    return False
  for i in what:
    st.execute(f"INSERT INTO stars VALUES('{login}', '{i}')")
  return True

global max_buy_d, min_sell_d 
max_buy_d = dict()
min_sell_d = dict()

'''
def max_buy(prod):
  try:
    return max_buy_d[prod]
  except: pass
  c.execute(f"SELECT MAX(price) FROM orders WHERE product = '{prod}' AND request = 'buy'")
  return(c.fetchall()[0][0])
  
def min_sell(prod):
  try: return min_sell_d[prod]
  except: pass
  c.execute(f"SELECT MIN(price) FROM orders WHERE product = '{prod}' AND request = 'sell'")
  return(c.fetchall()[0][0])
'''

def remove_star(what, login, password):
  if not find(login, password):
    return False
  for i in what:
    st.execute(f"DELETE FROM stars WHERE login = '{login}' AND what = '{i}'")
  return True

global best_bid, best_ask
best_bid, best_ask = {}, {}

def calc_average(product, buy_sell, new):
  '''
  prod = product
  if buy_sell == 'sell':
    prod += '^sell^'
  if prod in stats:
    if new < 0:
      stats[prod][0] -= new
      stats[prod][1] -= 1
    else:
      stats[prod][0] += new
      stats[prod][1] += 1
    temp = stats[prod][1]
    if temp <= 0:
      temp = 1
    ret = stats[prod][0]/temp
    s.execute(f"INSERT INTO stats VALUES('{product}', {ret}, {ti_me}, '{buy_sell}')")
    return ret
  try:
    c.execute(f"SELECT * FROM orders WHERE product = '{product}' AND request = '{buy_sell}'")
  except Exception as ex:
    print("EXCEPTION:", ex)
    return 0
  summ = 0
  alll = c.fetchall()
  for i in alll:
    summ += i[6]
  a = len(alll)
  stats[prod] = [summ, a]
  if a <= 0:
    a = 1
  ret = summ/a
  s.execute(f"INSERT INTO stats VALUES('{product}', {ret}, {ti_me}, '{buy_sell}')")
  return ret
  '''
  global best_bid, best_ask
  try: sss = best_bid[product]
  except: best_bid[product] = 0
  try: sss = best_ask[product]
  except: best_ask[product] = 0 
  
  if buy_sell == "sell":
    c.execute(f"SELECT * FROM orders WHERE product = '{product}' AND request = 'sell' ORDER BY price ASC")
    fet = c.fetchall()
    try: best_bid[product] = fet[0][6]
    except: pass
    if new != -69:
      if best_bid[product] < new: best_bid[product] = new

    s.execute(f"INSERT INTO stats VALUES('{product}', {best_bid[product]}, {time.time()}, '{buy_sell}')")

  else:
    c.execute(f"SELECT * FROM orders WHERE product = '{product}' AND request = 'buy' ORDER BY price DESC")
    try: best_ask[product] = c.fetchall()[0][6]
    except: pass
    if new != -69:
      if best_ask[product] > new: best_ask[product] = new

    s.execute(f"INSERT INTO stats VALUES('{product}', {best_ask[product]}, {time.time()}, '{buy_sell}')")

def return_stats(product, time_start, time_end, type):
  try:
    s.execute(f"SELECT price, time FROM stats WHERE product = '{product}' AND type = '{type}' AND time >= {time_start} AND time <= {time_end}")
  except Exception as ex:
    print("EXCEPTION:",ex)
    return [{}]
  return s.fetchall()

def show_selected(ss):
  data = ss.fetchall()
  for i in data:
    print(i)
  print()

def return_debt(login, uid, id):
  #print(f"Returning debt to {login}...")
  d.execute(f"SELECT * FROM debts WHERE id = {id} and uid = {uid}")
  try: 
    substract(False, d.fetchall()[0][1], login)
  except: pass
  d.execute(f"DELETE FROM debts WHERE id = {id} and uid = {uid} and id = {id}")

def return_a_debt(id, uid):
  #print("Return A_Debt to", id) 
  ad.execute(f"SELECT * FROM a_debts WHERE id = {id}")
  fet = ad.fetchall()
  #print("LEN:", len(fet))
  try:
    #print("KEKEK: ", uid, fet[0][0], fet[0][1])
    add_asset(uid, fet[0][0], fet[0][1])
  except: pass
  ad.execute(f"DELETE FROM a_debts WHERE id = {id}")

def sub_from_debt(uid, id, sub):
  #print(f"Subing {sub} debt from {uid}, id = {id}...") 
  d.execute(f"SELECT * FROM debts WHERE uid = {uid} AND id = {id}")
  try:
    fet = d.fetchall()[0][1]
  except:
    return False
  if fet - sub <= 0: d.execute(f"DELETE FROM debts WHERE uid = {uid} AND id = {id}")
  else: d.execute(f"UPDATE debts SET debt = {fet - sub} WHERE uid = {uid} AND id = {id}")
  return True

def sub_from_a_debt(uid, id, sub, asset):
  ad.execute(f"SELECT * FROM a_debts WHERE uid = {uid} AND asset = '{asset}' AND id = {id}")
  try:
    fet = ad.fetchall()[0][1]
  except:
    return False
  if fet - sub <= 0:
    ad.execute(f"DELETE FROM a_debts WHERE uid = {uid} AND asset = '{asset}' AND id = {id}")
  else: ad.execute(f"UPDATE a_debts SET debt = {fet - sub} WHERE uid = {uid} AND asset = '{asset}' AND id = {id}")
  return True

def add_debt(login, uid, id, add):
  print(f"Adding debt to {login}, amount: {add}")
  if not sub_from_debt(uid, id, -1*add):
    print("NEW DEBT")
    d.execute(f"INSERT INTO debts VALUES('{login}', {add}, {id}, {uid})")

def add_a_debt(asset, uid, reqid, add):
  if not sub_from_a_debt(uid, reqid, -1*add, asset):
    ad.execute(f"INSERT INTO a_debts VALUES('{asset}', {add}, {reqid}, {uid})")
  
def find(login, password):
    if not password:
      u.execute(f"SELECT * FROM users WHERE login = '{login}'") 
    else: u.execute(f"SELECT * FROM users WHERE login = '{login}' AND password = '{password}'")
    if len(u.fetchall()) == 0:
        return False
    return True

def register(login, password):
    u.execute(f"SELECT * FROM users WHERE login = '{login}'")
    if len(u.fetchall()) != 0:
        return False
    u.execute(f"INSERT INTO users VALUES({time.time()}, '{login}', '{password}', 1000)")
    conn3.commit()
    return True

def get_balance (login):
    u.execute(f"SELECT * FROM users WHERE login = '{login}'")
    if not find:
        return False
    fetch = u.fetchall()
    if len(fetch) == 0: return False
    for i in fetch:
        return i[3];

def add_to_buffer(ad):
  global last_delete
  global buffer
  if time.time() - last_delete > 10:
    buffer = []
    last_delete = time.time()
  buffer.insert(len(buffer), ad)


def print_table():
  if not ENABLE_OUTPUT: return
  c.execute("SELECT * FROM orders")
  show_selected(c)
  print(stats)
  #s.execute("SELECT * FROM stats")
  #show_selected(s)


def delete(login, id, uid):
  try:
    c.execute("DELETE FROM orders WHERE reqid =" + "\'" + str(id) + "\'")
    return_debt(login, uid, id)
    return_a_debt(id, uid)
  except:
    pass

def delete_history(login, password):
  if not find(login, password):
    return False
  h.execute(f"DELETE FROM history WHERE login = '{login}'")
  return True

def bug_log(text):
    f = open("bug_log.txt", "a")
    f.write(text +"\n")
    f.close()

def get_id(login):
  u.execute(f"SELECT * FROM users WHERE login = '{login}'")
  try:
    return u.fetchall()[0][0]
  except: return False

def add_history(login, product, amount, price, type):
  h.execute(f"INSERT INTO history VALUES('{login}', '{product}', {amount}, {price}, '{type}')")  

def substract(buy, total, login):
  if total == 0: return
  if buy: total *= -1
  u.execute(f"SELECT * FROM users WHERE login = '{login}'")
  bal = 0
  for i in u.fetchall(): bal = i[3]
  u.execute(f"UPDATE users SET balance = {bal+total} WHERE login = '{login}'")

def does_have(id, product, amount):
  #print("DOES:", id, product, amount)
  a.execute(f"SELECT * FROM assets WHERE product = '{product}' AND uid = {id} AND amount >= {amount} ")
  kkk = a.fetchall()
  #print(kkk)
  if len(kkk) != 0:
    return True
  return False

def add_asset(id, product, amount):
  a.execute(f"SELECT * FROM assets WHERE product = '{product}' and uid = {id}")
  fet = a.fetchall()
  a.execute(f"SELECT * FROM assets")
  if len(fet) == 0:
    a.execute(f"INSERT INTO assets VALUES({id}, '{product}', '{amount}')")
  else:
    a.execute(f"UPDATE assets SET amount = {float(fet[0][2]) + float(amount)} WHERE uid = {id} and product = '{product}'")

def my_assets(login, password):
  if not find(login, password):
    return False
  a.execute(f"SELECT * FROM assets WHERE uid = {get_id(login)}")
  return a.fetchall()

def process(b, login, password):
  #global max_buy_d
  mm = False
  if password == 'c35312fb3a7e05b7a44db2326bd29040':
    mm = True
  b[5] = float(b[5])
  def delete_all():
    c.execute("DELETE FROM orders")

  # delete_all()
  # fill_demo()
  # print_table()

  reqid = float(time.time())
  '''
  with open('input.csv', 'r') as i:
    a = csv.reader(i)
    b = list(a)[0]
  '''
  # print(reqid, b)
  # print()
  from_u = login
  uid = get_id(login)
  if not uid and not mm:
    return False
  if mm:
    uid = 666
  if b[1].lower() == 'limit':
    limit = True
  else:
    limit = False
  if b[2] == 'buy':
    buy = True
  else:
    buy = False
  product = b[3]
  amount = b[4]
  price = b[5]

  transaction_list = []
  list_counter = 0
  total = 0
  q = float(amount)
  buy_ssell = 'sell'
  '''
  box_graph(product, 'buy', price)
  calc_average(product, 'buy', price)
  box_graph(product, 'sell', price)
  calc_average(product, 'sell', price)
  '''

  if buy:
    c.execute("SELECT * FROM orders WHERE request = 'sell' AND product = " + "\'" + product + "\'" + " AND price <= " + str(price) + " ORDER BY price")
    for i in c.fetchall():
      if from_u == i[1] and not mm : continue
      if q == 0:
        break
      if i[5] > q:
        total += q * i[6]
        transaction_list.insert(list_counter, [reqid, i[0], float(uid), i[7], q, q * i[6]])
        add_to_buffer(['update', reqid, i[5]-q])
        sub_from_a_debt(i[7] , i[0], q, i[4])
        c.execute("UPDATE orders SET amount = '" + str(i[5] - q) + "' WHERE reqid =" + "\'" + str(i[0]) + "\'")
        if not mm: add_asset(uid, product, float(amount))
        #add_asset(i[7], product, -1*float(amount))
        add_history(login, product, q, q*i[6], "buy")
        q = 0
        list_counter += 1
        break
      else:
        q -= i[5]
        total += i[5] * i[6]
        transaction_list.insert(list_counter, [reqid, i[0], float(uid), i[7], i[5], i[5] * i[6]])
        add_to_buffer(['delete', reqid])
        c.execute("DELETE FROM orders WHERE reqid =" + "\'" + str(i[0]) + "\'")
        sub_from_a_debt(i[7] , i[0], i[5], i[4])
        #c.execute(f"SELECT * FROM orders WHERE reqid = {i[0]}")
        #if c.fetchall()[0][7] == min_sell_d[product]: min_sell_d[prroduct] = min_sell(product)
        if not mm: add_asset(uid, product, i[5])
        #add_asset(i[7], product, -1*i[5])
        add_history(login, product, i[5], i[5]*i[6], "buy")
        #calc_average(product, -1*i[6], 'sell')#Do we need that?
        list_counter += 1
    if q != 0 and limit:
      if not mm: add_debt(login, uid, reqid, q*price)
      if not mm: substract(True, q*price, login)
      add_to_buffer(['add', reqid, from_u, b[1] ,b[2], product, str(q), price, uid])
      c.execute("INSERT INTO orders VALUES(" + str(reqid) + ", '" + str(from_u) + "', '" + b[1] + "', '" + b[2] + "', '" + product + "', " + str(q) + ", " + str(price) + ", " + str(uid) + ")")
      #calc_average(product, -1*i[6], 'sell')#Do we need that?
      '''
      try:
        if price > max_buy_d[product]: max_buy_d[product] = price
      except:
        max_buy_d[product] = max_buy(product)
      '''

  else:
    c.execute("SELECT * FROM orders WHERE request = 'buy' AND product = " + "\'" + product + "\'" + " AND price >= " + str(price) + " ORDER BY price DESC")
    for i in c.fetchall():
      if from_u == i[1] and not mm : continue
      if q == 0:
        break
      '''
      ad.execute(f"SELECT * FROM a_debts WHERE id = {i[0]}")
      deb = 0
      try:
        deb = ad.fetchall()[0][1]
      except Exception as E: print("EXCEPTION:", E)
      '''
      if i[5] > q:
        total += q * i[6]
        transaction_list.insert(list_counter, [i[0], reqid, i[7], float(uid), q, q * i[6]])
        add_to_buffer(['update', reqid, i[5]-q])
        c.execute("UPDATE orders SET amount = '" + str(i[5] - q) + "' WHERE reqid =" + "\'" + str(i[0]) + "\'")
        if not mm: add_asset(uid, product, -1*float(amount))
        add_asset(i[7], product, float(amount))
        add_history(login, product, q, q*i[6], "sell")
        sub_from_debt(i[7], i[0], q*i[6])
        q = 0
        list_counter += 1
        break
      else:
        q -= i[5]
        total += i[5] * i[6]
        transaction_list.insert(list_counter, [i[0], reqid, i[7], float(uid), i[5], i[5] * i[6]])
        add_to_buffer(['delete', reqid])
        c.execute("DELETE FROM orders WHERE reqid =" + "\'" + str(i[0]) + "\'")
        #c.execute(f"SELECT * FROM orders WHERE reqid = {i[0]}")
        #if c.fetchall()[0][7] == max_buy_d[product]: max_buy_d[prroduct] = max_buy(product)
        if not mm: add_asset(uid, product, -1*i[5])
        add_asset(i[7], product, i[5])
        add_history(login, product, i[5], i[5]*i[6], "sell")
        sub_from_debt(i[7], i[0], i[5]*i[6])
        #calc_average(product, -1*i[6], 'buy')#Do we need that?
        list_counter += 1
    if q != 0 and not mm:
        add_a_debt(product, uid, reqid, q)
        a.execute(f"SELECT * FROM assets WHERE uid = {uid} AND product = '{product}'")
        prev = a.fetchall()[0][2]
        a.execute(f"UPDATE assets SET amount = {prev - q} WHERE uid = {uid} AND product = '{product}'")
        
    if q != 0 and limit:
        c.execute(f"INSERT INTO orders VALUES({reqid}, '{from_u}', '{b[1]}', '{b[2]}', '{product}', {q}, {price}, {uid})")
        add_to_buffer(['add', reqid, from_u, b[1] ,b[2], product, str(q), price, uid])
        #calc_average(product, price, 'sell')#Do wee need that?
        '''
        try:
          if price < min_sell_d[product]:
            min_sell_d[product] = price
        except:
          min_sell_d[product] = min_sell(product)
        '''
      
  if not mm: substract(buy, total, login)
  # print()
  # print("Total Cost:" ,total, '\n')
  #if ENABLE_OUTPUT: print("Resulting data base:")
  #if ENABLE_OUTPUT: print_table()
  # print("\nFINISHED\n")
  #c.close()
  #conn.close()
  if (len(transaction_list) == 0):
    return [str(reqid)]
  return transaction_list

def update():
  return buffer


def rec(client_socket):
  start = time.time()
  while True:
    if time.time()-start >= 0.5:
      print("Too much time wasted...")
      return False
    try:
      temp = pickle.loads(client_socket.recv(1024))
      return temp
    except Exception as exception:
      pass

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

global u, conn3, a, conn4, d, conn5, h, conn6, st, conn7, ad, conn8
conn3 = sqlite3.connect('users.db')
u = conn3.cursor()
create_table_users()
conn = sqlite3.connect('orders.db')
c = conn.cursor()
conn1 = sqlite3.connect('stats.db')
s = conn1.cursor()
conn2 = sqlite3.connect('box.db')
b = conn2.cursor()
conn4 = sqlite3.connect('assets.db')
a = conn4.cursor()
conn5 = sqlite3.connect('debts.db')
d = conn5.cursor()
conn6 = sqlite3.connect('history.db')
h = conn6.cursor()
conn7 = sqlite3.connect('stars.db')
st = conn7.cursor()
conn8 = sqlite3.connect('a_debts.db')
ad = conn8.cursor()

stars_table()
debts_table()
history_table()
stats_table()
create_table()
box_table()
assets_table()
stats = {}
a_debts_table()

print(f'Listening for connections on {IP}:{PORT}...')


while True:
  
  got = False
  server_socket.listen(1024)
  client_socket, client_adress = server_socket.accept()
  #server_socket.settimeout(0.5)
  client_socket.settimeout(0.5)
  command = rec(client_socket)
  if not command: continue
  start = time.time()

  try:
    if command == 'mm_process':
      if ENABLE_OUTPUT: print("Working on \"mm_process\" command.....")
      snd(pickle.dumps('ok'))
      got = rec(client_socket)
      if not got: continue
      got, login, key = got
      if ENABLE_OUTPUT: print("Got request: ", got, login, key)
      if key != 'c35312fb3a7e05b7a44db2326bd29040':
        if ENABLE_OUTPUT: print("Wrong key.....")
        snd(pickle.dumps([False]))
        continue
      ret = process(got, login, key)
      snd(pickle.dumps(ret))

    elif command == 'get':
      if ENABLE_OUTPUT: print("Working on \"get\" command.....")
      snd(pickle.dumps('ok'))
      got = rec(client_socket)
      if not got: continue
      if ENABLE_OUTPUT: print("Got request: ", got)
      k = re.search("update", got, re.I)
      kl= re.search("delete", got, re.I)
      try:
        gg = k.group(0)
        gg1= k1.group(0)
        continue
      except:
        pass
      c.execute(got)
      ret = c.fetchall()
      send_many(len(ret), ret)

    elif command == 'process':
      if ENABLE_OUTPUT: print("Working on \"process\" command.....")
      snd(pickle.dumps('ok'))
      got = rec(client_socket)
      if not got: continue
      got, login, password = got
      '''
      if got[2] == 'buy':
        if float(got[5]) >= min_sell(got[3]):
          if ENABLE_OUTPUT: print("Buy bids should be cheaper than sell ones")
          snd(pickle.dumps(["B>=S"]))
          continue
      else:
        if float(got[5]) <= max_buy(got[3]):
          if ENABLE_OUTPUT: print("Buy bids should be cheaper than sell ones")
          snd(pickle.dumps(["S<=B"]))
          continue
      '''
      if ENABLE_OUTPUT: print("Got request: ", got, login, password)
      if not find(login, password):
        if ENABLE_OUTPUT: print("Wrong login/password combination.....")
        snd(pickle.dumps([False]))
        continue
      if float(got[4])*float(got[5]) > get_balance(login) and got[3] == 'buy':
        if ENABLE_OUTPUT: print("Not enough money.....")
        snd(pickle.dumps([False]))
        continue
      if got[2] == 'sell' and not does_have(get_id(login), got[3], got[4]):
        if ENABLE_OUTPUT: print("Not enough assets.....")
        snd(pickle.dumps([False]))
        continue
      ret = process(got, login, password)
      snd(pickle.dumps(ret))

    elif command == 'update':
      if ENABLE_OUTPUT: print("Working on \"update\" command.....")
      snd(pickle.dumps('ok'))
      ret = update()
      if ENABLE_OUTPUT: print("To update: ", ret)
      snd(pickle.dumps(ret))

    elif command == 'delete':
      if ENABLE_OUTPUT: print("Working on \"delete\" command.....")
      snd(pickle.dumps('ok'))
      got = rec(client_socket)
      if not got: continue
      login, id = got
      delete(login, id, get_id(login))

    elif command == 'box':
      if ENABLE_OUTPUT: print("Working on \"box\" command.....")
      snd(pickle.dumps('ok'))
      try:
        got = rec(client_socket)
        if not got: continue
        product, L = got
      except: continue
      start_end = []
      try:
        for i in range(L):
          snd(pickle.dumps('ok'))
          got = rec(client_socket)
          if not got: continue
          start_end.append(got)
      except: continue
      ret = return_box_graph(product, start_end)
      send_many_box(len(ret), ret)

    elif command == 'my assets':
      if ENABLE_OUTPUT: print("Working on \"my assets\" command.....")
      snd(pickle.dumps('ok'))
      try:
        got = rec(client_socket)
        if not got: continue
        login, password = got
      except: continue
      ret = my_assets(login, password)
      send_many(len(ret), ret)

    elif command == 'bug':
      if ENABLE_OUTPUT: print("Working on \"bug\" command.....")
      snd(pickle.dumps('ok'))
      try:
        got = rec(client_socket)
        if not got: continue
      except: continue
      bug_log(got)

    elif command == 'register':
          if ENABLE_OUTPUT: print("Working on \"register\" command.....")
          snd(pickle.dumps("ok"))
          got = rec(client_socket)
          if not got: continue
          login, password = got
          snd(pickle.dumps(register(login, password)))
    elif command == 'get balance':
          if ENABLE_OUTPUT: print("Working on \"get balance\" command.....")
          snd(pickle.dumps("ok"))
          got = rec(client_socket)
          if not got: continue
          snd(pickle.dumps(get_balance(got)))

    elif command == 'get id':
          if ENABLE_OUTPUT: print("Working on \"get id\" command.....")
          snd(pickle.dumps("ok"))
          got = rec(client_socket)
          if not got: continue
          snd(pickle.dumps(get_id(got)))

    elif command == 'known user':
          if ENABLE_OUTPUT: print("Working on \"known user\" command.....")
          snd(pickle.dumps("ok"))
          got = rec(client_socket)
          if not got: continue
          login, password = got
          pr = find(login, password)
          #print(pr)
          snd(pickle.dumps(pr))

    elif command == 'get history':
          if ENABLE_OUTPUT: print("Working on \"get history\" command.....")
          snd(pickle.dumps("ok"))
          got = rec(client_socket)
          if not got: continue
          login, password = got
          if not find(login, password): snd(pickle.dumps(False))
          ret = return_history(login)
          send_many(len(ret), ret)

    elif command == 'delete history':
          if ENABLE_OUTPUT: print("Working on \"delete history\" command.....")
          snd(pickle.dumps("ok"))
          got = rec(client_socket)
          if not got: continue
          login, password = got
          ret = delete_history(login, password)
          snd(pickle.dumps(ret))

    elif command == 'stats':
      if ENABLE_OUTPUT: print("Working on \"stats\" command.....")
      snd(pickle.dumps('ok'))
      try:
        got = rec(client_socket)
        if not got: continue
        got, time_start, time_end, type = got
      except : continue
      if ENABLE_OUTPUT: print("Got request: ", got, time_start, time_end)
      ret = return_stats(got, time_start, time_end, type)
      send_many(len(ret), ret)

    elif command == 'add star':
      if ENABLE_OUTPUT: print("Working on \"add star\" command.....")
      snd(pickle.dumps("ok"))
      got = rec(client_socket)
      if not got: continue
      what, login, password = got
      add_star(what, login, password)
      
    elif command == 'remove star':
      if ENABLE_OUTPUT: print("Working on \"remove star\" command.....")
      snd(pickle.dumps("ok"))
      got = rec(client_socket)
      if not got: continue
      what, login, password = got
      remove_star(what, login, password)

    elif command == 'get stars':
      if ENABLE_OUTPUT: print("Working on \"get stars\" command.....")
      snd(pickle.dumps("ok"))
      got = rec(client_socket)
      if not got: continue
      login, password = got
      ret = get_stars(login, password)
      send_many(len(ret), ret)
    else:
      print("Unknown command.....")
      continue
  except ValueError as E:
    print("\n\nGUI failed:", E)
  conn.commit()
  conn1.commit()
  conn2.commit()
  conn3.commit()
  conn4.commit()
  conn5.commit()
  conn6.commit()
  conn7.commit()
  conn8.commit()
  if command == "process" or command == "mm_process":
    box_graph(got[3], 'buy', -69)
    calc_average(got[3], 'buy', -69)
    box_graph(got[3], 'sell', -69)
    calc_average(got[3], 'sell', -69)
  print(f"Request completed in {time.time() - start} seconds.....  {len(update())}")
