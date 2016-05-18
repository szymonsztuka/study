#source: https://pymotw.com/2/socket/udp.html
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 33001)
message = 'This is the message.  It will be repeated.\n'

try:
    for i in range(0,10):
        # Send data
        print ( 'sending "%s"' % message, file=sys.stderr)
        sent = sock.sendto(message.encode(), server_address)

    # Receive response
    #print ( 'waiting to receive', file=sys.stderr)
    #data, server = sock.recvfrom(4096)
    #print ( 'received "%s"' % data, file=sys.stderr)

finally:
    print ( 'closing socket', file=sys.stderr)
    sock.close()