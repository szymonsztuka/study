import itertools
from collections import namedtuple
from sys import argv
import sys
import os
from ascii_codec import AsciiCodec
from simple_codec import SimpleCodec
from mitchcodec import MitchCodec
from tip_codec import TipCodec
from tagged_codec import TaggedCodec
import simple_header_codec
from fix_codec import FixCodec
import errno

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

Option = namedtuple('Option', ["encode_mode", "input_groups", "selected_port", "selected_group", "codec", "stream", "localhost_ip", "original_group_name", "dest_server"])

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
    codecs = {key for key, value in codec.items() for e in input_groups if e in value}
    return Option(encode_mode, input_groups, selected_port, selected_group, codecs, header_overrides.get(selected_group, 0), input_ip[0] if input_ip else None,
                  "".join(original_feed_name), "".join(dest_server) )


def createCodec(option):
    if option.codec:
        if "fix" in option.codec:
            codec = FixCodec()
            enclosing = SimpleCodec(codec)
        elif "mitch" in option.codec:
            codec = MitchCodec(option.original_feed_name)
            tcoddec = TaggedCodec(codec)
            enclosing = SimpleCodec(tcoddec)
        elif "tip" in option.codec:
            codec = TipCodec()
            enclosing = SimpleCodec(codec)
        elif "ascii" in option.codec:
            codec = AsciiCodec()
            enclosing = SimpleCodec(codec)
        else:
            enclosing = SimpleCodec()  # TODO dummy
    else:
        enclosing = None
        print("Option not recognized, list of supported options")
        print(groups)
    return enclosing

def generator(codec, encode):
    if encode:
        for line in sys.stdin:
            res = codec.encode(line)
            if res:
                yield res
    else:
        for msg in simple_header_codec.read_messages_from_pipe():
            res = codec.decode(msg)
            if res:
                yield res


if __name__ == '__main__':

    option = options(argv[1:])
    codec = createCodec(option)
    for msg in generator(option.encode_mode):
        if option.encode_mode:
            os.write(sys.stdout.fileno(), msg)  # binary
        else:
            if msg:
                try:
                    sys.stdout.write(msg)  # ascii
                except IOError as e:
                    if e.errno != errno.EPIPE:
                        raise
                    else:
                        sys.exit()
    sys.exit()