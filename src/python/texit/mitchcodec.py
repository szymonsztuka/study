import binascii
from decimal import *
from datetime import datetime

getcontext().prec = 8


def chunkfy(data):
    return " ".join(data[i:i+2] for i in range(0, len(data), 2))


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
        rev_hex_val_unspaced = binascii.hexlify(
            bytearray(rev_byte_val[0:length - 1] + sign_byte.to_bytes(1, 'little'))).decode()
    else:
        rev_byte_val = data.to_bytes(length, 'little')
        rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
    return chunkfy(rev_hex_val_unspaced)


def decode_integer(data, start, length):
    return int.from_bytes(data[start: start + length], byteorder='little')


def encode_integer(data, length):
    rev_byte_val = int(data).to_bytes(length, 'little')
    rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
    return chunkfy(rev_hex_val_unspaced)


def decode_alpha(data, start, length):
    return data[start:start+length].decode()


def encode_alpha(data, length):
    return chunkfy(binascii.hexlify(data.encode()).decode())


def decode_quoted_alpha(data, start, length):
    return "'" + decode_alpha(data, start, length) + "'"


def encode_quoted_alpha(data, length):
    return encode_alpha(data[1:-1], length)


def decode_annotated_hex(description):
    def decode_annotated_hex_internal(data, start, length):
        return decode_hex(data, start, length) + "/" + description
    return decode_annotated_hex_internal


def encode_annotated_hex(data, length):
    return data[2:data.index("/")]


def decode_hex(data, start, length):
    return "0x" + binascii.hexlify(data[start:length+start]).decode()


def decode_blank(data, start, length):
    return None


def encode_blank(data, length):
    x = "00 " * int(length)
    return x[:-1]


def decode_bitfield(data, start, length):
    result = []
    for i in range(7, -1, -1):
        if data[start] & (1 << i) == 0:
            result.append('0')
        else:
            result.append('1')
    return result


def encode_bitfield(data, length):
    if data.startswith("0x"):
        return encode_integer(int(data,0),1)
    else:
        result = 0
        for i in data:
            result <<= 1
            result |= (i & 1)
        return encode_integer(result, 1)


def decode_annotated_bitfield(decorators):
    def decode_annotated_bitfield_inner(data, start, length):
        bit_array = decode_bitfield(data, start, length)
        return "0" + str(data[start:start+length])[3:-1] + "/" \
               + ",".join([elem[1] + "=" + bit_array[elem[0] - 1] for elem in decorators])
    return decode_annotated_bitfield_inner


def encode_annotated_bitfield(data, length):
    if "/" in data:
        data = data[:data.index("/")]
    return encode_bitfield(data, length)


def decode_price(implied_precision):
    def decode_price_inner(data, start, length):
        division = 10 ** implied_precision
        return "%0.8f" % float(Decimal(decode_signed_integer(data, start, length)/division))  # TODO pretty print 8 is hardcoded
    return decode_price_inner


def encode_price(implied_precision):
    def encode_price_inner(data, length):
        dot_index = data.find('.')
        if dot_index < 0:
            data += ("0"*implied_precision)
        else:
            exiting = len(data) - dot_index - 1
            for i in range(0,implied_precision-exiting):
                data += "0"
            data = data[0: dot_index] + data[dot_index + 1:]
        return encode_signed_integer(int(data), length)
    return encode_price_inner


##############################################################

def parse_msg(data):
    fields = dict()
    elements = data.split()
    for e in elements:
        pair = e.split("=")
        fields[pair[0]] = pair[1]
    return fields

def encode_msg_from_tag_vals(handlers, type_decoder, tag_values):
    type_byte = type_decoder(tag_values)
    if type_byte in handlers:
        handler = handlers[type_byte]
        result = " ".join(
            [field_handler[3](tag_values.get(field_handler[0]),field_handler[1]) for field_handler in handler])
        length = int((len(result) / 3) + 2)  # TODO move outside to IR as a tag length ?
        return (hex(length)[2:].zfill(2) + " " + result).upper()
    else:
        return None

def decode_msg_from_hex_strig(handlers, type_decoder, value):
    type_byte = type_decoder(value)
    binary_value = bytes.fromhex(value)
    if type_byte in handlers:
        handler = handlers[type_byte]
        result = ""
        offset = 1  # TODO process length as normal tag (add to IR)?
        for field_handler in handler:
            val = field_handler[2](binary_value, offset, field_handler[1])
            if val is not None:
                result += field_handler[0] + "=" + str(val).strip() + " "
            offset += field_handler[1]
        return result
    else:
        return None

######################################################

