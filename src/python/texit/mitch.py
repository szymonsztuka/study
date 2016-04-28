import binascii

hex_val = "00 10 00 00"
byte_val = bytes.fromhex(hex_val)
int_val = int.from_bytes(byte_val, byteorder='little')

rev_byte_val = int_val.to_bytes(4, byteorder='little')
rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
rev_hex_val = " ".join(rev_hex_val_unspaced[i:i+2] for i in range(0, len(rev_hex_val_unspaced), 2))
rev_hex_val2 = ' '.join(hex(b)[2:] for b in rev_byte_val)


print("hex_val " + str(type(hex_val)) + " len=" + str(len(hex_val)))
print("byte_val " + str(type(byte_val)) + " " + str(byte_val) + " len=" + str(len(byte_val)))
print("int_val " + str(type(int_val)) + " " + str(int_val))
print("rev_byte_val " + str(type(rev_byte_val)) + " " + str(rev_byte_val) + " len=" + str(len(rev_byte_val)))
print("rev_hex_val_unspaced " + str(type(rev_hex_val_unspaced)) + " " + str(rev_hex_val_unspaced) + " len=" + str(len(rev_hex_val_unspaced)))
print("rev_hex_val " + str(type(rev_hex_val)) + " " + str(rev_hex_val) + " len=" + str(len(rev_hex_val)))
print("rev_hex_val2 " + str(type(rev_hex_val2)) + " " + str(rev_hex_val2) + " len=" + str(len(rev_hex_val2)))


def chunkfy(data):
    return " ".join(data[i:i+2] for i in range(0, len(data), 2))


def parse_integer(data, start, length):
    return int.from_bytes(data[start: start + length], byteorder='little')


def encode_integer(data, length):
    rev_byte_val = data.to_bytes(length,'little')
    rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
    return chunkfy(rev_hex_val_unspaced)


def parse_signed_integer(data, start, length):
    rest_byte = 0x7f & data[0]  # 127
    res = int.from_bytes(rest_byte.to_bytes(2, 'little') + data[start + 1: start + 1 + length], byteorder='little')
    if data[0] & 0x80 == 0:  # 128
        return res
    else:
        return - res


def parse_signed_integer2(data, start, length):
    last_byte_index = start + length - 1
    rest_byte = 0x7f & data[last_byte_index]  # 127
    res = int.from_bytes(data[start: last_byte_index], byteorder='little')
    result = (rest_byte << 8 * (length - 1)) + res
    if data[last_byte_index] & 0x80 == 0:  # 128
        return result
    else:
        return - result


def encode_signed_integer2(data, length):
    if data < 0:
       rev_byte_val = (-data).to_bytes(length, 'little')
       sign_byte = rev_byte_val[length - 1] | 0x80  # 128
       rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val[0:length - 1] + sign_byte.to_bytes(1, 'little'))).decode()
    else:
       rev_byte_val = data.to_bytes(length, 'little')
       rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
    return chunkfy(rev_hex_val_unspaced)


def parse_signed_integer3(data, start, length):
    res = int.from_bytes(data[start: start + length], byteorder='little')
    if data[0] & 0x80 == 0:  # 128
        return res & ((~(1 << 15)) & 0xffff)
    else:
        return - (res & (~(1 << 15) & 0xffff))


from datetime import datetime


def parse_time(data, start):
    """HH:MM:SS"""
    return datetime.strptime(data[start:start+8].decode(), '%H:%M:%S').time()


def encode_time(data):
    """HH:MM:SS"""
    return encode_alpha(data)


def parse_date(data, start):
    """YYYYMMDD"""
    return datetime.strptime(data[start:start+8].decode(), '%Y%m%d')


def encode_date(data):
    """YYYYMMDD"""
    return encode_alpha(data)


def parse_alpha(data, start, length):
    return data[start:start+length].decode()


def encode_alpha(data):
    return chunkfy(binascii.hexlify(data.encode()).decode())


def parse_byte(data, start):
    return data[start:start+1].decode()


def encode_byte(data):
    return binascii.hexlify(data.encode()).decode()


def parse_bitfield(data, start):
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

print(parse_integer(bytes.fromhex("00 10"),0,2))
print(parse_integer(bytes.fromhex("00 10 00 00"),0,4))

print(parse_signed_integer2(bytes.fromhex("87"),0,1))
print(parse_signed_integer2(bytes.fromhex("07"),0,1))
print(parse_signed_integer2(bytes.fromhex("07 80"),0,2))
print(parse_signed_integer2(bytes.fromhex("07 00"),0,2))
print(parse_signed_integer2(bytes.fromhex("07 00 00 80"),0,4))
print(parse_signed_integer2(bytes.fromhex("07 00 00 00"),0,4))
print(parse_signed_integer2(bytes.fromhex("6c 08 00 80"),0,4))
print(parse_signed_integer2(bytes.fromhex("6c 08 00 00"),0,4))

print(parse_bitfield(bytes.fromhex("e5"),0))

print(parse_byte(bytes.fromhex("53"),0))
print(parse_byte(bytes.fromhex("73"),0))

print(parse_date(bytes.fromhex("32 30 31 36 30 34 32 36"),0))
print(parse_date(bytes.fromhex("31 39 39 39 31 32 33 31"),0))
print(parse_time(bytes.fromhex("31 33 3a 32 38 3a 30 37"),0))

print(parse_alpha(bytes.fromhex("61 62 63 64 65 66 67 24 31 33 3f"),0,11))

print(encode_integer(4096,2))
print(encode_signed_integer2(-7,1))
print(encode_signed_integer2(7,1))
print(encode_signed_integer2(-7,2))
print(encode_signed_integer2(7,2))
print(encode_signed_integer2(-7,4))
print(encode_signed_integer2(7,4))
print(encode_signed_integer2(-2156,4))
print(encode_signed_integer2(2156,4))

print(encode_byte("S"))
print(encode_byte("s"))

print(encode_alpha("abcdefg$13?"))

print(encode_date("20160426"))
print(encode_date("19991231"))
print(encode_time("13:28:07"))

print(parse_signed_integer2(bytes.fromhex("00 e1 f5 05 00 00 00 80"),0,8))
print(encode_signed_integer2(-100000000,8))
print(parse_signed_integer2(bytes.fromhex("00 e1 f5 05 00 00 00 00"),0,8))
print(encode_signed_integer2(100000000,8))

print(parse_signed_integer2(bytes.fromhex("d0 50"),0,2))
print(parse_signed_integer2(bytes.fromhex("d0 d0"),0,2))
print(encode_signed_integer2(288,2))

print(parse_signed_integer2(bytes.fromhex("d0"),0,1)) #ok
print(parse_signed_integer2(bytes.fromhex("50"),0,1)) #ok

print(parse_signed_integer2(bytes.fromhex("00 d0"),0,2))
print(parse_signed_integer2(bytes.fromhex("00 50"),0,2)) # -> 20480

print(encode_signed_integer2(-20480,2))
print(encode_signed_integer2(20480,2))

x = 80
print( x << 8*(2-1))

print("bits")
print(encode_bitfield([1, 1, 1, 0, 0, 1, 0, 1]))
