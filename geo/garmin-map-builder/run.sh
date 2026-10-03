#!/usr/bin/env bash
set -e

IMAGE_NAME="garmin-map-builder"
ENGINE="podman"
BUILD_MODE=false
OUT_DIR=""
COUNTRY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --docker)
            ENGINE="docker"
            shift
            ;;
        --build)
            BUILD_MODE=true
            shift
            ;;
        --country)
            COUNTRY="$2"
            shift 2
            ;;
        *)
            if [ -z "$OUT_DIR" ]; then
                OUT_DIR="$1"
                shift
            else
                echo "ERROR: Unknown argument: $1" >&2
                exit 1
            fi
            ;;
    esac
done

# Verify container engine binary exists
if ! command -v "$ENGINE" &> /dev/null; then
    echo "ERROR: '$ENGINE' binary not found in PATH." >&2
    exit 1
fi

# Build image mode
if [ "$BUILD_MODE" = true ]; then
    echo "Building container image '${IMAGE_NAME}' using ${ENGINE}..."
    "$ENGINE" build -t "${IMAGE_NAME}" .
    exit 0
fi

# Validation for run mode
if [ -z "$OUT_DIR" ] || [ -z "$COUNTRY" ]; then
    echo "Usage:"
    echo "  ./run.sh --build [--docker]"
    echo "  ./run.sh <out_dir> --country <CountryName> [--docker]"
    echo ""
    echo "Examples:"
    echo "  ./run.sh out/sweden --country Sweden"
    echo "  ./run.sh out/sweden --country Sweden --docker"
    exit 1
fi

# Ensure output directory exists and resolve absolute path
mkdir -p "$OUT_DIR"
ABS_OUT_DIR="$(cd "$OUT_DIR" && pwd)"

echo "Starting container via ${ENGINE} (mounting ${ABS_OUT_DIR} -> /work)..."

# :rw,z ensures SELinux labeling compatibility under Podman if enabled on host
"$ENGINE" run --rm \
    -v "${ABS_OUT_DIR}:/work:rw,z" \
    "${IMAGE_NAME}" \
    --country "${COUNTRY}"
