def decode_integer(data, start, length):
    return data[start: start + length].lstrip('0')


def encode_integer(data, length):
    return data.zfill(length)


def decode_decimal(data, start, length):
    return decode_integer(data, start, length)


def encode_decimal(data, length):
    return encode_integer(data, length)

#string of binary integer -> integer
def decode_binary_integer(data, start, length):
    bytes_val = data[start: start + length].encode("utf-8")
    int_val = int.from_bytes(bytes_val, byteorder='big')
    return int_val

#int literal or int -> string of binary integer
def encode_binary_integer(data, length):
    int_val = int(data)
    bytes_val = (int_val).to_bytes(length, byteorder='big')
    string_val = bytes_val.decode("utf-8")
    return string_val


def decode_alpha(data, start, length):
    return data[start:start+length] if length != 0 else data[start:]


def encode_alpha(data, length):
    return data


def decode_blank(data, start, length):
    return None


def encode_blank(data, length):
    return "\00" * int(length)


utf8exit_handlers = {
    "ex1": (
        ("type", 3,  decode_alpha, encode_alpha),
        ("Rsv", 1, decode_blank, encode_blank),
        ("bin1", 4, decode_binary_integer, encode_binary_integer),
        ("bin4", 4, decode_binary_integer, encode_binary_integer),
        ("integer", 5, decode_integer, encode_integer),
        ("bin2", 4, decode_binary_integer, encode_binary_integer),
        ("ascii", 10, decode_alpha, encode_alpha),
    ),
}


type_from_tag_vals = lambda tag_values: tag_values.get("type")

type_from_value = lambda value: value[0:3]

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
        result = "".join(
            [field_handler[3](tag_values.get(field_handler[0]),field_handler[1]) for field_handler in handler])
        return result
    else:
        return None


def decode_msg_from_utf8string(handlers, type_decoder, value):
    type = type_decoder(value)
    if type in handlers:
        handler = handlers[type]
        result = ""
        offset = 0
        for field_handler in handler:
            val = field_handler[2](value, offset, field_handler[1])
            if val is not None:
                result += field_handler[0] + "=" + str(val).strip() + " "
            offset += field_handler[1]
        return result[:-1]
    else:
        return None

def dict_decode_msg_from_utf8string(handlers, type_decoder, value):
    type = type_decoder(value)
    x= dict()
    if type in handlers:
        handler = handlers[type]
        result = ""
        offset = 0
        for field_handler in handler:
            val = field_handler[2](value, offset, field_handler[1])
            if val is not None:
                x[field_handler[0]] = str(val).strip()
            offset += field_handler[1]
        return x
    else:
        return None
#i1 = 1407
#print(type(i1),i1)
#b1 = (i1).to_bytes(4, byteorder='big')
#print(type(b1),b1)
#s2 = b1.decode("utf-8")
#print("s2",type(s2),s2)
#b2 = s2.encode("utf-8")
#print(type(b2),b2)
#i2 = int.from_bytes(b2, byteorder='big')
#print(type(i2),i2)

#s= "0078.0"
#dec_s = decode_integer(s,0,len(s))
#enc_s= encode_integer(dec_s,6)
#print(dec_s)
#print(enc_s)

#s= "780"
#dec_s = decode_decimal(s,0,len(s))
#enc_s= encode_decimal(dec_s,6)
#print(dec_s)
#print(enc_s)


#sample ="type=ex1 bin1=1 bin2=45 bin4=65 integer=7.6 ascii=Simon"
#result = encode_msg_from_tag_vals(utf8exit_handlers, type_from_tag_vals, parse_msg(sample))
#print(result)
#print(result.encode("utf-8"))
#rev_result = decode_msg_from_utf8string(utf8exit_handlers, type_from_value, result)
#print(rev_result)



def lstrip_hex(data,offset,hex_count):
    for i in range(0,hex_count):
        if msg[offset] == '<':
            offset += 4
        else:
            offset +=1
    return data[offset:]

#msg ="<As>n<as>M<er><6y><ty><ty>o1TEXTTXTTEXTEXTETX"
#print(lstrip_hex(msg,0,9))


def parse_msg_with_spaces(data):
    fields = dict()
    elems = data.split()
    prec = ()
    for e in elems:
        pair = e.split("=")
        if len(pair) == 2:
            if len(prec) > 0:
                fields[prec[0]]=prec[1]
            prec = pair
        else:
            prec[1] = prec[1] + " " + pair[0]
    if len(prec) > 0:
        fields[prec[0]] = prec[1]
    return fields

# msg="abc=12 def=ala ma kota gh=323 h="
#print(parse_msg_with_spaces(msg))