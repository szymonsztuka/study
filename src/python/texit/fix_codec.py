import sys
import os

class FixCodec:

    def __init__(self, tags={"1", "2", "3", "4", "35"}):
       self.tags = tags


    @staticmethod
    def replace_delimiters(data, fix_tags, old_delimiter=" ", new_delimiter=b'\x01'.decode("ascii"), append_new_delimiter=True):
        if data.rstrip() == '' or data is None:
            return None
        result = ""
        elems = data.split(old_delimiter)
        prev = ()
        for e in elems:
            pair = e.split("=")
            if len(pair) >= 2 and pair[0] in fix_tags:
                if len(prev) > 0:
                    result = result + prev[0] + "=" + "=".join(prev[1:]) + new_delimiter
                prev = pair
            else:
                prev[1] = prev[1] + " " + "=".join(pair)
        if len(prev) > 0:
            result = result + prev[0] + "=" + "=".join(prev[1:]) + new_delimiter
        if not append_new_delimiter:
            result = result[:len(result)-1]
        return result


    def encode(self, payload):
        msg = FixCodec.replace_delimiters(data=payload, fix_tags=self.tags)
        return msg.encode() if msg else None


    def decode(self, msg):
        decoded = msg.decode("utf-8")
        return FixCodec.replace_delimiters(data=decoded, fix_tags=self.tags, old_delimiter=b'\x01'.decode("ascii"), new_delimiter=" ", append_new_delimiter=False) + "\n"

    def read(self):
        for line in sys.stdin:
            os.write(sys.stdout.fileno(), self.encode(line))

def test():
    text = "35=d 1=FIXT.1 2=49 3=te company name < xxx > 4= \"56=78"
    codec = FixCodec()
    result = codec.encode(text)
    expected = bytearray(b'35=d\x011=FIXT.1\x012=49\x013=te company name < xxx >\x014= "56=78\x01')
    reverse = codec.decode(expected)
    if result == expected:
        print("ENCODE PASSED")
    else:
        print("ENCODE FAIL")
        print(result)
        print(expected)
    if reverse == text + " \n":
        print("DECODE PASSED")
    else:
        print("DECODE FAIL")
        print(reverse)
        print(text)

if __name__ == '__main__':
    test()
