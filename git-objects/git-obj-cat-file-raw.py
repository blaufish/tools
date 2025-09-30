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
    utf8 = decompressed_contents.decode("utf-8")

    if debug_bin:
        print(decompressed_contents, file=sys.stderr)

    if debug_sha:
        sha1 = hashlib.sha1(decompressed_contents).hexdigest()
        print(f"SHA1: {sha1}", file=sys.stderr)

    return utf8

def main():
    parser = argparse.ArgumentParser(
            prog='git-obj-cat-file-raw',
            description='Decompress a raw git object and print it',
            epilog='Hope you enjoy this!')
    parser.add_argument('file')
    parser.add_argument('--debug-bin', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('--debug-sha', action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()

    object_str = read_file(args.file, args.debug_bin, args.debug_sha)
    print(f"{object_str}", end="")

if __name__ == "__main__":
    main()
