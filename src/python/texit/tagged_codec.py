

class TaggedCodec:

    def __init__(self, payload_decoder=None):
        self.decoder = payload_decoder

    @staticmethod
    def parse_message(self, data):
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

    def encode(self, text):
        parser_payload = TaggedCodec.parse_message(text)
        encoded_payload = self.decoder.encode(parser_payload)
        if encoded_payload is None:
            return None
        return encoded_payload

    def decode(self, binary_val):
        res = self.decoder.decode(binary_val)
        #don't conver to tag values
        return res
