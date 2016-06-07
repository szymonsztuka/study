#various sampls from stackoverflow

###### Sample 2
import asyncio

@asyncio.coroutine
def get_greeting(name):
    reader, writer = yield from asyncio.open_connection('', 9999)

    writer.write(name + b'\r\n')

    greeting = yield from reader.readline()
    return greeting

def sample1():
    loop = asyncio.get_event_loop()
    coro = get_greeting(b'World')
    greeting = loop.run_until_complete(coro)
    print(greeting)

###### Sample 2
import asyncio
import threading

queue = asyncio.Queue()

def threaded(loop):
    import time
    while True:
        time.sleep(1)
        loop.call_soon_threadsafe(queue.put_nowait, time.time())
        loop.call_soon_threadsafe(lambda: print(queue.qsize()))

@asyncio.coroutine
def async():
    while True:
        time = yield from queue.get()
        print(time)

def sample2():
    loop = asyncio.get_event_loop()
    asyncio.Task(async())
    threading.Thread(target=threaded,args=(loop,)).start()
    loop.run_forever()

sample2()


### Sample 3
## Modification of https://gist.github.com/gregvish/7665915
import asyncio

clients = []

class SimpleChatClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        print("connection_made: {}".format(self.peername), "{}".format(self.transport))
        clients.append(self)

    def data_received(self, data):
        print("data_received: {}".format(data.decode()))
        for client in clients:
            if client is not self:
                client.transport.write("{}: {}".format(self.peername, data.decode()).encode())

    def connection_lost(self, ex):
        print("connection_lost: {}".format(self.peername))
        clients.remove(self)

if __name__ == '__main__':
    print("starting up..")

    loop = asyncio.get_event_loop()
    coro = loop.create_server(SimpleChatClientProtocol, port=1234)
    coro2 = loop.create_server(SimpleChatClientProtocol, port=1235)
    server = loop.run_until_complete(coro)
    server2 = loop.run_until_complete(coro2)

    for socket in server.sockets:
        print("serving on {}".format(socket.getsockname()))
    for socket in server2.sockets:
        print("serving on {}".format(socket.getsockname()))

    loop.run_forever()
