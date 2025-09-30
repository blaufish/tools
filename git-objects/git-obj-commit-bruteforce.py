#!/usr/bin/env python3

import hashlib
import os
import sys
import threading
import zlib

lock = threading.Lock()
terminate = False;

def hack(git_object, counter_start, counter_increment, goal, destination_clear, destination_compressed):
    global lock
    global terminate
    print(f"hack(..., {counter_start}, {counter_increment}, {goal})", file=sys.stderr);
    header, content = git_object.split(b'\x00', 1)
    hack_str = content.decode("utf-8")
    counter = counter_start;
    while True:
        with lock:
            if terminate:
                return
        commit_content = hack_str + "\n" + str(counter) + "\n"
        commit_content_bytes = commit_content.encode("utf-8")
        commit_content_bytes_len = len(commit_content_bytes)
        header = f"commit {commit_content_bytes_len}\x00"
        header_content = header + commit_content
        to_be_hashed = header_content.encode("utf-8")
        s = hashlib.sha1(to_be_hashed).hexdigest()
        if s.startswith(goal):
            with lock:
                terminate = True
            print(f"SHA1: {s}", file=sys.stderr);
            print(f"Write to: {destination_clear} (plain)", file=sys.stderr);
            with open(destination_clear, "wb") as f:
                f.write(to_be_hashed)
            print(f"Write to: {destination_compressed} (compressed)", file=sys.stderr);
            with open(destination_compressed, "wb") as f:
                bb = zlib.compress(to_be_hashed)
                f.write(bb)
            return
        counter = counter + counter_increment

filename = sys.argv[1]
compressed_contents = open(filename, 'rb').read()
decompressed_contents = zlib.decompress(compressed_contents)
#print(f"------\n{s}\n------)", file=sys.stderr);

cpus = len(os.sched_getaffinity(0))
print(f"\rCPUs detected: {cpus}", file=sys.stderr)

threads = [threading.Thread(target=hack, args=(decompressed_contents,i,cpus,sys.argv[2], sys.argv[3], sys.argv[4])) for i in range(0, cpus)]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
