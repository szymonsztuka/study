import utf8codec as u
import binascii
from sys import argv
import sys


def decode_a(data, start, length):
    return data[start: start + length].rstrip(' ')


def encode_a(data, length):
    add = " " * (length - len(data))
    return data + add


def encode_a(data, length):
    add = " " * (length - len(data))
    return data + add


def decode_x(data, start, length):
    return data[start: start + length].lstrip('0')


def encode_x(data, length):
    add = "0" * (length - len(data))
    return add + data


def decode_n(data, start, length):
    result = decode_x(data, start, length)
    if len(result) == 0:
        result = '0'
    return result


def encode_n(data, length):
    return encode_x(data,length)


def encode_optional(funct):
    def internal(data, length):
        res = funct(data, length)
        if str(res) == '' or str(res).strip('0') or str(res).rstrip():
            return ''
        else:
            return res
    return internal


#http://www.oslobors.no/ob_eng/Oslo-Boers/Trading/Trading-systems/SOLA
hsvf_handlers = {
    "C": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2,  decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode", 1, decode_a, encode_a),
        ("StrikePrice", 8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("Volume", 8, decode_x, encode_x),
        ("TradePrice", 8, decode_n, encode_n),
        ("NetChangeSign", 1, decode_x, encode_x),
        ("NetChange", 8, decode_x, encode_x),
        ("StampTime", 6, decode_n, encode_n),
        ("OpenInterest", 7, decode_n, encode_n),
        ("PriceIndicatorMarker", 1, decode_a, encode_a)
    ),
    "CF": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2,  decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CorporateAction", 1, decode_a, encode_a),
        ("Volume", 8, decode_x, encode_x),
        ("TradePrice", 8, decode_x, encode_x),
        ("NetChangeSign", 1, decode_a, encode_a),
        ("NetChange", 8, decode_x, encode_x),
        ("StampTime", 6, decode_n, encode_n),
        ("PriceIndicatorMarker", 1, decode_a, encode_a)
    ),
    "E": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_x, encode_x),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_n, encode_n),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode", 1, decode_a, encode_a),
        ("StrikePrice", 8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("ScheduleInstrumentStatus", 1, decode_a, encode_a),
        ("ScheduledStatusChangeTime", 6, decode_n, encode_n)
    ),
    "EB": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_x, encode_x),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_n, encode_n),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode", 1, decode_a, encode_a),
        ("StrikePrice", 8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("ScheduleInstrumentStatus", 1, decode_a, encode_a),
        ("ScheduledStatusChangeTime", 6, decode_n, encode_n)
    ),
    "EF": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CorporateAction", 1, decode_a, encode_a),
        ("ScheduleInstrumentStatus", 1, decode_a, encode_a),
        ("ScheduledStatusChangeTime", 6, decode_n, encode_n)
    ),
    "F": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode", 1, decode_a, encode_a),
        ("StrikePrice", 8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("BidPrice", 8, decode_x, encode_x),
        ("BidSize", 5, decode_n, encode_n),
        ("AskPrice", 8, decode_x, encode_x),
        ("AskSize", 5, decode_n, encode_n),
        ("InstrumentStatusMarker", 1, decode_a, encode_a)
    ),
    "FF": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CorporateAction", 1, decode_a, encode_a),
        ("BidPrice", 8, decode_x, encode_x),
        ("BidSize", 5, decode_n, encode_n),
        ("AskPrice", 8, decode_x, encode_x),
        ("AskSize", 5, decode_n, encode_n),
        ("InstrumentStatusMarker", 1, decode_a, encode_a)
    ),
    "GC": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a), #x -> a
        ("InstrumentGroup", 2, decode_x, encode_x),
        ("GroupStatus", 1, decode_a, encode_a),
        ("ScheduledTime", 6, decode_n, encode_n),
        ("UnderlyingSymbolRoot", 10, decode_a, encode_a), #x -> a
        ("DeliveryType", 1, decode_a, encode_a),
        ("DefaultContractSize", 8, decode_n, encode_n),
        ("Description", 100, decode_a, encode_a)  #x -> a
    ),
    "GR": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a), #x -> a
        ("InstrumentGroup", 2, decode_x, encode_x),
        ("GroupStatus", 1, decode_a, encode_a),
        ("Filler", 6, decode_a, encode_a), #x -> a
        ("UnderlyingSymbolRoot", 10, decode_a, encode_a), #x -> a
        ("DeliveryType", 1, decode_a, encode_a),
        ("DefaultContractSize", 8, decode_n, encode_n),
        ("Description", 100, decode_a, encode_a), #x -> a
    ),
    "H": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode", 1, decode_a, encode_a),
        ("StrikePrice", 8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("InstrumentStatusMarker", 1, decode_a, encode_a),
        ("NumberOfLevel", 1, decode_n, encode_n),
        ("LevelOfMarketDepth", 1, decode_a, encode_a),
        ("BidPrice", 8, decode_x, encode_x),
        ("BidSize", 5, decode_n, encode_n),
        ("NumberOfBidOrders", 2, decode_x, encode_x),
        ("AskPrice", 8, decode_x, encode_x),
        ("AskSize", 5, decode_n, encode_n),
        ("NumberOfAskOrders", 2, decode_x, encode_x),

        ("LevelOfMarketDepth2", 1, decode_a, encode_a),
        ("BidPrice2", 8, decode_x, encode_x),
        ("BidSize2", 5, decode_n, encode_n),
        ("NumberOfBidOrders2", 2, decode_x, encode_x),
        ("AskPrice2", 8, decode_x, encode_x),
        ("AskSize2", 5, decode_n, encode_n),
        ("NumberOfAskOrders2", 2, decode_x, encode_x),

        ("LevelOfMarketDepth3", 1, decode_a, encode_a),
        ("BidPrice3", 8, decode_x, encode_x),
        ("BidSize3", 5, decode_n, encode_n),
        ("NumberOfBidOrders3", 2, decode_x, encode_x),
        ("AskPrice3", 8, decode_x, encode_x),
        ("AskSize3", 5, decode_n, encode_n),
        ("NumberOfAskOrders3", 2, decode_x, encode_x),

        ("LevelOfMarketDepth4", 1, decode_a, encode_a),
        ("BidPrice4", 8, decode_x, encode_x),
        ("BidSize4", 5, decode_n, encode_n),
        ("NumberOfBidOrders4", 2, decode_x, encode_x),
        ("AskPrice4", 8, decode_x, encode_x),
        ("AskSize4", 5, decode_n, encode_n),
        ("NumberOfAskOrders4", 2, decode_x, encode_x),

        ("LevelOfMarketDepth5", 1, decode_a, encode_a),
        ("BidPrice5", 8, decode_x, encode_x),
        ("BidSize5", 5, decode_n, encode_n),
        ("NumberOfBidOrders5", 2, decode_x, encode_x),
        ("AskPrice5", 8, decode_x, encode_x),
        ("AskSize5", 5, decode_n, encode_n),
        ("NumberOfAskOrders5", 2, decode_x, encode_x)
    ),
    "HF": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CorporateAction", 1, decode_a, encode_a),
        ("InstrumentStatusMarker", 1, decode_a, encode_a),
        ("NumberOfLevel", 1, decode_n, encode_n),

        ("LevelOfMarketDepth", 1, decode_a, encode_a),
        ("BidPrice", 8, decode_x, encode_x),
        ("BidSize", 5, decode_n, encode_n),
        ("NumberOfBidOrders", 2, decode_x, encode_x),
        ("AskPrice", 8, decode_x, encode_x),
        ("AskSize", 5, decode_n, encode_n),
        ("NumberOfAskOrders", 2, decode_x, encode_x),

        ("LevelOfMarketDepth2", 1, decode_a, encode_a),
        ("BidPrice2", 8, decode_x, encode_x),
        ("BidSize2", 5, decode_n, encode_n),
        ("NumberOfBidOrders2", 2, decode_x, encode_x),
        ("AskPrice2", 8, decode_x, encode_x),
        ("AskSize2", 5, decode_n, encode_n),
        ("NumberOfAskOrders2", 2, decode_x, encode_x),

        ("LevelOfMarketDepth3", 1, decode_a, encode_a),
        ("BidPrice3", 8, decode_x, encode_x),
        ("BidSize3", 5, decode_n, encode_n),
        ("NumberOfBidOrders3", 2, decode_x, encode_x),
        ("AskPrice3", 8, decode_x, encode_x),
        ("AskSize3", 5, decode_n, encode_n),
        ("NumberOfAskOrders3", 2, decode_x, encode_x),

        ("LevelOfMarketDepth4", 1, decode_a, encode_a),
        ("BidPrice4", 8, decode_x, encode_x),
        ("BidSize4", 5, decode_n, encode_n),
        ("NumberOfBidOrders4", 2, decode_x, encode_x),
        ("AskPrice4", 8, decode_x, encode_x),
        ("AskSize4", 5, decode_n, encode_n),
        ("NumberOfAskOrders4", 2, decode_x, encode_x),

        ("LevelOfMarketDepth5", 1, decode_a, encode_a),
        ("BidPrice5", 8, decode_x, encode_x),
        ("BidSize5", 5, decode_n, encode_n),
        ("NumberOfBidOrders5", 2, decode_x, encode_x),
        ("AskPrice5", 8, decode_x, encode_x),
        ("AskSize5", 5, decode_n, encode_n),
        ("NumberOfAskOrders5", 2, decode_x, encode_x)
    ),
    "I": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode", 1, decode_a, encode_a),
        ("StrikePrice", 8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("Volume", 8, decode_n, encode_n),
        ("TradePrice", 8, decode_x, encode_x),
        ("StampTime", 6, decode_n, encode_n),
        ("OpenInterest", 7, decode_n, encode_n),
        ("PriceIndicatorMarker", 1, decode_x, encode_x)
    ),
    "IF": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CorporateAction", 1, decode_a, encode_a),
        ("Volume", 8, decode_n, encode_n),
        ("TradePrice", 8, decode_x, encode_x),
        ("StampTime", 6, decode_n, encode_n),
        ("PriceIndicatorMarker", 1, decode_x, encode_x)
    ),
    "J": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2,  decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode", 1, decode_a, encode_a),
        ("StrikePrice", 8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("StrikePriceCurrency", 3, decode_a, encode_a),
        ("MaximumNumberOfContractsPerOrder", 6, decode_n, encode_n),
        ("MinimumNumberOfContractsPerOrder", 6, decode_n, encode_n),
        ("MaximumThresholdPrice", 8, decode_x, encode_x),
        ("MinimumThresholdPrice", 8, decode_x, encode_x),
        ("TickIncrementTable", 7, decode_x, encode_x),
        ("Filler", 1, decode_n, encode_n),
        ("OptionType", 1, decode_a, encode_a),
        ("MarketFlowIndicator", 2, decode_a, encode_a),
        ("GroupInstrument", 2, decode_x, encode_x),
        ("Instrument", 2, decode_x, encode_x),
        ("ISIN", 12, decode_x, encode_x),
        ("InstrumentExternalCode", 30, decode_a, encode_a),  # x -> a
        ("OptionMarker", 2, decode_a, encode_a),
        ("UnderlyingSymbolRoot", 10, decode_a, encode_a),  # x -> a
        ("ContractSize", 8, decode_n, encode_n),
        ("TickValue", 8, decode_x, encode_x)
    ),
    "JF": ( #verified
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CorporateAction", 1, decode_a, encode_a),
        ("ExpiryYear", 2, decode_n, encode_n),
        ("ExpiryMonth", 1, decode_a, encode_a),
        ("ExpiryDay", 2, decode_n, encode_n),
        ("MaximumNumberOfContractsPerOrder", 6, decode_n, encode_n),
        ("MinimumNumberOfContractsPerOrder", 6, decode_n, encode_n),
        ("MaximumThresholdPrice", 8, decode_x, encode_x),
        ("MinimumThresholdPrice", 8, decode_x, encode_x),
        ("TickIncrementTable", 7, decode_x, encode_x),
        ("Filler", 1, decode_x, encode_x),
        ("MarketFlowIndicator", 2, decode_a, encode_a),
        ("GroupInstrument", 2, decode_x, encode_x),
        ("Instrument", 4, decode_x, encode_x),
        ("ISIN", 12, decode_x, encode_x),
        ("InstrumentExternalCode", 30, decode_a, encode_a), #x -> a
        ("Currency", 3, decode_a, encode_a),
        ("UnderlyingSymbolRoot", 10, decode_a, encode_a), #x -> a
        ("ContractSize", 8, decode_n, encode_n),
        ("TickValue1", 8, decode_x, encode_x)
    ),
    "N": (
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CallPutCode",1, decode_a, encode_a),
        ("StrikePrice",8, decode_x, encode_x),
        ("CorporateAction", 1, decode_a, encode_a),
        ("BidPrice", 8, decode_x, encode_x),
        ("BidSize", 5, decode_n, encode_n),
        ("AskPrice", 8, decode_x, encode_x),
        ("AskSize", 5, decode_n, encode_n),
        ("LastPrice", 8, decode_x, encode_x),
        ("ClosingPrice", 8, decode_x, encode_x),
        ("SettlementPrice", 8, decode_x, encode_x),
        ("OpenInterest", 7, decode_n, encode_n),
        ("Tick", 1, decode_a, encode_a),  # x -> a
        ("Volume", 8, decode_n, encode_n),
        ("NetChangeSign", 1, decode_a, encode_a),
        ("NetChange", 8, decode_x, encode_x),
        ("OpenPrice", 8, decode_x, encode_x),
        ("HighPrice", 8, decode_x, encode_x),
        ("LowPrice", 8, decode_x, encode_x),
        ("OptionMarker",2, decode_a, encode_a),
        ("UnderlyingSymbolRoot", 10, decode_a, encode_a),  # x-> a
        ("DeliveryYear", 2, decode_n, encode_n),
        ("DeliveryMonth", 1, decode_a, encode_a),
        ("DeliveryDay", 2, decode_n, encode_n)
    ),
    "NF": ( #verified
        ("SequenceNumber", 9, decode_n, encode_n),
        ("type", 2, decode_a, encode_a),
        ("ExchangeID", 1, decode_a, encode_a),
        ("SymbolRoot", 6, decode_a, encode_a),
        ("MaturityYear", 2, decode_n, encode_n),
        ("MaturityMonth", 1, decode_a, encode_a),
        ("MaturityDay", 2, decode_n, encode_n),
        ("CorporateAction", 1, decode_a, encode_a),
        ("BidPrice", 8, decode_x, encode_x),
        ("BidSize", 5, decode_n, encode_n),
        ("AskPrice", 8, decode_x, encode_x),
        ("AskSize", 5, decode_n, encode_n),
        ("LastPrice", 8, decode_x, encode_x),
        ("OpenPrice", 8, decode_x, encode_x),
        ("HighPrice", 8, decode_x, encode_x),
        ("OpenPrice", 8, decode_x, encode_x),
        ("LowPrice", 8, decode_x, encode_x),
        ("ClosingPrice", 8, decode_x, encode_x),
        ("SettlementPrice", 8, decode_x, encode_x),
        ("NetChangeSign", 1, decode_a, encode_a),
        ("NetChange", 8, decode_x, encode_x),
        ("Volume", 8, decode_n, encode_n),
        ("PreviousSettlement", 8, decode_x, encode_x),
        ("OpenInterest", 7, decode_a, encode_a), #n -> a
        ("UnderlyingSymbolRoot", 10, decode_a, encode_a) # x-> a
    )
}


