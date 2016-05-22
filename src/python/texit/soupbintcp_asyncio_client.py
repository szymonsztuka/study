#modificaation of http://stackoverflow.com/questions/30937042/asyncio-persisent-client-protocol-class-using-queue
import asyncio
import sys
import time

class SubscriberClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.transport = None
        self.loop = loop
        self.queue = asyncio.Queue()
        self._ready = asyncio.Event()
        self._timesend = time.time()
        asyncio.ensure_future(self._send_messages())
        asyncio.ensure_future(self._timer())

    @asyncio.coroutine
    def _send_messages(self):
        """ Send messages to the server as they become available. """
        yield from self._ready.wait()
        print("Ready!")
        while True:
            data = yield from self.queue.get()
            self.transport.write(data.encode('utf-8'))
            #print('Message sent: {!r}'.format(data))
            self._timesend = time.time()

    @asyncio.coroutine
    def _timer(self):
        """ Send messages to the server as they become available. """
        while True:
            yield from asyncio.sleep(1)
            if self._timesend + 0.9 <= time.time():
                diff = time.time() - self._timesend
                #self._timesend = time.time()
                yield from self.queue.put(str(diff)+"\n")

    def connection_made(self, transport):
        """ Upon connection send the message to the
        server

        A message has to have the following items:
            type:       subscribe/unsubscribe
            channel:    the name of the channel
        """
        self.transport = transport
        print("Connection made.")
        self._ready.set()

    @asyncio.coroutine
    def send_message(self, data):
        """ Feed a message to the sender coroutine. """
        yield from self.queue.put(data)

    def data_received(self, data):
        """ After sending a message we expect a reply
        back from the server

        The return message consist of three fields:
            type:           subscribe/unsubscribe
            channel:        the name of the channel
            channel_count:  the amount of channels subscribed to
        """
        print('Message received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

@asyncio.coroutine
def feed_messages(protocol):
    """ An example function that sends the same message repeatedly. """
    for line in sys.stdin:
        print(protocol)
        yield from protocol.send_message(line)
        from random import randint
        yield from asyncio.sleep(randint(0, 3000) / 1000.0)
    print("end of file")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: SubscriberClientProtocol(loop), '127.0.0.1', 10666)
    _, proto = loop.run_until_complete(coro)

    try:
        task = loop.create_task(feed_messages(proto))
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()