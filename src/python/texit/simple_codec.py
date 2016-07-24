import time

import simple_header_codec

class SimpleCodec:

    def __init__(self, header_encoder, payload_decoder, header_tags, last_tag, header_tags_metadata_overrides=None):
        self.header_encoder = header_encoder
        self.payload_decoder = payload_decoder
        self.header_tags = [" " + e + "=" for e in header_tags]
        self.last_tag = " " + last_tag + "="
        self.header_tags_metadata_overrides = header_tags_metadata_overrides

    def index_of_payload(self, line):
        start = line.find(self.last_tag)
        if start >= 0:
            start = line.find(" ", start + 1) + 1
        return start

    def split_header_and_payload(self, line):
        payload_start = self.index_of_payload(line)
        if payload_start >= 0:
            payload = line[payload_start:].rstrip()
            header = line[0:payload_start]
            return header, payload
        else:
            return None, None

    def get_metadata(self, header, encoded_payload, payload):
        header = " " + header #TODO fix
        result = [header[offset + length: header.index(" ", offset + length)] if offset >= 0 else '0' for offset, length in ((header.find(e), len(e)) for e in self.header_tags)] \
            + [len(encoded_payload)] 
        # TODO apply header_tags_metadata_overrides  
        return result

    def encode(self, text):
        header, payload = self.split_header_and_payload(text)
        if self.payload_decoder is not None:
            encoded_payload = self.payload_decoder.encode(payload)
            if encoded_payload is None:
                encoded_payload = ""
        header_metadata = self.get_metadata(header, encoded_payload, payload)
        encoded_header = self.header_encoder.encode(*header_metadata)
        return encoded_header + encoded_payload

    def decode(self, binary_val):
        header = self.header_encoder.decode(binary_val)
        try:
            res = self.payload_decoder.decode(binary_val[24:])
        except UnicodeDecodeError:
            print(binary_val[24:])
        if res is None:
            print("Error", header)
        return header + res

if __name__ == '__main__':
    
    headers= ["time", "stream"]
    last_header_tag = headers[1]
    line = "time=07:59:59.9999 stream=1 "



