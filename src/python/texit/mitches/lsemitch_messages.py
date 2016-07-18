import mitches.mitch_fields as f

# http://www.londonstockexchange.com/products-and-services/millennium-exchange/technicalinformation/technicalinformation.htm

messages = {
    hex(int("0x00", 16)): (  # artificial packet header
        ("Length", 2, f.decode_integer, f.encode_integer),
        ("MessageCount", 1, f.decode_integer, f.encode_integer),
        ("MarketDataGroup", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("SequenceNumber", 4, f.decode_integer, f.encode_annotated_integer)
    ),
    hex(int("0x41", 16)): (  # A
        ("length", 1, f.decode_blank, f.encode_const_integer(34)),
        ("type", 1, f.decode_annotated_hex("AddOrder"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("OrderID", 8, f.decode_integer, f.encode_integer),
        ("Side", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Quantity", 8, f.decode_integer, f.encode_integer),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("Price", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("Flags", 1, f.decode_annotated_bitfield({(1, "bit1")}), f.encode_annotated_bitfield)
    ),
    hex(int("0x42", 16)): (  # B
        ("length", 1, f.decode_blank, f.encode_const_integer(19)),
        ("type", 1, f.decode_annotated_hex("TradeBreak"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("TradeID", 8, f.decode_integer, f.encode_integer),
        ("TradeType", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
    ),
    hex(int("0x43", 16)): (  # C
        ("length", 1, f.decode_blank, f.encode_const_integer(39)),
        ("type", 1, f.decode_annotated_hex("OrderExecutedWithPrice"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("OrderID", 8, f.decode_integer, f.encode_integer),
        ("ExecutedQuantity", 4, f.decode_integer, f.encode_integer),
        ("DisplayQuantity", 4, f.decode_integer, f.encode_integer),
        ("TradeID", 8, f.decode_integer, f.encode_integer),
        ("Printable", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Price", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
    ),
    hex(int("0x44", 16)): (  # D
        ("length", 1, f.decode_blank, f.encode_const_integer(19)),
        ("type", 1, f.decode_annotated_hex("OrderDeleted"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("OrderID", 8, f.decode_integer, f.encode_integer),
        ("Flags", 1, f.decode_annotated_bitfield({(4, "bit4")}), f.encode_annotated_bitfield),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
    ),
    hex(int("0x45", 16)): (  # E
        ("length", 1, f.decode_blank, f.encode_const_integer(26)),
        ("type", 1, f.decode_annotated_hex("OrderExecuted"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("OrderID", 8, f.decode_integer, f.encode_integer),
        ("ExecutedQuantity", 4, f.decode_integer, f.encode_integer),
        ("TradeID", 8, f.decode_integer, f.encode_integer)
    ),
    hex(int("0x46", 16)): (
        ("length", 1, f.decode_blank, f.encode_const_integer(45)),
        ("type", 1, f.decode_annotated_hex("AddAttributedOrder"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("OrderID", 8, f.decode_integer, f.encode_integer),
        ("Side", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Quantity", 8, f.decode_integer, f.encode_integer),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("Price", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("Attribution", 11, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Flags", 1, f.decode_annotated_bitfield({(2, "bit2"), (3, "bit3")}), f.encode_annotated_bitfield)
    ),
    hex(int("0x47", 16)): (
        ("length", 1, f.decode_blank, f.encode_const_integer(32)),
        ("type", 1, f.decode_annotated_hex("SymbolStatus"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("InstrumentID", 8, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("TradingStatus", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Flags", 1, f.decode_annotated_bitfield({(5, "bit5")}), f.encode_annotated_bitfield),
        ("HaltReason", 4, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("SessionChangeReason", 1, f.decode_integer, f.encode_integer),
        ("NewEndTime", 8, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("BookType", 1, f.decode_integer, f.encode_integer),
    ),
    hex(int("0x49", 16)): (  # I
        ("length", 1, f.decode_blank, f.encode_const_integer(30)),
        ("type", 1, f.decode_annotated_hex("IndicAuctInfo"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("PairQuantity", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 5, f.decode_blank, f.encode_blank),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("Price", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("AuctType", 1, f.decode_quoted_alpha, f.encode_quoted_alpha)
    ),
    hex(int("0x50", 16)): (  # P
        ("length", 1, f.decode_blank, f.encode_const_integer(33)),
        ("type", 1, f.decode_annotated_hex("Trade"), f.encode_annotated_hex),
        ("ExecQuantity", 8, f.decode_integer, f.encode_integer),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("Price", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("TradeID", 8, f.decode_integer, f.encode_annotated_integer),
        ("CrossType", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
    ),
    hex(int("0x51", 16)): (  # Q
        ("length", 1, f.decode_blank, f.encode_const_integer(33)),
        ("MsgType", 1, f.decode_annotated_hex("AuctionTrade"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("Quantity", 4, f.decode_integer, f.encode_integer),
        ("InstID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("Pr", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points 
        ("TrMtchID", 8, f.decode_integer, f.encode_annotated_integer),
        ("AuctTy", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
    ),
    hex(int("0x52", 16)): (  # R
        ("length", 1, f.decode_blank, f.encode_const_integer(65)),
        ("type", 1, f.decode_annotated_hex("SymbDir"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("SymbolStatus", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("ISIN", 12, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("SEDOL", 12, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Segment", 6, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Rsv", 6, f.decode_blank, f.encode_blank),
        ("Curr", 3, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Rsv", 5, f.decode_blank, f.encode_blank),
        ("PreviousClosePrice", 8, f.decode_price(8), f.encode_price(8)),
     ),
     hex(int("0x53", 16)): (  # S
        ("length", 1, f.decode_blank, f.encode_const_integer(7)),
        ("type", 1, f.decode_annotated_hex("SysEv"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("Code", 1, f.decode_quoted_alpha, f.encode_quoted_alpha)
    ),
    hex(int("0x54", 16)): (   # T
        ("length", 1, f.decode_blank, f.encode_const_integer(6)),
        ("type", 1, f.decode_annotated_hex("Time"), f.encode_annotated_hex),
        ("Seconds", 4, f.decode_integer, f.encode_integer),
    ),
    hex(int("0x55", 16)): (
        ("length", 1, f.decode_blank, f.encode_const_integer(27)),
        ("type", 1, f.decode_annotated_hex("OrderModified"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("OrderID", 8, f.decode_integer, f.encode_integer),
        ("NewQuantity", 4, f.decode_integer, f.encode_integer),
        ("NewPrice", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("Flags", 1, f.decode_annotated_bitfield({(0, "bit0"), (5, "bit5")}), f.encode_annotated_bitfield)
    ),
    hex(int("0x77", 16)): (  # w
        ("length", 1, f.decode_blank, f.encode_const_integer(23)),
        ("type", 1, f.decode_annotated_hex("Stats"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("StatType", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Price", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("OpenClosePriceIndicator", 1, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Rsv", 1, f.decode_blank, f.encode_blank),
    ),
    hex(int("0x78", 16)): (
        ("length", 1, f.decode_blank, f.encode_const_integer(70)),
        ("type", 1, f.decode_annotated_hex("OffBkTrade"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("ExecQuantty", 4, f.decode_integer, f.encode_integer),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("Price", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("TradeID", 8, f.decode_integer, f.encode_annotated_integer),
        ("TradeType", 4, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("TradeTi", 8, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("TradeDa", 8, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("TrdCurr", 4, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("OrigPrice", 8, f.decode_price(8), f.encode_price(8)),  # 8 decimal points
        ("ExecVen", 5, f.decode_quoted_alpha, f.encode_quoted_alpha),
        ("Flags", 1, f.decode_annotated_bitfield({(5, "bit5")}), f.encode_annotated_bitfield),
    ),
    hex(int("0x79", 16)): (
        ("length", 1, f.decode_blank, f.encode_const_integer(13)),
        ("type", 1, f.decode_annotated_hex("OrderBookClear"), f.encode_annotated_hex),
        ("Nanosecond", 4, f.decode_integer, f.encode_integer),
        ("InstrumentID", 4, f.decode_integer, f.encode_integer),
        ("Rsv", 2, f.decode_blank, f.encode_blank),
        ("Flags", 1, f.decode_annotated_bitfield({(5, "bit5")}), f.encode_annotated_bitfield),
    ),
    hex(int("0x3B", 16)): (
        ("auxiliary", 0, f.decode_quoted_alpha, f.encode_quoted_alpha),
    )
}

