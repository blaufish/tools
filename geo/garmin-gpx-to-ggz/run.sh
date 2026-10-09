#!/usr/bin/env bash
set -e

usage() {
    echo "Usage: $0 --gpx <dir-input-gpx> --ggz <dir-output-ggz>"
    echo "       $0 --build"
    echo "       $0 --debug"
    exit 1
}

IMAGE_NAME="gpx2ggz-builder:latest"
INPUT_DIR=""
OUTPUT_DIR=""
build=""
debug=""

while [[ $# -gt 0 ]]; do
    case "$1" in
	--build)
	    build=true
            shift 1
            ;;
	--debug)
	    debug=true
            shift 1
            ;;
        --gpx)
            [[ -z "$2" ]] && usage
            INPUT_DIR="$2"
            shift 2
            ;;
        --ggz)
            [[ -z "$2" ]] && usage
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

if command -v podman &> /dev/null; then
    RUNTIME="podman"
elif command -v docker &> /dev/null; then
    RUNTIME="docker"
else
    echo "Error: Neither podman nor docker command line tool was found."
    exit 1
fi

if [[ ! -z "$build" ]]
then
    echo "Building container image using $RUNTIME..."
    $RUNTIME build -t "$IMAGE_NAME" -f Dockerfile .
fi

if [[ -z "$INPUT_DIR" || -z "$OUTPUT_DIR" ]]; then
    echo "Error: Both --gpx and --ggz flags are required."
    usage
fi

mkdir -p "$OUTPUT_DIR"
ABS_INPUT="$(realpath "$INPUT_DIR")"
ABS_OUTPUT="$(realpath "$OUTPUT_DIR")"

echo "Running GGZ Converter..."
$RUNTIME run --rm \
    -v "$ABS_INPUT:/data/input:Z" \
    -v "$ABS_OUTPUT:/data/output:Z" \
    "$IMAGE_NAME" \
    --gpx /data/input \
    --ggz /data/output

if [[ ! -z "$debug" ]]
then
    set -x
    pushd -- "$ABS_INPUT"
    files=(*.gpx)
    data_files=("${files[@]/#//data/input/}")
    $RUNTIME run --rm \
       -v "$ABS_INPUT:/data/input:Z" \
       -v "$ABS_OUTPUT:/data/output:Z" \
        --entrypoint /ggz-tools/gpx2ggz.py \
       "$IMAGE_NAME" \
       "${data_files[@]}" \
       /data/output/geocaches-ref.ggz
    popd
    set +x
fi

echo "Verifying generated GGZ files..."
GGZ_FILES=("$ABS_OUTPUT"/*.ggz)

if [ ! -e "${GGZ_FILES[0]}" ]; then
    echo "Error: Conversion completed, but no .ggz files were found in $ABS_OUTPUT"
    exit 1
fi

for file in "${GGZ_FILES[@]}"; do
    filename="$(basename "$file")"
    echo "----------------------------------------"
    echo "Validating $filename..."
    echo "----------------------------------------"

    echo "[*] Running ggz_verify..."
    $RUNTIME run --rm \
        -v "$ABS_OUTPUT:/data/output:Z" \
        --entrypoint /ggz-tools/ggz_verify.py \
        "$IMAGE_NAME" \
        "/data/output/$filename"
done

echo "Verification complete. All GGZ archives passed checks."
