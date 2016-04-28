from xml.dom import minidom
import binascii


def chunkfy(data):
    return " ".join(data[i:i+2] for i in range(0, len(data), 2))


def decode_integer(data, start, length):
    return int.from_bytes(data[start: start + length], byteorder='little')


def encode_integer(data, length):
    rev_byte_val = data.to_bytes(length, 'little')
    rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
    return chunkfy(rev_hex_val_unspaced)


def encode_UInt(length):
    def x(data):
        return encode_integer(int(data), length)
    return x

def decode_signed_integer_ver_1(data, start, length):
    rest_byte = 0x7f & data[0]  # 127
    res = int.from_bytes(rest_byte.to_bytes(2, 'little') + data[start + 1: start + 1 + length], byteorder='little')
    if data[0] & 0x80 == 0:  # 128
        return res
    else:
        return - res


def decode_signed_integer(data, start, length):
    last_byte_index = start + length - 1
    rest_byte = 0x7f & data[last_byte_index]  # 127
    res = int.from_bytes(data[start: last_byte_index], byteorder='little')
    result = (rest_byte << 8 * (length - 1)) + res
    if data[last_byte_index] & 0x80 == 0:  # 128
        return result
    else:
        return - result


def encode_signed_integer(data, length):
    if data < 0:
       rev_byte_val = (-data).to_bytes(length, 'little')
       sign_byte = rev_byte_val[length - 1] | 0x80  # 128
       rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val[0:length - 1] + sign_byte.to_bytes(1, 'little'))).decode()
    else:
       rev_byte_val = data.to_bytes(length, 'little')
       rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
    return chunkfy(rev_hex_val_unspaced)


def decode_signed_integer_ver_3(data, start, length):
    res = int.from_bytes(data[start: start + length], byteorder='little')
    if data[0] & 0x80 == 0:  # 128
        return res & ((~(1 << 15)) & 0xffff)
    else:
        return - (res & (~(1 << 15) & 0xffff))


from datetime import datetime


def decode_time(data, start):
    """HH:MM:SS"""
    return datetime.strptime(data[start:start+8].decode(), '%H:%M:%S').time()


def encode_time(data):
    """HH:MM:SS"""
    return encode_alpha(data)


def decode_date(data, start):
    """YYYYMMDD"""
    return datetime.strptime(data[start:start+8].decode(), '%Y%m%d')


def encode_date(data):
    """YYYYMMDD"""
    return encode_alpha(data)


def decode_alpha(data, start, length):
    return data[start:start+length].decode()


def encode_alpha(data):
    return chunkfy(binascii.hexlify(data.encode()).decode())


def decode_byte(data, start, length):
    return data[start:start+1].decode()


def encode_byte(data):
    return binascii.hexlify(data.encode()).decode()

def decode_bitfield(data, start):
    result = []
    for i in range(7, -1, -1):
        if data[start] & (1 << i) == 0:
            result.append('0')
        else:
            result.append('1')
    return result


def encode_bitfield(data):
    result = 0
    for i in data:
        result <<= 1
        result |= (i & 1)
    return encode_integer(result, 1)

#####################################################
#####################################################

def parse_alpha_with_length(length):
    def x(data, start):
        return decode_alpha(data, start, length)
    return x

def encode_price(length):
    def x(data):
        return encode_signed_integer(int(data), length)
    return x

#def encode_b(data):
#    rev_byte_val = ord(data).to_bytes(1, byteorder='little')
#    rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
#    return rev_hex_val_unspaced


doc = minidom.parse("level2-itchmarketdataspecification-5-1-230710.txt")
sizes = {"Alpha": 0, "BitField": 1, "Byte": 1, "Date": 8, "Time": 8, "Price": 8, "UInt8": 1, "UInt16": 2, "UInt32": 4,
        "UInt64": 8}
decoders = {"Alpha": decode_alpha, "BitField": decode_bitfield, "Byte": decode_byte, "Date": decode_date,
            "Time": decode_time, "Price": decode_signed_integer, "UInt8": decode_integer, "UInt16": decode_integer,
            "UInt32": decode_integer, "UInt64": decode_integer}
encoders = {"Alpha": encode_alpha, "BitField": encode_bitfield, "Byte": encode_byte, "Date": encode_date,
            "Time": encode_time,
            "Price": encode_price(8), "UInt8": encode_UInt(1), "UInt16": encode_UInt(2), "UInt32": encode_UInt(4),
            "UInt64": encode_UInt(8)}

msgs = doc.getElementsByTagName("msg")
message_handlers = dict()
for msg in msgs:
        print("%s %s" % (msg.getAttribute("msgtype"), msg.getAttribute("name")))
        fields = msg.getElementsByTagName("fld")
        field_handlers = []
        for field in fields:
            print("    %s / %s / %s  %s" % (field.getAttribute("datatype"), field.getAttribute("length"),
                                            field.getAttribute("decimal_points"), field.getAttribute("name")))
            field_size = sizes[field.getAttribute("datatype")]
            if field_size == 0:
                field_size = int(field.getAttribute("length"))
            field_handlers.append((field.getAttribute("name").replace(" ", ""),field.getAttribute("datatype"),
                                   field_size,encoders[field.getAttribute("datatype")],
                                   decoders[field.getAttribute("datatype")]))
        #print(hex(int(msg.getAttribute("msgtype"),16)))
        message_handlers[hex(int(msg.getAttribute("msgtype"),16))] = field_handlers


#print(size["Alpha"])



##handler = ("0x77": (field,field,files))
print("message_handlers")
print(message_handlers)

raw_msg = "0x50 ITCHNanosecond=UInt32 ITCHExecutedQuantity=UInt32 LSEITCHInstrumentID=UInt32 ITCHReserved1=Byte ITCHReserved2=Byte ITCHPrice=Price ITCHTradeID=UInt64 ITCHSideOfAggressor=Byte"
raw_msg = "0x50 ITCHNanosecond=123456 ITCHExecutedQuantity=1000 LSEITCHInstrumentID=13131313 ITCHReserved1=1 ITCHReserved2=1 ITCHPrice=380 ITCHTradeID=13131313 ITCHSideOfAggressor=1"

def parse_msg(data):
    fields = dict()
    elements = data.split()
    for e in elements[1:]:
        pair = e.split("=")
        fields[pair[0]] = pair[1]
    return(hex(int(elements[0],16)),fields)

#print(parse_msg(raw_msg))

obj = parse_msg(raw_msg)
handler = message_handlers[obj[0]]
#print("handler: " + str(type(obj[0])))
#print(handler)
print("\nencode:")
for msg_handler in handler:
    val = obj[1][msg_handler[0]] #
    print(val + " + " + msg_handler[1] + "  -> " + msg_handler[3](val))



hex_string_msg = "50 40 e2 01 00 e8 03 00 00 31 5e c8 00 31 31 7c 01 00 00 00 00 00 00 31 5e c8 00 00 00 00 00 31"

#progressing only parser
#print(hex_msg[0:2])
print("\ndecode:")
#key = decode_byte(      bytes.fromhex(hex_msg[0:2])    ,0)
msg_type = message_handlers["0x"+hex_string_msg[0:2]]
byte_msg = bytes.fromhex(hex_string_msg)

offset = 1
for msg_handler in msg_type:
    val = msg_handler[4](byte_msg,offset,msg_handler[2])
    print(chunkfy(binascii.hexlify(byte_msg[offset:offset+msg_handler[2]]).decode()) + " + "+msg_handler[1]+" -> " + str(val))
    offset += msg_handler[2]
