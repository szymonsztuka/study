from sys import argv

class MitchCodec:

    def __init__(self, handler, type_tag="type", type_bin_offset=1):
        self.type_from_binary = lambda value: hex(ord(value[type_bin_offset:type_bin_offset+1].decode("ascii")))  # TODO use indices from grammars
        self.type_tag = type_tag
        self.type_from_tag_vals = lambda tag_values: hex(int(tag_values.get(type_tag)[:tag_values.get(type_tag).index("(")], 16))  # TODO use indices from grammars
        self.handlers = handler

    def decode_from_hex_string(self, value): #TODO move to enclosing codec
        type_decoder = lambda value: hex(int("0x" + value[3:5], 16))
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
            return self.type_tag + "=" + type_byte + "(Unsupported)"

if __name__ == '__main__':
    if '-e' in argv:
        codec = MitchCodec("lsegtp")
        for msg in MitchCodec.read_messages_from_pipe():
            print(codec.decode(msg))
    else: # -d
        pass
