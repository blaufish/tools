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

def main():
    parser = argparse.ArgumentParser(
            prog='git-obj-cat-file-raw',
            description='Decompress a raw git object and print it',
            epilog='Hope you enjoy this!')
    parser.add_argument('file')
    parser.add_argument('--debug-bin', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--debug-sha', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--decode', default=None)
    args = parser.parse_args()

    object_bin = read_file(args.file, args.debug_bin, args.debug_sha)
    output(object_bin, args.decode)

if __name__ == "__main__":
    main()
