# Git Object Cat-File Raw

Prints the object, including the object header.

## Usage

`./git-objects/git-obj-cat-file-raw -h`

``` plain
usage: git-obj-cat-file-raw [-h] [--debug-bin | --no-debug-bin]
                            [--debug-sha | --no-debug-sha]
                            [--decode-tree | --no-decode-tree]
                            [--decode DECODE]
                            [--skip-header | --no-skip-header] file

Decompress a raw git object and print it

positional arguments:
  file

options:
  -h, --help            show this help message and exit
  --debug-bin, --no-debug-bin
  --debug-sha, --no-debug-sha
  --decode-tree, --no-decode-tree
  --decode DECODE
  --skip-header, --no-skip-header

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

## Skip header

Skip header removes object headers like `commit 258<NUL>`, `tree 107<NUL>` and `blob 1138<NUL>`.
(Default: off)

Example:

`./git-obj-cat-file-raw.py --skip-header ../.git/objects/ab/e74c6bfeffc1928f9f8533b516751149255c7a | xxd | head`

``` plain
00000000: 2321 2f75 7372 2f62 696e 2f65 6e76 2070  #!/usr/bin/env p
00000010: 7974 686f 6e33 0a0a 696d 706f 7274 2061  ython3..import a
00000020: 7267 7061 7273 650a 696d 706f 7274 2068  rgparse.import h
00000030: 6173 686c 6962 0a69 6d70 6f72 7420 6f73  ashlib.import os
00000040: 0a69 6d70 6f72 7420 7379 730a 696d 706f  .import sys.impo
00000050: 7274 2074 6872 6561 6469 6e67 0a69 6d70  rt threading.imp
00000060: 6f72 7420 7a6c 6962 0a0a 6465 6620 7265  ort zlib..def re
00000070: 6164 5f66 696c 6528 6669 6c65 6e61 6d65  ad_file(filename
00000080: 2c20 6465 6275 675f 6269 6e2c 2064 6562  , debug_bin, deb
00000090: 7567 5f73 6861 293a 0a20 2020 2063 6f6d  ug_sha):.    com
```

`./git-obj-cat-file-raw.py --no-skip-header ../.git/objects/ab/e74c6bfeffc1928f9f8533b516751149255c7a | xxd | head`

``` plain
00000000: 626c 6f62 2031 3133 3800 2321 2f75 7372  blob 1138.#!/usr
00000010: 2f62 696e 2f65 6e76 2070 7974 686f 6e33  /bin/env python3
00000020: 0a0a 696d 706f 7274 2061 7267 7061 7273  ..import argpars
00000030: 650a 696d 706f 7274 2068 6173 686c 6962  e.import hashlib
00000040: 0a69 6d70 6f72 7420 6f73 0a69 6d70 6f72  .import os.impor
00000050: 7420 7379 730a 696d 706f 7274 2074 6872  t sys.import thr
00000060: 6561 6469 6e67 0a69 6d70 6f72 7420 7a6c  eading.import zl
00000070: 6962 0a0a 6465 6620 7265 6164 5f66 696c  ib..def read_fil
00000080: 6528 6669 6c65 6e61 6d65 2c20 6465 6275  e(filename, debu
00000090: 675f 6269 6e2c 2064 6562 7567 5f73 6861  g_bin, debug_sha
```

## Tree decode

Tree decode decodes a git tree.
(Default: off)

Example:
`./git-obj-cat-file-raw.py --decode-tree ../.git/objects/e4/661f4c2710db8dbfc1034b9b26643e874ea475`

``` plain
100755 git-obj-cat-file-raw.py abe74c6bfeffc1928f9f8533b516751149255c7a
100755 git-obj-commit-bruteforce.py 6c9b2f5104eaecb9b35f978b6e5761bbfca8d281
```
