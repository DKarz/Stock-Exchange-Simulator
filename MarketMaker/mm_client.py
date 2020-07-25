import socket
import pickle
import time

global key
key = 'c35312fb3a7e05b7a44db2326bd29040'

IP = "127.0.0.1"
PORT = 1234

def rec(client_socket):
  start = time.time()
  while True:
    if time.time()-start >= 1:
        print("Too much time wasted.....")
        return False
    try:
      temp = pickle.loads(client_socket.recv(1024))
      return temp
    except Exception as exception:
      pass


def process(req, login):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    command = 'mm_process'
    client_socket.send(pickle.dumps(command))
    rec(client_socket)
    client_socket.send(pickle.dumps([req, login, key]))
    re = rec(client_socket)
    client_socket.close()
    return re

def delete(login, id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    command = 'delete'
    client_socket.send(pickle.dumps(command))
    rec(client_socket)
    client_socket.send(pickle.dumps([login, id]))