type_from_value = lambda value: value[9:11].rstrip()

def parse_msg(data):
    fields = dict()
    elements = data.split()
    for e in elements:
        pair = e.split("=")
        fields[pair[0]] = pair[1]
    return fields

def parse_msg_with_spaces(data):
    fields = dict()
    elems = data.split()
    prec = ()
    for e in elems:
        pair = e.split("=")
        if len(pair) == 2:
            if len(prec) > 0:
                fields[prec[0]]=prec[1]
            prec = pair
        else:
            prec[1] = prec[1] + " " + pair[0]
    if len(prec) > 0:
        fields[prec[0]] = prec[1]
    return fields

def chunkfy(data):
    return " ".join(data[i:i+2] for i in range(0, len(data), 2))

def encode_hex(payload):
    return chunkfy(binascii.hexlify(payload.encode()).decode()).upper()

#line =
#expected_hex =

#seq = line[0:line.index(" ")]
#payload = line[len(seq)+1:]
#if type_from_value(payload) in hsvf_handlers:
#    a = u.decode_msg_from_utf8string(hsvf_handlers, type_from_value, payload)
#    print("Decoded:")
#    print(a)
#    print("Encoded:")
#    back = u.encode_msg_from_tag_vals(hsvf_handlers, u.type_from_tag_vals, parse_msg_with_spaces(a))
#    print("Res: "+ back)
#    print("Exp: " + payload)
#    print(back.rstrip() == payload)
#    print("Encoded in hex:")
#    hex = encode_hex(back)
#    print("Res: "+ hex)
#    print("Exp: " +expected_hex)
#    print(expected_hex == hex)

