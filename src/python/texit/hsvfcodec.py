import utf8codec as u


def encode_alpha(data, length):
    missing = length - len(data)
    add = " " * missing
    return data + add

#http://www.oslobors.no/ob_eng/Oslo-Boers/Trading/Trading-systems/SOLA
hsvf_handlers = {
    "C": (
        ("SequenceNumber", 9, u.decode_integer, u.encode_integer),
        ("type", 2,  u.decode_alpha, encode_alpha),
        ("ExchangeID", 1, u.decode_alpha, encode_alpha),
        ("SymbolRoot", 6, u.decode_alpha, encode_alpha),
        ("MaturityYear", 2, u.decode_integer, u.encode_integer),
        ("MaturityMonth", 1, u.decode_alpha, encode_alpha),
        ("MaturityDay", 2, u.decode_integer, u.encode_integer),
        ("CallPutCode", 1, u.decode_alpha, encode_alpha),
        ("StrikePrice", 8, u.decode_integer, u.encode_integer),  #X
        ("CorporateAction", 1, u.decode_alpha, encode_alpha),
        ("Volume", 8, u.decode_integer, u.encode_integer),
        ("TradePrice", 8, u.decode_integer, u.encode_integer),
        ("NetChangeSign", 1, u.decode_integer, u.encode_integer),
        ("NetChange", 8, u.decode_alpha, encode_alpha),
        ("StampTime", 6, u.decode_integer, u.encode_integer),
        ("OpenInterest", 7, u.decode_integer, u.encode_integer),
        ("PriceIndicatorMarker", 1, u.decode_alpha, encode_alpha)
    ),
    "CF": (
        ("SequenceNumber", 9, u.decode_integer, u.encode_integer),
        ("type", 2,  u.decode_alpha, encode_alpha),
        ("ExchangeID", 1, u.decode_alpha, encode_alpha),
        ("SymbolRoot", 6, u.decode_alpha, encode_alpha),
        ("MaturityYear", 2, u.decode_integer, u.encode_integer),
        ("MaturityMonth", 1, u.decode_alpha, encode_alpha),
        ("MaturityDay", 2, u.decode_integer, u.encode_integer),
        ("CorporateAction", 1, u.decode_alpha, encode_alpha),
        ("Volume", 8, u.decode_integer, u.encode_integer),
        ("TradePrice", 8, u.decode_integer, u.encode_integer),
        ("NetChangeSign", 1, u.decode_integer, u.encode_integer),
        ("NetChange", 8, u.decode_alpha, encode_alpha),
        ("StampTime", 6, u.decode_integer, u.encode_integer),
        ("PriceIndicatorMarker", 1, u.decode_alpha, encode_alpha)
    ),
    "H": (
        ("SequenceNumber", 9, u.decode_integer, u.encode_integer),
        ("type", 2, u.decode_alpha, encode_alpha),
        ("ExchangeID", 1, u.decode_alpha, encode_alpha),
        ("SymbolRoot", 6, u.decode_alpha, encode_alpha),
        ("MaturityYear", 2, u.decode_integer, u.encode_integer),
        ("MaturityMonth", 1, u.decode_alpha, encode_alpha),
        ("MaturityDay", 2, u.decode_integer, u.encode_integer),
        ("CallPutCode", 1, u.decode_alpha, encode_alpha),
        ("StrikePrice", 8, u.decode_integer, u.encode_integer),  #X
        ("CorporateAction", 1, u.decode_alpha, encode_alpha),
        ("InstrumentStatusMarker", 1, u.decode_alpha, encode_alpha),
        ("NumberOfLevel", 1, u.decode_integer, u.encode_integer),
        ("LevelOfMarketDepth", 1, u.decode_alpha, encode_alpha),
        ("BidPrice", 8, u.decode_integer, u.encode_integer),  #X
        ("BidSize", 5, u.decode_integer, u.encode_integer),
        ("NumberOfBidOrders", 2, u.decode_integer, u.encode_integer),  #X
        ("AskPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("AskSize", 5, u.decode_integer, u.encode_integer),
        ("NumberOfAskOrders", 2, u.decode_integer, u.encode_integer),  #X

        ("LevelOfMarketDepth2", 1, u.decode_alpha, encode_alpha),
        ("BidPrice2", 8, u.decode_integer, u.encode_integer),  # X
        ("BidSize2", 5, u.decode_integer, u.encode_integer),
        ("NumberOfBidOrders2", 2, u.decode_integer, u.encode_integer),  # X
        ("AskPrice2", 8, u.decode_integer, u.encode_integer),  # X
        ("AskSize2", 5, u.decode_integer, u.encode_integer),
        ("NumberOfAskOrders2", 2, u.decode_integer, u.encode_integer),  # X

        ("LevelOfMarketDepth3", 1, u.decode_alpha, encode_alpha),
        ("BidPrice3", 8, u.decode_integer, u.encode_integer),  # X
        ("BidSize3", 5, u.decode_integer, u.encode_integer),
        ("NumberOfBidOrders3", 2, u.decode_integer, u.encode_integer),  # X
        ("AskPrice3", 8, u.decode_integer, u.encode_integer),  # X
        ("AskSize3", 5, u.decode_integer, u.encode_integer),
        ("NumberOfAskOrders3", 2, u.decode_integer, u.encode_integer),  # X

        ("LevelOfMarketDepth4", 1, u.decode_alpha, encode_alpha),
        ("BidPrice4", 8, u.decode_integer, u.encode_integer),  # X
        ("BidSize4", 5, u.decode_integer, u.encode_integer),
        ("NumberOfBidOrders4", 2, u.decode_integer, u.encode_integer),  # X
        ("AskPrice4", 8, u.decode_integer, u.encode_integer),  # X
        ("AskSize4", 5, u.decode_integer, u.encode_integer),
        ("NumberOfAskOrders4", 2, u.decode_integer, u.encode_integer),  # X

        ("LevelOfMarketDepth5", 1, u.decode_alpha, encode_alpha),
        ("BidPrice5", 8, u.decode_integer, u.encode_integer),  # X
        ("BidSize5", 5, u.decode_integer, u.encode_integer),
        ("NumberOfBidOrders5", 2, u.decode_integer, u.encode_integer),  # X
        ("AskPrice5", 8, u.decode_integer, u.encode_integer),  # X
        ("AskSize5", 5, u.decode_integer, u.encode_integer),
        ("NumberOfAskOrders5", 2, u.decode_integer, u.encode_integer)  # X
    ),
    "J": (
        ("SequenceNumber", 9, u.decode_integer, u.encode_integer),
        ("type", 2,  u.decode_alpha, encode_alpha),
        ("ExchangeID", 1, u.decode_alpha, encode_alpha),
        ("SymbolRoot", 6, u.decode_alpha, encode_alpha),
        ("MaturityYear", 2, u.decode_integer, u.encode_integer),
        ("MaturityMonth", 1, u.decode_alpha, encode_alpha),
        ("MaturityDay", 2, u.decode_integer, u.encode_integer),
        ("CallPutCode", 1, u.decode_alpha, encode_alpha),
        ("StrikePrice", 8, u.decode_integer, u.encode_integer),  #X
        ("CorporateAction", 1, u.decode_alpha, encode_alpha),
        ("StrikePriceCurrency", 3, u.decode_alpha, encode_alpha),
        ("MaximumNumberOfContractsPerOrder", 6, u.decode_integer, u.encode_integer),
        ("MinimumNumberOfContractsPerOrder", 6, u.decode_integer, u.encode_integer),
        ("MaximumThresholdPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("MinimumThresholdPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("TickIncrementTable", 7, u.decode_integer, u.encode_integer),  # X
        ("Filler", 1, u.decode_integer, u.encode_integer),
        ("OptionType", 1, u.decode_alpha, encode_alpha),
        ("MarketFlowIndicator", 2, u.decode_alpha, encode_alpha),
        ("GroupInstrument", 2, u.decode_integer, u.encode_integer),  # X
        ("Instrument", 2, u.decode_integer, u.encode_integer),  # X
        ("ISIN", 12, u.decode_integer, u.encode_integer),  # X
        ("InstrumentExternalCode", 30, u.decode_integer, u.encode_integer),  # X
        ("OptionMarker", 2, u.decode_alpha, encode_alpha),
        ("UnderlyingSymbolRoot", 10, u.decode_integer, u.encode_integer),  # X
        ("ContractSize", 8, u.decode_integer, u.encode_integer),
        ("TickValue", 8, u.decode_integer, u.encode_integer)  # X
    ),
    "JF": (
        ("SequenceNumber", 9, u.decode_integer, u.encode_integer),
        ("type", 2, u.decode_alpha, encode_alpha),
        ("ExchangeID", 1, u.decode_alpha, encode_alpha),
        ("SymbolRoot", 6, u.decode_alpha, encode_alpha),
        ("MaturityYear", 2, u.decode_integer, u.encode_integer),
        ("MaturityMonth", 1, u.decode_alpha, encode_alpha),
        ("MaturityDay", 2, u.decode_integer, u.encode_integer),
        ("CorporateAction", 1, u.decode_alpha, encode_alpha),
        ("ExpiryYear", 2, u.decode_integer, u.encode_integer),
        ("ExpiryMonth", 1, u.decode_alpha, encode_alpha),
        ("ExpiryDay", 2, u.decode_integer, u.encode_integer),
        ("MaximumNumberOfContractsPerOrder", 6, u.decode_integer, u.encode_integer),
        ("MinimumNumberOfContractsPerOrder", 6, u.decode_integer, u.encode_integer),
        ("MaximumThresholdPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("MinimumThresholdPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("TickIncrementTable", 7, u.decode_integer, u.encode_integer),  # X
        ("Filler", 1, u.decode_integer, u.encode_integer),
        ("OptionType", 1, u.decode_alpha, encode_alpha),
        ("MarketFlowIndicator", 2, u.decode_alpha, encode_alpha),
        ("GroupInstrument", 2, u.decode_integer, u.encode_integer),  # X
        ("Instrument", 2, u.decode_integer, u.encode_integer),  # X
        ("ISIN", 12, u.decode_integer, u.encode_integer),  # X
        ("InstrumentExternalCode", 30, u.decode_integer, u.encode_integer),  # X
        ("Currency", 3, u.decode_alpha, encode_alpha),
        ("UnderlyingSymbolRoot", 10, u.decode_integer, u.encode_integer),  # X
        ("ContractSize", 8, u.decode_integer, u.encode_integer),
        ("TickValue", 8, u.decode_integer, u.encode_integer)  # X
    ),
    "NF": (
        ("SequenceNumber", 9, u.decode_integer, u.encode_integer),
        ("type", 2, u.decode_alpha, encode_alpha),
        ("ExchangeID", 1, u.decode_alpha, encode_alpha),
        ("SymbolRoot", 6, u.decode_alpha, encode_alpha),
        ("MaturityYear", 2, u.decode_integer, u.encode_integer),
        ("MaturityMonth", 1, u.decode_alpha, encode_alpha),
        ("MaturityDay", 2, u.decode_integer, u.encode_integer),
        ("CorporateAction", 1, u.decode_alpha, encode_alpha),
        ("BidPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("BidSize", 5, u.decode_integer, u.encode_integer),
        ("AskPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("AskSize", 5, u.decode_integer, u.encode_integer),
        ("LastPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("OpenPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("HighPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("OpenPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("LowPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("ClosingPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("SettlementPrice", 8, u.decode_integer, u.encode_integer),  # X
        ("NetChangeSign", 1, u.decode_alpha, encode_alpha),  #todo x
        ("NetChange", 8, u.decode_integer, u.encode_integer),  # X
        ("Volume", 8, u.decode_integer, u.encode_integer),
        ("PreviousSettlement", 8, u.decode_integer, u.encode_integer),  # X
        ("OpenInterest", 7, u.decode_integer, u.encode_integer),
        ("UnderlyingSymbolRoot", 10, u.decode_integer, u.encode_integer), # X
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

msg= ""
a=u.decode_msg_from_utf8string(hsvf_handlers, type_from_value, msg)
print("Decoded:")
print(a)
print("Encoded:")
print(u.encode_msg_from_tag_vals(hsvf_handlers, u.type_from_tag_vals, parse_msg(a)))
print(msg)
