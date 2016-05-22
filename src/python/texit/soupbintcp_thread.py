import select
import time

#mysocket.setblocking(0)

#ready = select.select([mysocket], [], [], timeout_in_seconds)
#if ready[0]:
#    data = mysocket.recv(4096)

from queue import Queue
from threading import Thread
from random import randint

import sched, time
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    print("Doing stuf..", time.time()) #a floating point number expressed in seconds since the epoch
    sc.enter(1, 1, do_something, (sc,))

s.enter(1,1, do_something, (s,))
#s.run()

q = Queue()


def produce(q):
    j = 0
    while j < 100:
        i = randint(0, 1100)
        time.sleep(i / 1000.0)
        q.put(i)
        j +=1
    q.put(-1)

def back_info(connecton):
    print("Back Info")
    while True:
        print("await")
        try:
            data = connection.recv(100)
        except socket.error:
            print("no data yet..")
        print("receiver", data)
    print("End")

def do_stuff(q,connection):
    while True:
        try:
            r = q.get(block=True, timeout=1)
            q.task_done()
            if r == -1:
                connection.close()
                break
            print(r)

        except:
            print("nothing", time.time())
            r = -1
        connection.sendall((str(r)+"\n").encode())

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print ('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)
sock.listen(1)
print ('waiting for a connection', file=sys.stderr)
connection, client_address = sock.accept()

receiver =  Thread(target=back_info, args=(connection,))
worker = Thread(target=do_stuff, args=(q,connection,))
producer = Thread(target=produce, args=(q,))
receiver.start()
worker.start()
producer.start()

