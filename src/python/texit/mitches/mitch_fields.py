import binascii
from decimal import *
from datetime import datetime

#getcontext().prec = 8


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
        if '' == data:
            data = '0'
        rev_byte_val = int(data).to_bytes(length, 'little')
        rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
        return chunkfy(rev_hex_val_unspaced)


def decode_alpha(data, start, length):
        if length != 0:
            #try:
            return data[start:start+length].decode()
        else:
            try:
                x = data[start:].decode()
                return x
            except UnicodeDecodeError:
                return data[start:].decode("ISO-8859-1")

def encode_alpha(data, length):
        payload = binascii.hexlify(data.encode()).decode()
        #if len(payload)<2*length:
            #print("00" * (length - int(len(payload)/2 )))
        payload += ("00" * (length - int(len(payload)/2)) )
        return chunkfy(payload)


def encode_quoted_alpha_with_spaces(data, length):
        payload = binascii.hexlify(data[1:-1].encode()).decode()
        #if len(payload)<2*length:
            #print("00" * (length - int(len(payload)/2 )))
        payload += ("20" * (length - int(len(payload)/2)) )
        return chunkfy(payload)


def decode_quoted_alpha_with_spaces(data, start, length):
        return "'" + decode_alpha(data, start, length).rstrip(' ') + "'"


def decode_quoted_alpha(data, start, length):
        #print(data, "|", start, "|",length)
        return "'" + decode_alpha(data, start, length).strip('\0').rstrip(' ') + "'"


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
            return encode_integer(val,length)
        return encode_const_integer_internal


def decode_hex(data, start, length):
        return "0x" + binascii.hexlify(data[start:length+start]).decode()


def decode_blank(data, start, length):
        return None


def encode_blank(data, length):
        x = "00 " * int(length)
        return x[:-1]


def encode_blank_spaces(data, length):
        x = "20 " * int(length)
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
