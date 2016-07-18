from decimal import *
from sys import argv
import sys
import fep_message
import time
#import mitches.borsaitaliamitch_messages
#import mitches.eurotlxmitch_messages
#import mitches.jsemitch_messages
import mitches.lsemitch_messages
import mitches.mitch_fields
#import mitches.oslomitch_messages


class Mitchexit:

    def __init__(self, codec_name, ref_stream=None):
        self.ref_data_stream = int(ref_stream) if ref_stream is not None else None
        self.all_handlers = {"lsemitch": mitches.lsemitch_messages.messages,
                             #"oslomitch": mitches.oslomitch_messages.messages,
                             #"jsemitch": mitches.jsemitch_messages.messages,
                             #"borsaitaliamitch": mitches.borsaitaliamitch_messages.messages,
                             #"eurotlxmitch": mitches.eurotlxmitch_messages.messages
                             }
        self.handlers = self.all_handlers[codec_name]

    @staticmethod
    def parse_message(data):
        fields = dict()
        elements = data.split()
        last_pair = ""
        for e in elements:
            pair = e.split("=")
            if len(pair) > 1:
                fields[pair[0]] = pair[1]
                last_pair = pair[0]
            elif last_pair != "":
                fields[last_pair] = fields[last_pair] + " " + pair[0]
        return fields


    @staticmethod
    def encode_msg_from_tag_vals(handlers, type_decoder, tag_values):
        try:
            type_byte = type_decoder(tag_values)
            if type_byte in handlers:
                handler = handlers[type_byte]
                result = " ".join(
                    [field_handler[3](tag_values.get(field_handler[0]),field_handler[1]) for field_handler in handler])
                return result.upper()
            else:
                return None
        except ValueError:
            return None

    @staticmethod
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

    @staticmethod
    def decode_payload(handlers, type_decoder, binary_value):
        try:
            type_byte = type_decoder(binary_value) #  TODO needs to be INT
        except UnicodeDecodeError:
            print(binary_value)
        if type_byte in handlers:
            handler = handlers[type_byte]
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

    type_from_tag_vals = lambda tag_values: hex(int(tag_values.get("type")[:tag_values.get("type").index("(")], 16)) \
    if "type" in tag_values else hex(int("0x3B", 16))

    type_from_binary = lambda value: hex(ord(value[2:3].decode("ascii")))

    type_from_hex_string = lambda value: hex(int("0x" + value[3:5],16))

    @staticmethod
    def index_of_payload(line):
        start = line.find(" xxx=")
        if start >= 0:
            start = line.find(" ", start + 1) + 1
        return start

    @staticmethod
    def split_header_and_payload(line):
        payload_start = Mitchexit.index_of_payload(line)
        if payload_start >= 0:
            payload = line[payload_start:].rstrip()
            header = line[0:payload_start]
            return header, payload
        else:
            return None, None

    @staticmethod
    def encode_payload(payload, handlers):
        if 'type' in payload:
            msg = payload.rstrip()
            msg_tag_values = Mitchexit.parse_message(msg)
            hex_message = Mitchexit.encode_msg_from_tag_vals(handlers, Mitchexit.type_from_tag_vals, msg_tag_values)
            if hex_message is None:
                return None
            else:
                return bytearray.fromhex(hex_message.rstrip())

    header_tags = [" " + e + "=" for e in ["zzz", "yyy"]]

    #stream, sequence, payload_leng, time
    def get_metadata(self, header, encoded_payload, payload, timestamp=0):
        result = [int(header[offset + length: header.index(" ", offset + length)]) if offset >= 0 else '0' for offset, length in ((header.find(e), len(e)) for e in self.header_tags)] \
            + [len(encoded_payload), int(time.time()) if timestamp == 0 else timestamp]
        return result

    def encode_message(self, text):
        header, payload = Mitchexit.split_header_and_payload(text)
        #header_metadata = repari sequence/stream/etc
        encoded_payload = Mitchexit.encode_payload(payload, self.handlers)
        if encoded_payload is None:
            return None
        header_metadata = self.get_metadata(header, encoded_payload, payload)
        encoded_header = fep_message.encode_header(*header_metadata)
        return encoded_header + encoded_payload

    def decode_message(self, binary_val):
        superheader = fep_message.decode_header(binary_val)
        res = Mitchexit.decode_payload(self.handlers, Mitchexit.type_from_binary, binary_val[24:])
        return superheader + res

if __name__ == '__main__':
    codec = Mitchexit("lsemitch")
    for msg in fep_message.read_fep_messages_from_pipe():
        print(codec.decode_message(msg))
        
##############################################################

def parse_msg(data):
    fields = dict()
    elements = data.split()
    for e in elements:
        pair = e.split("=")
        print(pair)
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


def test_from_text_msg(schema, type_from_tag_vals, type_from_hex_string, text_message):
    msg_tag_values = parse_msg(text_message)
    hex_message = encode_msg_from_tag_vals(schema, type_from_tag_vals, msg_tag_values)
    print(text_message)
    print(hex_message)
    print(decode_msg_from_hex_string(schema, type_from_hex_string, hex_message))
    print("")

def test_from_hex_msg(schema, type_from_tag_vals, type_from_hex_string, hex_message):
    text_message = decode_msg_from_hex_string(schema, type_from_hex_string, hex_message)
    print(hex_message)
    print(text_message)
    msg_tag_values = parse_msg(text_message)
    print(encode_msg_from_tag_vals(schema, type_from_tag_vals, msg_tag_values))
    print("")

