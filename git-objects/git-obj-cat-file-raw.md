# Git Object Cat-File Raw

Prints the object, including the object header.

## Usage

`./git-objects/git-obj-cat-file-raw -h`

``` plain
usage: git-obj-cat-file-raw [-h] [--debug-bin | --no-debug-bin]
                            [--debug-sha | --no-debug-sha]
                            [--decode-tree | --no-decode-tree]
                            [--decode DECODE] file

Decompress a raw git object and print it

positional arguments:
  file

options:
  -h, --help            show this help message and exit
  --debug-bin, --no-debug-bin
  --debug-sha, --no-debug-sha
  --decode-tree, --no-decode-tree
  --decode DECODE

Hope you enjoy this!
```

## Dump object

`./git-obj-cat-file-raw.py ../.git/objects/e4/661f4c2710db8dbfc1034b9b26643e874ea475 | xxd`

``` plain
00000000: 7472 6565 2031 3037 0031 3030 3735 3520  tree 107.100755
00000010: 6769 742d 6f62 6a2d 6361 742d 6669 6c65  git-obj-cat-file
00000020: 2d72 6177 2e70 7900 abe7 4c6b feff c192  -raw.py...Lk....
00000030: 8f9f 8533 b516 7511 4925 5c7a 3130 3037  ...3..u.I%\z1007
00000040: 3535 2067 6974 2d6f 626a 2d63 6f6d 6d69  55 git-obj-commi
00000050: 742d 6272 7574 6566 6f72 6365 2e70 7900  t-bruteforce.py.
00000060: 6c9b 2f51 04ea ecb9 b35f 978b 6e57 61bb  l./Q....._..nWa.
00000070: fca8 d281
```

`./git-obj-cat-file-raw.py ../.git/objects/e4/661f4c2710db8dbfc1034b9b26643e874ea475 | shasum`

``` plain
e4661f4c2710db8dbfc1034b9b26643e874ea475  -
```

## Tree decode

`./git-obj-cat-file-raw.py --decode-tree ../.git/objects/e4/661f4c2710db8dbfc1034b9b26643e874ea475`

``` plain
100755 git-obj-cat-file-raw.py abe74c6bfeffc1928f9f8533b516751149255c7a
100755 git-obj-commit-bruteforce.py 6c9b2f5104eaecb9b35f978b6e5761bbfca8d281
```
