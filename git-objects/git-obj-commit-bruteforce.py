#!/usr/bin/env python3

import argparse
import hashlib
import os
import sys
import threading
import zlib

lock = threading.Lock()
terminate = False;

def bruteforce(git_object, counter_start, counter_increment, shorthash, destination_clear, destination_compressed):
    global lock
    global terminate
    print(f"bruteforce(..., {counter_start}, {counter_increment}, {shorthash})", file=sys.stderr);
    old_header, old_content = git_object.split(b'\x00', 1)
    old_content_str = old_content.decode("utf-8")
    counter = counter_start;
    while True:
        with lock:
            if terminate:
                return
        commit_content = old_content_str + "\n" + str(counter) + "\n"
        commit_content_bytes = commit_content.encode("utf-8")
        commit_content_bytes_len = len(commit_content_bytes)
        header = f"commit {commit_content_bytes_len}\x00"
        header_content = header + commit_content
        to_be_hashed = header_content.encode("utf-8")
        s = hashlib.sha1(to_be_hashed).hexdigest()
        if s.startswith(shorthash):
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

def read_file(filename):
    compressed_contents = open(filename, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents)
    return decompressed_contents

def execute_threaded(shorthash, decompressed_contents, f_out, f_out_uncompressed):
    cpus = len(os.sched_getaffinity(0))
    print(f"CPUs detected: {cpus}", file=sys.stderr)

    threads = [threading.Thread(target=bruteforce, args=(decompressed_contents, i, cpus, shorthash, f_out_uncompressed, f_out)) for i in range(0, cpus)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def main():
    parser = argparse.ArgumentParser(
            prog='git-obj-commit-bruteforce',
            description='Find a git commit with a specific short hash using bruteforce',
            epilog='Hope you enjoy this!')
    parser.add_argument('--shorthash', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output-uncompressed', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    uncompressed_input = read_file(args.input)

    execute_threaded(
            args.shorthash,
            uncompressed_input,
            args.output,
            args.output_uncompressed)

if __name__ == "__main__":
    main()
