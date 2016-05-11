#copied and modified from https://pymotw.com/2/socket/tcp.html
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print ('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)
sock.listen(1)

print ('waiting for a connection', file=sys.stderr)
connection, client_address = sock.accept()
try:
    print ( 'connection from', client_address, file=sys.stderr)
    for data in sys.stdin:
         print ('sending', file=sys.stderr)
         connection.sendall(data.encode())
    print ( 'no more data', client_address, file=sys.stderr)
finally:
    connection.close()