from datetime import timedelta
from sys import stdin

def get_microsec(date_str):
    partss = date_str.split('.')
    l = partss[0].split(':')
    return ((int(l[0])-1) * 3600 + int(l[1]) * 60 + int(l[2])) * 1000 * 10 + int(partss[1])

def encode_header(length, stream, timestamp):
    
    length_bytes = int(length).to_bytes(4, byteorder='big')
    stream_bytes = int(stream).to_bytes(2, byteorder='big')
    i = get_microsec(timestamp)
    timestamp_bytes = i.to_bytes(4, byteorder='big')

    return bytearray(
    [length_bytes[0], 
     length_bytes[1],
     length_bytes[2],
     length_bytes[3],
     stream_bytes[0],  
     stream_bytes[1],
     stream_bytes[2],
     stream_bytes[3],
     timestamp_bytes[0],  
     timestamp_bytes[1],
     timestamp_bytes[2],
     timestamp_bytes[3],
    ])


def decode_header(header):

     length = int.from_bytes(header[0:4], byteorder='big')
     stream =  int.from_bytes(header[4:8], byteorder='big')
     t = int.from_bytes(header[8:12], byteorder='big') * 100 + 3600000 * 1000
     time = str(timedelta(microseconds=t))
     if len(time) < 12:
         time += '.0000'
     else:
         time = time[:-2]
     if len(time) < 13:
         time = '0' + time



     return "length=" + length + " stream=" + str(stream) + " time=" + str(time)


def read_messages_from_pipe(chunk_size=12):
    while True:
        header = stdin.buffer.read(chunk_size)
        if header:
            int_val = int.from_bytes(header[0:4], byteorder='big')
            payload = stdin.buffer.read(int_val)
            yield header + payload
        else:
            break


#print(get_microsec("16:30:01.0001"))
#print(get_microsec("16:30:01.0000"))
