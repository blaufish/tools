# Tools, scripts and other funsies!

## Git Object tools

* [git-obj-cat-file-raw](git-objects/git-obj-cat-file-raw.py)
* [git-obj-commit-bruteforce.py](git-objects/git-obj-commit-bruteforce.py)

### Git Object Cat-File Raw

Prints the object, including the object header.

`./git-objects/git-obj-cat-file-raw -h`

``` plain
usage: git-obj-cat-file-raw [-h] [--debug-bin | --no-debug-bin] [--debug-sha | --no-debug-sha] file

Decompress a raw git object and print it

positional arguments:
  file

options:
  -h, --help            show this help message and exit
  --debug-bin, --no-debug-bin
  --debug-sha, --no-debug-sha

Hope you enjoy this!
```

### Git Object Commit Bruteforce

Searches for a commit message resulting in the user-prefered commit short hash.

`./git-objects/git-obj-commit-bruteforce.py -h`

``` plain
usage: git-obj-commit-bruteforce [-h] --shorthash SHORTHASH --input INPUT
                                 --output-uncompressed OUTPUT_UNCOMPRESSED
                                 --output OUTPUT

Find a git commit with a specific short hash using bruteforce

options:
  -h, --help            show this help message and exit
  --shorthash SHORTHASH
  --input INPUT
  --output-uncompressed OUTPUT_UNCOMPRESSED
  --output OUTPUT

Hope you enjoy this!
```

Example usage:

``` plain
time \
 ./git-obj-commit-bruteforce.py \
 --shorthash 1234567 \
 --input ../.git/objects/8c/44315e65ecb9f842dddd187f16e19c999e0582 \
 --output-uncompressed out.uncompressed \
 --output out.compressed
```

``` plain
CPUs detected: 32
bruteforce(..., 0, 32, 1234567)
bruteforce(..., 1, 32, 1234567)
bruteforce(..., 2, 32, 1234567)
bruteforce(..., 3, 32, 1234567)
bruteforce(..., 4, 32, 1234567)
bruteforce(..., 5, 32, 1234567)
bruteforce(..., 6, 32, 1234567)
bruteforce(..., 7, 32, 1234567)
bruteforce(..., 8, 32, 1234567)
bruteforce(..., 9, 32, 1234567)
bruteforce(..., 10, 32, 1234567)
bruteforce(..., 11, 32, 1234567)
bruteforce(..., 12, 32, 1234567)
bruteforce(..., 13, 32, 1234567)
bruteforce(..., 14, 32, 1234567)
bruteforce(..., 15, 32, 1234567)
bruteforce(..., 16, 32, 1234567)
bruteforce(..., 17, 32, 1234567)
bruteforce(..., 18, 32, 1234567)
bruteforce(..., 19, 32, 1234567)
bruteforce(..., 20, 32, 1234567)
bruteforce(..., 21, 32, 1234567)
bruteforce(..., 22, 32, 1234567)
bruteforce(..., 23, 32, 1234567)
bruteforce(..., 24, 32, 1234567)
bruteforce(..., 25, 32, 1234567)
bruteforce(..., 26, 32, 1234567)
bruteforce(..., 27, 32, 1234567)
bruteforce(..., 28, 32, 1234567)
bruteforce(..., 30, 32, 1234567)
bruteforce(..., 29, 32, 1234567)
bruteforce(..., 31, 32, 1234567)
SHA1: 1234567c9970a96b777c9e926d9788db36a043ff
Write to: out.uncompressed (plain)
Write to: out.compressed (compressed)

real    10m50.982s
user    11m23.609s
sys     0m23.950s
```
