from xml.dom import minidom
import binascii
from decimal import *
from datetime import datetime

getcontext().prec = 8


def chunkfy(data):
    return " ".join(data[i:i+2] for i in range(0, len(data), 2))


def decode_integer(data, start, length):
    return int.from_bytes(data[start: start + length], byteorder='little')


def encode_integer(data, length):
    rev_byte_val = data.to_bytes(length, 'little')
    rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
    return chunkfy(rev_hex_val_unspaced)


def encode_uint(length):
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


def decode_bitfield(data, start, length):
    result = []
    for i in range(7, -1, -1):
        if data[start] & (1 << i) == 0:
            result.append('0')
        else:
            result.append('1')
    return result


def encode_bitfield(data):
    if data.startswith("0x"):
        return encode_integer(int(data,0),1)
    else:
        result = 0
        for i in data:
            result <<= 1
            result |= (i & 1)
        return encode_integer(result, 1)

#####################################################


def parse_alpha_with_length(length):
    def x(data, start):
        return decode_alpha(data, start, length)
    return x


def encode_price_from_string(data, length):
    dotIndex = data.find('.')
    if dotIndex < 0:
        data += "00000000"
    else:
        exiting = len(data)-dotIndex -1
        for i in range(0,8-exiting):
            data += "0"
        data = data[0:dotIndex] + data[dotIndex+1:]
    return encode_signed_integer(int(data), length)


def encode_price(length):
    def x(data):
        return encode_price_from_string(data, length)
    return x


def decode_price(decimals):
    def x(data, start, length):
        return float(Decimal(decode_signed_integer(data, start, length)/decimals))
    return x


#def encode_b(data):
#    rev_byte_val = ord(data).to_bytes(1, byteorder='little')
#    rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
#    return rev_hex_val_unspaced

#####################################################

def load_grammar(file):
    doc = minidom.parse(file)
    sizes = {"Alpha": 0, "BitField": 1, "Byte": 1, "Date": 8, "Time": 8, "Price": 8, "UInt8": 1, "UInt16": 2, "UInt32": 4,
        "UInt64": 8}
    decoders = {"Alpha": decode_alpha, "BitField": decode_bitfield, "Byte": decode_byte, "Date": decode_date,
            "Time": decode_time, "Price": decode_price(100000000), "UInt8": decode_integer, "UInt16": decode_integer,
            "UInt32": decode_integer, "UInt64": decode_integer}
    encoders = {"Alpha": encode_alpha, "BitField": encode_bitfield, "Byte": encode_byte, "Date": encode_date,
            "Time": encode_time,
            "Price": encode_price(8), "UInt8": encode_uint(1), "UInt16": encode_uint(2), "UInt32": encode_uint(4),
            "UInt64": encode_uint(8)}
    msgs = doc.getElementsByTagName("msg")
    message_handlers = dict()
    for msg in msgs:
        fields = msg.getElementsByTagName("fld")
        field_handlers = []
        for field in fields:
            #print("    %s / %s / %s  %s" % (field.getAttribute("datatype"), field.getAttribute("length"),
            #                                field.getAttribute("decimal_points"), field.getAttribute("name")))
            field_size = sizes[field.getAttribute("datatype")]
            if field_size == 0:
                field_size = int(field.getAttribute("length"))
            #if msg.getAttribute("name") in mitch_names_to_feprdr_names_map:
            #    name = mitch_names_to_feprdr_names_map[msg.getAttribute("name")][field.getAttribute("name")]
            #else:
            name = field.getAttribute("name")
            field_handlers.append((name,field.getAttribute("datatype"),
                                   field_size,encoders[field.getAttribute("datatype")],
                                   decoders[field.getAttribute("datatype")]))
        message_handlers[hex(int(msg.getAttribute("msgtype"),16))] = field_handlers
    return message_handlers


def parse_msg(data):
    fields = dict()
    elements = data.split()
    for e in elements[1:]:
        pair = e.split("=")
        fields[pair[0]] = pair[1]
    return hex(int(elements[0].split("=")[1],16)), fields


def encode_message(message_handlers, raw_msg):
    obj = parse_msg(raw_msg)
    if obj[0] in message_handlers:
        handler = message_handlers[obj[0]]
        result = str(obj[0][2:]) + " "
        for msg_handler in handler:
            if msg_handler[0] in obj[1]:
                val = obj[1][msg_handler[0]]
            else:
                val = "\00"
            result += msg_handler[3](val)
            result += " "
            length = (len(result) / 3) + 1
        return (hex(int(length))[2:].zfill(2) + " " + result[0:-1]).upper()
    else:
        return None


