#!/usr/bin/env python3

import hashlib
import os
import sys
import threading
import zlib

filename = sys.argv[1]

compressed_contents = open(filename, 'rb').read()
decompressed_contents = zlib.decompress(compressed_contents)
object_str = decompressed_contents.decode("utf-8")

print(decompressed_contents, file=sys.stderr)

sha1 = hashlib.sha1(decompressed_contents).hexdigest()
print(f"SHA1: {sha1}", file=sys.stderr);

print(f"{object_str}", end="");