# http://www.londonstockexchange.com/products-and-services/millennium-exchange/technicalinformation/technicalinformation.htm
mitch_handlers_1 = {
    hex(int("0x41", 16)): (
        #"length": "length",
        ("type", 1, decode_annotated_hex("AddOrder"), encode_annotated_hex),
        ("Nanosecond",),
        ("OrderID",),
        ("Side",),
        ("Quantity",),
        ("InstrumentID",),
        ("Rsv1",),
        ("Rsv2",),
        ("Price",),
        ("Flags", 1, decode_annotated_bitfield({(1, "bit1")}), encode_annotated_bitfield)
    ),
    hex(int("0x46", 16)): (
        #"length": "length",
        ("type", 1, decode_annotated_hex("AddAttributedOrder"), encode_annotated_hex),
        ("Nanosecond",),
        ("OrdID",),
        ("Side",),
        ("Quantity",),
        ("InstrumentID",),
        ("Rsv1",),
        ("Rsv2",),
        ("Price",),
        ("Attribution",),
        ("Flags", 1, decode_annotated_bitfield({(2, "bit2"), (3, "bit3")}), encode_annotated_bitfield)
    ),
    hex(int("0x44", 16)): (
        #"length": "length",
        ("type", 1, decode_annotated_hex("OrderDeleted"), encode_annotated_hex),
        ("Nanosecond",),
        ("OrderID",),
        ("Flags", 1, decode_annotated_bitfield({(4, "bit4")}), encode_annotated_bitfield),
        ("InstID",),
    ),
    hex(int("0x55", 16)): (
        #"length": "length",
        ("type", 1, decode_annotated_hex("OrderModified"), encode_annotated_hex),
        ("Nanosecond",),
        ("OrderID",),
        ("NewQuantity",),
        ("NewPrice",),
        ("Flags", 1, decode_annotated_bitfield({(0, "bit0"), (5, "bit5")}), encode_annotated_bitfield)
    ),
    hex(int("0x79", 16)): (
        #"length": "length",
        ("type", 1, decode_annotated_hex("OrderBookClear"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("InstrumentID", 4, decode_integer, encode_integer),
        ("Rsv1", 2, decode_blank, encode_blank),
        ("Flags", 1, decode_annotated_bitfield({(5, "bit5")}), encode_annotated_bitfield),
    ),
    hex(int("0x54", 16)): (
        #"length": "length",
        ("type", 1, decode_annotated_hex("Time"), encode_annotated_hex),
        ("ITCH Seconds", "Secs")
    ),
    hex(int("0x45", 16)): (  # "ITCH Order Executed"
        #"length": "length",
        ("type", 1, decode_annotated_hex("OrderExecuted"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("ExecutedQuantity", 8, decode_integer, encode_integer),
        ("TradeID", 8, decode_integer, encode_integer)
    ),
    hex(int("0x43", 16)): (
        #"length": "length",
        ("type", 1, decode_annotated_hex("OrderExecutedWithPrice"), encode_annotated_hex),
        ("Nanosecond",),
        ("OrderID",),
        ("ExecutedQuantity",),
        ("DisplayQuantity",),
        ("TradeID",),
        ("Printable",),
        ("Price",)
    )
}

#http://www.oslobors.no/ob_eng/Oslo-Boers/Trading/Trading-systems/Millennium-Exchange/Technical-documentation
mitch_handlers_2 = {
    hex(int("0x41", 16)): (
        # ("length", "byte"),
        ("type", 1, decode_annotated_hex("AddOrder"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("Side", 1, decode_quoted_alpha, encode_quoted_alpha),
        ("Quantity", 8, decode_integer, encode_integer),
        ("InstrumentID", 4, decode_integer, encode_integer),
        ("Rsv1", 2, decode_blank, encode_blank),
        ("Price", 8, decode_price(8), encode_price(8)),  # 8 decimal points
        ("Flags", 1, decode_annotated_bitfield({(1, "bit1")}), encode_annotated_bitfield),
        ("Rsv2", 8, decode_blank, encode_blank)
    )
}


type_from_tag_vals = lambda tag_values: hex(int(tag_values.get("type")[:tag_values.get("type").index("/")], 16))
type_from_hex_string = lambda value: hex(int("0x" + value[3:5],16))

######################################

def test_from_text_msg(schema, text_message):
    print(schema)
    msg_tag_values = parse_msg(text_message)
    hex_message = encode_msg_from_tag_vals(schema, type_from_tag_vals, msg_tag_values)
    print(text_message)
    print(hex_message)
    print(decode_msg_from_hex_strig(schema, type_from_hex_string, hex_message))
    print("")


test_from_text_msg(mitch_handlers_1, "type=0x79/OrderBookClear Nanosecond=34344000 InstrumentID=21472 Flags=0x08/bit5=1")

test_from_text_msg(mitch_handlers_2, "type=0x41/AddOrder Nanosecond=1 OrderID=2 Side='B' Quantity=34 InstrumentID=4 Price=5.00000000 Flags=0x01/bit1=0")