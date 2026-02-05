import argparse
import struct
import os

# Mapping common markers to names
MARKERS = {
    0xFFD8: "SOI (Start of Image)",
    0xFFD9: "EOI (End of Image)",
    0xFFE0: "APP0 (JFIF Application Segment)",
    0xFFE1: "APP1 (Exif/XMP)",
    0xFFDB: "DQT (Define Quantization Table)",
    0xFFC0: "SOF0 (Start of Frame, Baseline)",
    0xFFC2: "SOF2 (Start of Frame, Progressive)",
    0xFFC4: "DHT (Define Huffman Table)",
    0xFFDA: "SOS (Start of Scan)",
    0xFFFE: "COM (Comment)"
}

def parse_jpeg(filename):
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return

    print(f"\nParsing: {filename}")
    print("-" * 50)

    with open(filename, "rb") as f:
        data = f.read()

    offset = 0
    while offset < len(data):
        # Look for the start of a marker (0xFF)
        if data[offset] != 0xFF:
            offset += 1
            continue
        
        # Ensure we have at least 2 bytes for the marker
        if offset + 1 >= len(data):
            break

        marker_code = struct.unpack(">H", data[offset:offset+2])[0]
        marker_name = MARKERS.get(marker_code, f"Unknown Marker ({marker_code:04X})")
        
        # Display Marker
        output = f"{offset:05X}: {marker_code:04X}: {marker_name}"

        # SOI and EOI don't have lengths
        if marker_code in [0xFFD8, 0xFFD9]:
            print(output)
            offset += 2
        else:
            # Next 2 bytes are the segment length
            length = struct.unpack(">H", data[offset+2:offset+4])[0]
            
            # Extract a small preview of the data (hex)
            payload_start = offset + 4
            payload_end = offset + 2 + length
            preview_bytes = data[payload_start : min(payload_start + 8, payload_end)]
            preview_hex = " ".join(f"{b:02x}" for b in preview_bytes)
            
            # Extract ASCII strings (like 'JFIF' or 'Exif')
            preview_ascii = "".join(chr(b) if 32 <= b <= 126 else "." for b in preview_bytes)

            print(f"{output} Length {length:04X}  {preview_hex.ljust(23)} ({preview_ascii})")
            
            # Move to next marker
            # Special case: SOS (Start of Scan) is followed by the image stream
            if marker_code == 0xFFDA:
                break # Usually we stop here or switch to bitstream parsing
            
            offset += 2 + length

def main():
    parser = argparse.ArgumentParser(description="Simple JFIF/JPEG Structure Parser")
    parser.add_argument("files", nargs="+", help="One or more JPEG files to parse")
    args = parser.parse_args()

    for file in args.files:
        parse_jpeg(file)

if __name__ == "__main__":
    main()
