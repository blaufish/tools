# JPEG Tools

A simple JPEG parser and JPEG patcher.

## JPEG Parser

Converts the begining of a JPEG file to human readable structure.

Usage:

``` bash
python3 parse_jpeg.py -h
```

``` plain
usage: parse_jpeg.py [-h] files [files ...]

Simple JFIF/JPEG Structure Parser

positional arguments:
  files       One or more JPEG files to parse

options:
  -h, --help  show this help message and exit
```

Example usage:

``` bash
python3 parse_jpeg.py patched.jpg
```

``` plain
Parsing: patched.jpg
--------------------------------------------------
00000: FFD8: SOI (Start of Image)
00002: FFE0: APP0 (JFIF Application Segment) Length 0010  4a 46 49 46 00 01 01 01 (JFIF....)
00014: FFE1: APP1 (Exif/XMP) Length 000D  54 65 53 74 00 68 65 6c (TeSt.hel)
00023: FFE0: APP0 (JFIF Application Segment) Length 0394  47 65 6e 65 72 69 63 20 (Generic )
003B9: FFE1: APP1 (Exif/XMP) Length 15A6  45 78 69 66 00 00 49 49 (Exif..II)
01961: FFDB: DQT (Define Quantization Table) Length 0043  00 01 01 01 01 01 01 01 (........)
019A6: FFDB: DQT (Define Quantization Table) Length 0043  01 01 01 01 02 01 02 04 (........)
019EB: FFC0: SOF0 (Start of Frame, Baseline) Length 0011  08 01 2c 01 90 03 01 21 (..,....!)
019FE: FFC4: DHT (Define Huffman Table) Length 001F  00 00 01 05 01 01 01 01 (........)
01A1F: FFC4: DHT (Define Huffman Table) Length 00B5  10 00 02 01 03 03 02 04 (........)
01AD6: FFC4: DHT (Define Huffman Table) Length 001F  01 00 03 01 01 01 01 01 (........)
01AF7: FFC4: DHT (Define Huffman Table) Length 00B5  11 00 02 01 02 04 04 03 (........)
01BAE: FFDA: SOS (Start of Scan) Length 000C  03 01 00 02 11 03 11 00 (........)
```

## JPEG Patcher

Injects a custom segment into a JPEG. 

Example usage:

``` plain
usage: patch_jpeg.py [-h]
                     --input-image INPUT_IMAGE
                     --output-image OUTPUT_IMAGE
                     --input-blob INPUT_BLOB
                     --hex HEX
                     [--position POSITION] [--prefix PREFIX]

patch_jpeg.py: error: the following arguments are required: --input-image, --output-image, --input-blob, --hex
```

``` bash
python3 patch_jpeg.py -h
```

``` plain
usage: patch_jpeg.py [-h]
                     --input-image INPUT_IMAGE
                     --output-image OUTPUT_IMAGE
                     --input-blob INPUT_BLOB
                     --hex HEX
                     [--position POSITION] [--prefix PREFIX]

Inject a custom segment into a JPEG file.

options:
  -h, --help            show this help message and exit
  --input-image INPUT_IMAGE
                        Source JPEG file
  --output-image OUTPUT_IMAGE
                        Filename for the patched result
  --input-blob INPUT_BLOB
                        File containing the data to inject
  --hex HEX             4 hex characters (e.g., FFE2)
  --position POSITION   Segment index to inject after (0 = after SOI)
  --prefix PREFIX       Optional string prefix (will be null-terminated)
```

Patching a JPEG:

``` bash
echo hello > blob.bin

python3 patch_jpeg.py \
  --input-image input.jpg \
  --output-image patched.jpg \
  --hex ffe1 --prefix TeSt \
  --input-blob blob.bin
```

Parsing a JPEG:

``` plain
Injected payload after segment 1
Successfully created patched.jpg
```
