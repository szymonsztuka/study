
#http://www.oslobors.no/ob_eng/Oslo-Boers/Trading/Trading-systems/Millennium-Exchange/Technical-documentation
mitch_handlers_2 = {
    hex(int("0x41", 16)): (
        ("length", 1, decode_blank, encode_const_integer(46)),
        ("type", 1, decode_annotated_hex("AddOrder"), encode_annotated_hex),
        ("Nanosecond", 4, decode_integer, encode_integer),
        ("OrderID", 8, decode_integer, encode_integer),
        ("Side", 1, decode_quoted_alpha, encode_quoted_alpha),
        ("Quantity", 8, decode_integer, encode_integer),
        ("InstrumentID", 4, decode_integer, encode_integer),
        ("Rsv1", 2, decode_blank, encode_blank),
        ("Price", 8, decode_price(8), encode_price(8)),  # 8 decimal points
        ("Flags", 1, decode_annotated_bitfield({(1, "bit1")}), encode_annotated_bitfield),
        ("Rsv2", 8, decode_blank, encode_blank)
    )
}
