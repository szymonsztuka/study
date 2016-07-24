
class AsciiCodec:

    def encode(self, data):
        return data.encode()

    def decode(self, data):
        return data

if __name__ == '__main__':
    codec = AsciiCodec()
    a = codec.decode("xyz")
    print(a)
