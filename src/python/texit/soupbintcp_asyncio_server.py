#modificaation of http://stackoverflow.com/questions/30937042/asyncio-persisent-client-protocol-class-using-queue
import asyncio
import sys
import time

class SubscriberServerProtocol(asyncio.Protocol):
    """ A Server Protocol listening for subscriber messages """

    def __init__(self,queue):
        print("new")
        self.transport = None
        print(queue)
        self.queue = queue
        self._ready = asyncio.Event()
        self._timesend = time.time()
        self._timereceived = time.time()
        asyncio.ensure_future(self._send_messages())
        asyncio.ensure_future(self._timer())
        asyncio.ensure_future(self._feed_messages_from_pipe())

    def connection_made(self, transport):
        """ Called when connection is initiated """

        self.peername = transport.get_extra_info('peername')
        print('connection from {}'.format(self.peername))
        self.transport = transport
        self._timereceived = time.time()
        self._ready.set()

    def data_received(self, data):
        """ The protocol expects a json message containing
        the following fields:

            type:       subscribe/unsubscribe
            channel:    the name of the channel

        Upon receiving a valid message the protocol registers
        the client with the pubsub hub. When succesfully registered
        we return the following json message:

            type:           subscribe/unsubscribe/unknown
            channel:        The channel the subscriber registered to
            channel_count:  the amount of channels registered
        """

        # Receive a message and decode the json output
        send_message = data.decode()
        print('Sending {!r}'.format(send_message))
        #self.transport.write(send_message.encode())
        self._timereceived = time.time()

    def eof_received(self):
        """ an EOF has been received from the client.

        This indicates the client has gracefully exited
        the connection. Inform the pubsub hub that the
        subscriber is gone
        """
        print('Client {} closed connection'.format(self.peername))
        self.transport.close()

    def connection_lost(self, exc):
        """ A transport error or EOF is seen which
        means the client is disconnected.

        Inform the pubsub hub that the subscriber has
        Disappeared
        """
        if exc:
            print('{} {}'.format(exc, self.peername))

    @asyncio.coroutine
    def _timer(self):
        """ Send messages to the server as they become available. """
        while True:
            yield from asyncio.sleep(1)
            if self._timesend + 1 <= time.time():
                diff = time.time() - self._timesend
                yield from self.queue.put(str(diff)+"\n")
            if self._timereceived + 1 < time.time():
                diff = time.time() - self._timereceived
                print("late" + str(diff))

    @asyncio.coroutine
    def _send_messages(self):
        """ Send messages to the server as they become available. """
        yield from self._ready.wait()
        print("Ready!")
        while True:
            data = yield from self.queue.get()
            self.transport.write(data.encode('utf-8'))
            # print('Message sent: {!r}'.format(data))
            self._timesend = time.time()

    @asyncio.coroutine
    def _feed_messages_from_pipe(self):
        """ An example function that sends the same message repeatedly. """
        for line in sys.stdin:
            yield from self.queue.put(line)
            from random import randint
            yield from asyncio.sleep(randint(0, 3000) / 1000.0)
        print("end of file")


loop = asyncio.get_event_loop()
queue = asyncio.Queue()
# Each client will create a new protocol instance
coro = loop.create_server(lambda: SubscriberServerProtocol(queue), '127.0.0.1', 10666)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
try:
    server.close()
    loop.until_complete(server.wait_closed())
    loop.close()
except:
    pass