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
    if length != 0:
        return data[start:start+length].decode()
    else:
        return data[start:].decode()

def encode_alpha(data, length):
    payload = binascii.hexlify(data.encode()).decode()
    #if len(payload)<2*length:
        #print("00" * (length - int(len(payload)/2 )))
    payload += ("00" * (length - int(len(payload)/2)) )
    return chunkfy(payload)


def decode_quoted_alpha(data, start, length):
    return "'" + decode_alpha(data, start, length).strip('\0')+ "'"


def encode_quoted_alpha(data, length):
    return encode_alpha(data[1:-1], length)


def decode_annotated_hex(description):
    def decode_annotated_hex_internal(data, start, length):
        return decode_hex(data, start, length) + "/" + description
    return decode_annotated_hex_internal


def encode_annotated_hex(data, length):
    return data[2:data.index("/")]


def encode_const_integer(val):
    def encode_const_integer_internal(data, length):
        return encode_integer(val,1)
    return encode_const_integer_internal


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
        return "0x" + binascii.hexlify(bytearray(data[start:start+length])).decode() \
               + "/" \
               + ",".join([elem[1] + "=" + bit_array[elem[0] - 1] for elem in decorators])
    return decode_annotated_bitfield_inner


def encode_annotated_bitfield(data, length):
    if "/" in data:
        data = data[:data.index("/")]
    return encode_bitfield(data, length)


def decode_price(implied_precision):
    def decode_price_inner(data, start, length):
        division = 10 ** implied_precision
        format = "%0." + str(implied_precision) + "f"  # TODO cache formats
        return format % float(Decimal(decode_signed_integer(data, start, length)/division))
    return decode_price_inner


def encode_price(implied_precision):
    def encode_price_inner(data, length):
        dot_index = data.find('.')
        if dot_index < 0:
            data += ("0" * implied_precision)
        else:
            exiting = len(data) - dot_index - 1
            for i in range(0, implied_precision - exiting):
                data += "0"
            if implied_precision - exiting < 0:
                data = data[0: dot_index] + data[dot_index + 1:implied_precision - exiting]
            else:
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
        return result.upper()
    else:
        return None


def encode_all(handlers, type_decoder, tag_values):
    return encode_msg_from_tag_vals(handlers, type_decoder, tag_values)


def decode_msg_from_hex_string(handlers, type_decoder, value):
    type_byte = type_decoder(value)
    if type_byte in handlers:
        handler = handlers[type_byte]
        binary_value = bytes.fromhex(value)
        result = ""
        offset = 0
        for field_handler in handler:
            val = field_handler[2](binary_value, offset, field_handler[1])
            if val is not None:
                result += field_handler[0] + "=" + str(val).strip() + " "
            offset += field_handler[1]
        return result[:-1]
    else:
        return None

######################################################

