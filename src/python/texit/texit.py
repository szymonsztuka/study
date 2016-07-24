import itertools
from collections import namedtuple
from sys import argv
import sys
import os
from ascii_codec import AsciiCodec
from simple_codec import SimpleCodec
from mitch_codec import MitchCodec
from tip_codec import TipCodec
from tagged_codec import TaggedCodec
import simple_header_codec

codec = {"fix": {"x", "x1", "x2", "y1"}, "itch": {"y2"}, "z": {"g"}}
groups = {"x": {"x1", "x2", "g"}, "y": {"y1", "y2"}}
ports = {"x": 100, "y": 120}
input_elements = {"x1", "x", "-p120"}
header_overrides = {}

input_groups = set(itertools.chain.from_iterable([groups.get(e, {e}) for e in input_elements if not e.startswith("-p")]))
input_port = ["".join(e[2:]) for e in input_elements if e.startswith("-p")]
selected_group = next(key for key, value in groups.items() if value >= input_groups)
if selected_group:
    selected_port = ports.get(selected_group, 0) if not input_port else input_port[0]
    print(sorted(list(input_groups)), "->", selected_group, ",", selected_port)
    codecs = {e: key for key, value in codec.items() for e in input_groups if e in value}
    print(codecs)
else:
    print("nothing")


Option = namedtuple('Option', ["codec", "input_groups", "selected_port", "selected_group", "codec", "stream", "localhost_ip", "original_feed_name", "dest_server"])

def options(input_elements):
    original_feed_name = [e for e in input_elements if not e.startswith("-")]
    input_groups = set(itertools.chain.from_iterable([groups.get(e, {e}) for e in input_elements if not e.startswith("-")]))
    input_port = ["".join(e[2:]) for e in input_elements if e.startswith("-p")]
    input_ip = ["".join(e[3:]) for e in input_elements if e.startswith("-ip")]
    dest_server = ["".join(e[5:]) for e in input_elements if e.startswith("-dest")]
    encode_mode = False if ("-decode" in input_elements or "-d" in input_elements) else True
    selected_group = next((key for key, value in groups.items() if value >= input_groups), None)
    codecs = {}
    selected_port = None
    if selected_group:
        selected_port = ports.get(selected_group, 0) if not input_port else input_port[0]
        #print(sorted(list(input_groups)), "->", selected_group, ",", selected_port)
    codecs = {key for key, value in codec.items() for e in input_groups if e in value}
        #print("CODEC: ",codecs)
        #print(original_feed_name)
    return Option(encode_mode, input_groups, selected_port, selected_group, codecs, header_overrides.get(selected_group, 0), input_ip[0] if input_ip else None,
                  "".join(original_feed_name), "".join(dest_server) )

def empty(x):
    pass

def generator(option):
    if option.encode_mode:
        if option.codec:
            if "mitch" in option.codec:
                if option.dest_server:
                    res = header_overrides.get(option.selected_group, {})
                    ref_stream = res.get(option.dest_server, None)
                    if ref_stream is None:
                        raise ValueError('option -dist provided with unrecognized value')
                else:
                    ref_stream = None
                codec = MitchCodec(option.original_feed_name)
                tcoddec = TaggedCodec(codec)
                enclosing = SimpleCodec(tcoddec)
                encode_message = enclosing.encode
            elif "tip" in option.codec:
                codec = TipCodec()
                enclosing = SimpleCodec(codec)
            elif "ascii" in option.codec:
                codec = AsciiCodec()
                enclosing = SimpleCodec(codec)
            else:
                encode_message = empty
            #seq = 1
            for line in sys.stdin:
                res = enclosing.encode(line) #encode_message(line) TODO TODO
                if res:
                    yield res
                    #os.write(sys.stdout.fileno(), res)
                    #seq += 1
        else:
            print("Parser not recognized, list of supported parsers")
            print(groups)
    else:
        if option.codec:
            if "mitch" in option.codec:
                if option.dest_server:
                    res = header_overrides.get(option.selected_group, {})
                    ref_stream = res.get(option.dest_server, None)
                    if ref_stream is None:
                        raise ValueError('option -dist provided with unrecognized value')
                else:
                    ref_stream = None
                codec = MitchCodec(option.original_feed_name)
                tcoddec = TaggedCodec(codec)
                enclosing = SimpleCodec(tcoddec)
            elif "ascii" in option.codec:

                codec = AsciiCodec()
                enclosing = SimpleCodec(codec)

            for msg in simple_header_codec.read_messages_from_pipe():
                res = enclosing.decode(msg)
                if res:
                    yield res

        else:
            print("Parser not recognized, list of supported parsers")
            print(groups)

if __name__ == '__main__':
    #x = options(["-e", "ascii"])
    #print(x)
    #sys.exit()

    option = options(argv[1:])
    for x in generator(option):
        if option.encode_mode:
            os.write(sys.stdout.fileno(), x) # binary
        else:
            print(x)  # ascii
        #else if send mode (tex to send, bin to send):
        #
    sys.exit()