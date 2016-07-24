from sys import argv
import mitches.borsaitaliamitch_messages
import mitches.eurotlxmitch_messages
import mitches.jsemitch_messages
import mitches.lsegtp_messages
import mitches.lsemitch_messages
import mitches.mitch_fields
import mitches.oslomitch_messages

class MitchCodec:

    def __init__(self, codec_name, ref_stream=None):
        self.ref_data_stream = int(ref_stream) if ref_stream is not None else None
        self.all_handlers = {"lsegtp": mitches.lsegtp_messages.messages,
                             "lsemitch": mitches.lsemitch_messages.messages,
                             "osloitch": mitches.oslomitch_messages.messages,
                             "jseitch": mitches.jsemitch_messages.messages,
                             "borsaitaliaitch": mitches.borsaitaliamitch_messages.messages,
                             "eurotlx": mitches.eurotlxmitch_messages.messages
                             }
        if "lsegtp" == codec_name:
            self.type_from_binary = lambda value: hex(ord(value[1:2].decode("ascii"))) if value[1:2] == b'\x3B' else hex(ord(value[2:3].decode("ascii")))
        else:
            self.type_from_binary = lambda value: hex(ord(value[1:2].decode("ascii")))

        self.type_from_tag_vals = lambda tag_values: hex(int(tag_values.get("type")[:tag_values.get("type").index("(")], 16)) \
            if "MsgType" in tag_values else hex(int("0x3B", 16))
        self.handlers = self.all_handlers[codec_name]

    def decode_from_hex_string(self, value):
        type_decoder = lambda value: hex(int("0x" + value[3:5],16))
        type_byte = type_decoder(value)
        if type_byte in self.handlers:
            handler = self.handlers[type_byte]
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

    def encode(self, tag_values):
        try:
            type_byte = self.type_from_tag_vals(tag_values)
            if type_byte in self.handlers:
                handler = self.handlers[type_byte]
                result = " ".join([field_handler[3](tag_values.get(field_handler[0]), field_handler[1]) for field_handler in handler])
                #print("result", result)
                return bytearray.fromhex(result.rstrip().upper())
            else:
                return None
        except ValueError:
            return None

    def decode(self, binary_value):
        try:
            type_byte = self.type_from_binary(binary_value)
        except UnicodeDecodeError:
            print(binary_value)
        if type_byte in self.handlers:
            handler = self.handlers[type_byte]
            result = ""
            offset = 0
            for field_handler in handler:
                val = field_handler[2](binary_value, offset, field_handler[1])
                if val is not None:
                    result += field_handler[0] + "=" + str(val).strip() + " "
                offset += field_handler[1]
            return result[:-1]
        else:
            return "MsgType="+type_byte+"(Unsupported)"

if __name__ == '__main__':
    if '-e' in argv:
        codec = MitchCodec("lsegtp")
        for msg in MitchCodec.read_messages_from_pipe():
            print(codec.decode(msg))
    else: # -d
        pass


