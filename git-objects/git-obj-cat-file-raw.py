#!/usr/bin/env python3

import argparse
import hashlib
import os
import sys
import threading
import zlib

def read_file(filename, debug_bin, debug_sha):
    compressed_contents = open(filename, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents)

    if debug_bin:
        print(decompressed_contents, file=sys.stderr)

    if debug_sha:
        sha1 = hashlib.sha1(decompressed_contents).hexdigest()
        print(f"SHA1: {sha1}", file=sys.stderr)

    return decompressed_contents

def output(object_bin, decode):
    if decode is None:
        sys.stdout.buffer.write(object_bin)
    else:
        object_str = object_bin.decode(decode)
        print(f"{object_str}", end="")

def is_object(object_bin, object_type): # peek, taste, the object header
    object_type_bin = object_type.encode("utf-8")
    return object_bin.startswith(object_type_bin)

def output_tree(object_bin):
    seek = 0
    # skip object header
    while object_bin[seek] != 0:
        seek = seek + 1
    seek = seek + 1
    # parse tree
    while seek < len(object_bin):
        base = seek
        while object_bin[seek] != 0:
            seek = seek + 1

        readable = object_bin[base:seek]
        sha = object_bin[seek+1:seek+21]

        seek = seek + 21

        sha_str = sha.hex().encode("utf-8")
        sys.stdout.buffer.write(readable)
        sys.stdout.buffer.write(b"\x20")
        sys.stdout.buffer.write(sha_str)
        sys.stdout.buffer.write(b"\x0a")

def main():
    parser = argparse.ArgumentParser(
            prog='git-obj-cat-file-raw',
            description='Decompress a raw git object and print it',
            epilog='Hope you enjoy this!')
    parser.add_argument('file')
    parser.add_argument('--debug-bin', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--debug-sha', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--decode-tree', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--decode', default=None)
    args = parser.parse_args()

    object_bin = read_file(args.file, args.debug_bin, args.debug_sha)

    if args.decode_tree and is_object(object_bin, "tree"):
        output_tree(object_bin)
        return

    output(object_bin, args.decode)

if __name__ == "__main__":
    main()
