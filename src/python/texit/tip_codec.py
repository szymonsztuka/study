
class TipCodec:

    def __init__(self, message_tags={"Qt","BDTe","BDIn"}):
        self.message_tags = {e + ";" for e in message_tags }

    def index_of_tip_payload(self, line):
        e = next((e for e in self.message_tags if e in line), None)
        if e is None:
            return -1
        else:
            return line.find(e)


    def encode(self, payload):
        i = TipCodec.index_of_tip_payload(payload)
        return payload[i:].encode()

    @staticmethod
    def test_tip():
        m1 = "time=06:30:03.6882 ;QtLGn;RxWelcome;"
        m2 = "time=06:30:03.6883    4   BDTe;n1;i1;Si1;s1;"
        m3 = "time=06:30:03.7071     BDIn;n1;i2;Si3;s4;Uc5;x6;SYmABC;NAmDEF;NAl                               ;CUxGHI;"
        i2 = TipCodec.index_of_tip_payload(m2)