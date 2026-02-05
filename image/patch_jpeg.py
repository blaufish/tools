import argparse
import struct
import sys

def patch_jpeg():
    parser = argparse.ArgumentParser(description="Inject a custom segment into a JPEG file.")
    parser.add_argument("--input-image", required=True, help="Source JPEG file")
    parser.add_argument("--output-image", required=True, help="Filename for the patched result")
    parser.add_argument("--input-blob", required=True, help="File containing the data to inject")
    parser.add_argument("--hex", required=True, help="4 hex characters (e.g., FFE2)")
    parser.add_argument("--position", type=int, default=1, help="Segment index to inject after (0 = after SOI)")
    parser.add_argument("--prefix", help="Optional string prefix (will be null-terminated)")

    args = parser.parse_args()

    # 1. Prepare the payload
    try:
        marker_bytes = bytes.fromhex(args.hex)
        if len(marker_bytes) != 2:
            raise ValueError
    except ValueError:
        print("Error: --hex must be 4 hex characters (2 bytes), e.g., FFE2")
        sys.exit(1)

    with open(args.input_blob, "rb") as f:
        blob_data = f.read()

    # Build segment data: [prefix + \x00] + blob
    segment_data = b""
    if args.prefix:
        segment_data += args.prefix.encode('ascii') + b"\x00"
    segment_data += blob_data

    # Length field = length of data + 2 bytes for the length field itself
    length_val = len(segment_data) + 2
    if length_val > 65535:
        print(f"Error: Payload too large ({length_val} bytes). Max is 65535.")
        sys.exit(1)
    
    length_bytes = struct.pack(">H", length_val)
    full_injection = marker_bytes + length_bytes + segment_data

    # 2. Parse and Reconstruction
    with open(args.input_image, "rb") as f:
        src = f.read()

    if src[:2] != b"\xff\xd8":
        print("Error: Input is not a valid JPEG (missing SOI).")
        sys.exit(1)

    output = bytearray()
    # Always start with SOI
    output.extend(src[:2])
    
    current_pos = 2
    segments_passed = 0

    # If position is 0, inject immediately after SOI
    if args.position == 0:
        output.extend(full_injection)
        print("Injected payload at position 0 (after SOI)")

    # Traverse existing segments
    while current_pos < len(src):
        # Check for marker
        if src[current_pos] == 0xFF:
            marker = src[current_pos:current_pos+2]
            
            # Stop if we hit entropy data (SOS) or end (EOI)
            if marker == b"\xff\xda" or marker == b"\xff\xd9":
                output.extend(src[current_pos:])
                break
                
            # Read length of current segment to skip it
            seg_len = struct.unpack(">H", src[current_pos+2:current_pos+4])[0]
            total_seg_size = 2 + seg_len
            
            # Copy the current segment to output
            output.extend(src[current_pos : current_pos + total_seg_size])
            
            current_pos += total_seg_size
            segments_passed += 1

            # Inject if we reached the target count
            if segments_passed == args.position:
                output.extend(full_injection)
                print(f"Injected payload after segment {segments_passed}")
        else:
            # Handle stray bytes or malformed padding
            output.append(src[current_pos])
            current_pos += 1

    # 3. Save
    with open(args.output_image, "wb") as f:
        f.write(output)
    print(f"Successfully created {args.output_image}")

if __name__ == "__main__":
    patch_jpeg()