def decode_message(message_handlers, hex_string_msg):
    result = ""#hex_string_msg[0:2] + " + length -> " +  str(int.from_bytes(bytes.fromhex(hex_string_msg[0:2]), byteorder='little')) + "\n"
    result += "type=" + "0x" + hex_string_msg[3:5] + " "
    #print(message_handlers.keys())
    field_handlers = message_handlers["0x" + hex_string_msg[3:5]]
    byte_msg = bytes.fromhex(hex_string_msg)
    offset = 2
    for handler in field_handlers:
        val = handler[4](byte_msg, offset, handler[2])
        #result += (chunkfy(binascii.hexlify(byte_msg[offset:offset + handler[2]]).decode()) + " + " + handler[1] + " -> '" + str(val).strip()+ "'") + "\n"
        result += handler[0] + "=" + str(val).strip()+ "" + " "
        offset += handler[2]
    return result

#########################################################
mitch_names_to_new_names_map = {
     hex(int("0x41",16)): {
"ITCH Nanosecond":"Nanosecond",
"ITCH Order ID":"OrderID",
"ITCH Side":"Side",
"ITCH Quantity":"Quantity",
"LSE ITCH Instrument ID":"InstrumentID",
"ITCH Reserved 1": "Rsv1",
"ITCH Reserved 2": "Rsv2",
"ITCH Price":"Price",
"ITCH Flags":"Flags"},

    hex(int("0x46",16)): { #"ITCH Add Attributed Order"
"ITCH Nanosecond" : "Nanosec",
"ITCH Order ID" :"OrdID",
"ITCH Side" :"Side",
"ITCH Quantity" :"Quantity",
"LSE ITCH Instrument ID" :"InstrumentID",
"ITCH Reserved 1" :"Rsv1",
"ITCH Reserved 2" :"Rsv2",
"ITCH Price" :"Price",
"ITCH Attribution" :"Attribution",
"ITCH Flags" :"Flags"},

    hex(int("0x44",16)): { #"ITCH Order Deleted"
"ITCH Nanosecond" :"Nanosecond",
"ITCH Order ID" :"OrderID",
"ITCH Flags" :"Flags",
"InstID" : "InstID"},

    hex(int("0x55",16)): { #"ITCH Order Modified"
"ITCH Nanosecond" :"Nanosecond",
"ITCH Order ID" :"OrderID",
"ITCH New Quantity" :"NewQuantity",
"ITCH New Price" :"NewPrice",
"ITCH Flags" :"Flags"},

    hex(int("0x79",16)): { #"ITCH Order Book Clear"
"ITCH Nanosecond": "Nanosecond",
"LSE ITCH Instrument ID" : "InstrumentID" ,
"ITCH Reserved 1": "Rsv1",
"ITCH Reserved 2": "Rsv2",
"ITCH Flags" : "Flags"},

    hex(int("0x54",16)): {#"ITCH Time"
"ITCH Seconds": "Secs"},

    hex(int("0x45",16)): { #"ITCH Order Executed"
"ITCH Nanosecond":"Nanosecond",
"ITCH Order ID": "OrderID",
"ITCH Executed Quantity": "ExecutedQuantity",
"ITCH Trade ID": "TradeID"},

    hex(int("0x43",16)): { #"ITCH Order Executed With Price"
"ITCH Nanosecond" : "Nanosecond",
"ITCH Order ID" : "OrderID",
"ITCH Executed Quantity" : "ExecutedQuantity",
"ITCH Display Quantity" : "DisplayQuantity",
"ITCH Trade ID" : "TradeID",
"ITCH Printable" : "Printable",
"ITCH Price" : "Price" }
}


def apply_name_convention_for_fields(message_handlers, mitch_names_to_new_names_map):
    new_dict = dict()
    for key, value in message_handlers.items():
        if key in mitch_names_to_new_names_map:
            new_values = []
            for e in value:
                new_values.append([mitch_names_to_new_names_map[key][e[0]], *e[1:]])
            new_dict[key] = new_values
    return new_dict

#message_handlers = apply_name_convention_for_fields(load_grammar("level2-itchmarketdataspecification-5-1-230710.txt"),mitch_names_to_new_names_map)
#print(message_handlers)
#print(encode_message(message_handlers, "Type=0x79 Nanosecond=034344000 InstrumentID=21472 Flags=0x00"))
#print(" ")
#print(decode_message(message_handlers, "0D 79 40 0C 0C 02 E0 53 00 00 00 00 00"))