# http://www.londonstockexchange.com/products-and-services/millennium-exchange/technicalinformation/technicalinformation.htm
mitch_handlers_1 = {
    hex(int("0x41", 16)): (
        ("length", 1, decode_blank, encode_const_integer(34)),
        ("type", 1, decode_annotated_hex("AddOrder"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("Side", 1, decode_quoted_alpha, encode_quoted_alpha),
        ("Quantity", 8, decode_integer, encode_integer),
        ("InstrumentID", 4, decode_integer, encode_integer),
        ("Rsv", 2, decode_blank, encode_blank),
        ("Price", 8, decode_price(8), encode_price(8)),  # 8 decimal points
        ("Flags", 1, decode_annotated_bitfield({(1, "bit1")}), encode_annotated_bitfield)
    ),
    hex(int("0x42", 16)): (
        ("length", 1, decode_blank, encode_const_integer(19)),
        ("type", 1, decode_annotated_hex("TradeBreak"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("TradeID", 8, decode_integer, encode_integer),
        ("TradeType", 1, decode_quoted_alpha, encode_quoted_alpha),
        ("InstrumentID", 4, decode_integer, encode_integer),
    ),
    hex(int("0x43", 16)): (
        ("length", 1, decode_blank, encode_const_integer(39)),
        ("type", 1, decode_annotated_hex("OrderExecutedWithPrice"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("ExecutedQuantity", 4, decode_integer, encode_integer),
        ("DisplayQuantity", 4, decode_integer, encode_integer),
        ("TradeID", 8, decode_integer, encode_integer),
        ("Printable", 1, decode_quoted_alpha, encode_quoted_alpha),
        ("Price", 8, decode_price(8), encode_price(8)),  # 8 decimal points
    ),
    hex(int("0x44", 16)): (
        ("length", 1, decode_blank, encode_const_integer(19)),
        ("type", 1, decode_annotated_hex("OrderDeleted"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("Flags", 1, decode_annotated_bitfield({(4, "bit4")}), encode_annotated_bitfield),
        ("InstrumentID", 4, decode_integer, encode_integer),
    ),
    hex(int("0x45", 16)): (
        ("length", 1, decode_blank, encode_const_integer(26)),
        ("type", 1, decode_annotated_hex("OrderExecuted"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("ExecutedQuantity", 4, decode_integer, encode_integer),
        ("TradeID", 8, decode_integer, encode_integer)
    ),
    hex(int("0x46", 16)): (
        ("length", 1, decode_blank, encode_const_integer(45)),
        ("type", 1, decode_annotated_hex("AddAttributedOrder"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("Side", 1, decode_quoted_alpha, encode_quoted_alpha),
        ("Quantity", 8, decode_integer, encode_integer),
        ("InstrumentID", 4, decode_integer, encode_integer),
        ("Rsv", 2, decode_blank, encode_blank),
        ("Price", 8, decode_price(8), encode_price(8)),  # 8 decimal points
        ("Attribution", 11, decode_quoted_alpha, encode_quoted_alpha),
        ("Flags", 1, decode_annotated_bitfield({(2, "bit2"), (3, "bit3")}), encode_annotated_bitfield)
    ),
    hex(int("0x47", 16)): (
        ("length", 1, decode_blank, encode_const_integer(32)),
        ("type", 1, decode_annotated_hex("SymbolStatus"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("InstrumentID", 8, decode_integer, encode_integer),
        ("Rsv", 2, decode_blank, encode_blank),
        ("TradingStatus", 1, decode_quoted_alpha, encode_quoted_alpha),
        ("Flags", 1, decode_annotated_bitfield({(5, "bit5")}), encode_annotated_bitfield),
        ("HaltReason", 4, decode_quoted_alpha, encode_quoted_alpha),
        ("SessionChangeReason", 1, decode_integer, encode_integer),
        ("NewEndTime", 8, decode_quoted_alpha, encode_quoted_alpha),
        ("BookType", 1, decode_integer, encode_integer),
    ),
    hex(int("0x54", 16)): (
        ("length", 1, decode_blank, encode_const_integer(6)),
        ("type", 1, decode_annotated_hex("Time"), encode_annotated_hex),
        ("Seconds", 4, decode_integer, encode_integer),
    ),
    hex(int("0x55", 16)): (
        ("length", 1, decode_blank, encode_const_integer(27)),
        ("type", 1, decode_annotated_hex("OrderModified"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("NewQuantity", 4, decode_integer, encode_integer),
        ("NewPrice", 8, decode_price(8), encode_price(8)),  # 8 decimal points
        ("Flags", 1, decode_annotated_bitfield({(0, "bit0"), (5, "bit5")}), encode_annotated_bitfield)
    ),
    hex(int("0x79", 16)): (
        ("length", 1, decode_blank, encode_const_integer(13)),
        ("type", 1, decode_annotated_hex("OrderBookClear"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("InstrumentID", 4, decode_integer, encode_integer),
        ("Rsv", 2, decode_blank, encode_blank),
        ("Flags", 1, decode_annotated_bitfield({(5, "bit5")}), encode_annotated_bitfield),
    ),
    hex(int("0x3B", 16)): (
        ("auxiliary", 0, decode_quoted_alpha, encode_quoted_alpha),
    )
}

#http://www.oslobors.no/ob_eng/Oslo-Boers/Trading/Trading-systems/Millennium-Exchange/Technical-documentation
mitch_handlers_2 = {
    hex(int("0x41", 16)): (
        ("length", 1, decode_blank, encode_const_integer(46)),
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

#https://www.jse.co.za/services/technologies/equity-market-trading-and-information-technology-change
mitch_handlers_3 = {

}
type_from_tag_vals = lambda tag_values: hex(int(tag_values.get("type")[:tag_values.get("type").index("/")], 16)) \
    if "type" in tag_values else hex(int("0x3B", 16))
type_from_hex_string = lambda value: hex(int("0x" + value[3:5],16))

######################################

def test_from_text_msg(schema, type_from_tag_vals, type_from_hex_string, text_message):
    msg_tag_values = parse_msg(text_message)
    hex_message = encode_all(schema, type_from_tag_vals, msg_tag_values)
    print(text_message)
    print(hex_message)
    print(decode_msg_from_hex_string(schema, type_from_hex_string, hex_message))
    print("")

def test_from_hex_msg(schema, type_from_tag_vals, type_from_hex_string, hex_message):
    text_message = decode_msg_from_hex_string(schema, type_from_hex_string, hex_message)
    print(hex_message)
    print(text_message)
    msg_tag_values = parse_msg(text_message)
    print(encode_all(schema, type_from_tag_vals, msg_tag_values))
    print("")