if __name__ == '__main__':
    handlers = hsvf_handlers
    if 'f' in argv:
        for line in sys.stdin:
            if " " not in line:
                print("'"+line+"'")
            else:
                seq = line[0:line.index(" ")]
                payload = line[len(seq)+1:]
                if type_from_value(payload) in handlers:
                    sys.stdout.write(line)
    elif 'e' in argv or len(argv) == 1:  # default option
        for line in sys.stdin:
            if " " not in line:
                print("'"+line+"'")
            else:
                seq = line[0:line.index(" ")]
                payload = line[len(seq)+1:]
                if type_from_value(payload)  in handlers:
                    parts = u.dict_decode_msg_from_utf8string(handlers, type_from_value, payload)
                    res = u.encode_msg_from_tag_vals(handlers, lambda tag_values: tag_values.get("MsgType"), parts)
                    full = encode_hex(res,int(seq.split("=")[1]))
                    sys.stdout.write(full)
                    sys.stdout.write("\n")
    elif 't' in argv or len(argv) == 1:  # default option
        for line in sys.stdin:
            if " " not in line:
                print("'"+line+"'")
            else:
                seq = line[0:line.index(" ")]
                payload = line[len(seq)+1:]
                if type_from_value(payload) in handlers:
                    sys.stdout.write(payload)
                    sys.stdout.write("\n")