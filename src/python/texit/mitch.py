import binascii
import mitchcodec as c

hex_val = "00 10 00 00"
byte_val = bytes.fromhex(hex_val)
int_val = int.from_bytes(byte_val, byteorder='little')

rev_byte_val = int_val.to_bytes(4, byteorder='little')
rev_hex_val_unspaced = binascii.hexlify(bytearray(rev_byte_val)).decode()
rev_hex_val = " ".join(rev_hex_val_unspaced[i:i+2] for i in range(0, len(rev_hex_val_unspaced), 2))
rev_hex_val2 = ' '.join(hex(b)[2:] for b in rev_byte_val)


print("hex_val " + str(type(hex_val)) + " len=" + str(len(hex_val)))
print("byte_val " + str(type(byte_val)) + " " + str(byte_val) + " len=" + str(len(byte_val)))
print("int_val " + str(type(int_val)) + " " + str(int_val))
print("rev_byte_val " + str(type(rev_byte_val)) + " " + str(rev_byte_val) + " len=" + str(len(rev_byte_val)))
print("rev_hex_val_unspaced " + str(type(rev_hex_val_unspaced)) + " " + str(rev_hex_val_unspaced) + " len=" + str(len(rev_hex_val_unspaced)))
print("rev_hex_val " + str(type(rev_hex_val)) + " " + str(rev_hex_val) + " len=" + str(len(rev_hex_val)))
print("rev_hex_val2 " + str(type(rev_hex_val2)) + " " + str(rev_hex_val2) + " len=" + str(len(rev_hex_val2)))


#test_from_text_msg(mitch_handlers_1, "type=0x41/AddOrder Nanosecond=007706000 OrderID=363367994316859631 Side='S' Quantity=2500 InstrumentID=37908 Price=42.95000000 Flags=0x00/bit1=0")

#test_from_text_msg(mitch_handlers_1, "type=0x46/AddAttributedOrder Nanosecond=683608000 OrderID=363526361572180373 Side='B' Quantity=200000 InstrumentID=5090 Price=33.00000000 Attribution='WNTSGB2LBIC' Flags=0x20/bit2=0,bit3=1")

#test_from_text_msg(mitch_handlers_1, "type=0x44/OrderDeleted Nanosecond=088393000 OrderID=363526361572180374 Flags=0x00/bit4=0 InstrumentID=5081")

#test_from_text_msg(mitch_handlers_1, "type=0x55/OrderModified Nanosecond=306445000 OrderID=363526361572180587 NewQuantity=200000 NewPrice=36.00000000 Flags=0x08/bit0=0,bit5=1")

#test_from_text_msg(mitch_handlers_1, "type=0x79/OrderBookClear Nanosecond=34344000 InstrumentID=21472 Flags=0x08/bit5=1")

#test_from_text_msg(mitch_handlers_1, "type=0x54/Time Seconds=18010")

#test_from_text_msg(mitch_handlers_1, "type=0x45/OrderExecuted Nanosecond=211867000 OrderID=363526341171088975 ExecutedQuantity=31 TradeID=1420024233328668")

#test_from_text_msg(mitch_handlers_1, "type=0x43/OrderExecutedWithPrice Nanosecond=177651000 OrderID=363526341171092635 ExecutedQuantity=7 DisplayQuantity=2 TradeID=1420024233328641 Printable='N' Price=755.00000000")

#test_from_text_msg(mitch_handlers_2, "type=0x41/AddOrder Nanosecond=1 OrderID=2 Side='B' Quantity=34 InstrumentID=4 Price=5.00000000 Flags=0x01/bit1=0")

print(c.decode_integer(bytes.fromhex("00 10"),0,2))
print(c.decode_integer(bytes.fromhex("00 10 00 00"),0,4))

print(c.decode_signed_integer(bytes.fromhex("87"),0,1))
print(c.decode_signed_integer(bytes.fromhex("07"),0,1))
print(c.decode_signed_integer(bytes.fromhex("07 80"),0,2))
print(c.decode_signed_integer(bytes.fromhex("07 00"),0,2))
print(c.decode_signed_integer(bytes.fromhex("07 00 00 80"),0,4))
print(c.decode_signed_integer(bytes.fromhex("07 00 00 00"),0,4))
print(c.decode_signed_integer(bytes.fromhex("6c 08 00 80"),0,4))
print(c.decode_signed_integer(bytes.fromhex("6c 08 00 00"),0,4))

print(c.decode_bitfield(bytes.fromhex("e5"),0,1))

print(c.decode_hex(bytes.fromhex("53"),0,1))
print(c.decode_hex(bytes.fromhex("73"),0,1))

#print(c.parse_date(bytes.fromhex("32 30 31 36 30 34 32 36"),0))
#print(c.parse_date(bytes.fromhex("31 39 39 39 31 32 33 31"),0))
#print(c.parse_time(bytes.fromhex("31 33 3a 32 38 3a 30 37"),0))

#print(c.parse_alpha(bytes.fromhex("61 62 63 64 65 66 67 24 31 33 3f"),0,11))

print(c.encode_integer(4096,2))
print(c.encode_signed_integer(-7,1))
print(c.encode_signed_integer(7,1))
print(c.encode_signed_integer(-7,2))
print(c.encode_signed_integer(7,2))
print(c.encode_signed_integer(-7,4))
print(c.encode_signed_integer(7,4))
print(c.encode_signed_integer(-2156,4))
print(c.encode_signed_integer(2156,4))

#print(encode_byte("S"))
#print(encode_byte("s"))

#print(encode_alpha("abcdefg$13?"))

#print(encode_date("20160426"))
#print(encode_date("19991231"))
#print(encode_time("13:28:07"))

#print(parse_signed_integer2(bytes.fromhex("00 e1 f5 05 00 00 00 80"),0,8))
#print(encode_signed_integer2(-100000000,8))
#print(parse_signed_integer2(bytes.fromhex("00 e1 f5 05 00 00 00 00"),0,8))
#print(encode_signed_integer2(100000000,8))

#print(parse_signed_integer2(bytes.fromhex("d0 50"),0,2))
#print(parse_signed_integer2(bytes.fromhex("d0 d0"),0,2))
#print(encode_signed_integer2(288,2))

#print(parse_signed_integer2(bytes.fromhex("d0"),0,1)) #ok
#print(parse_signed_integer2(bytes.fromhex("50"),0,1)) #ok

#print(parse_signed_integer2(bytes.fromhex("00 d0"),0,2))
#print(parse_signed_integer2(bytes.fromhex("00 50"),0,2)) # -> 20480

#print(encode_signed_integer2(-20480,2))
#print(encode_signed_integer2(20480,2))

#x = 80
#print( x << 8*(2-1))

#print(encode_bitfield([1, 1, 1, 0, 0, 1, 0, 1]))
