#!/usr/bin/env bash
set -e

# --- STEP 1: Strict check for mounted /work directory ---
if [ ! -d "/work" ] || ! touch /work/.write_test 2>/dev/null; then
    echo "=================================================" >&2
    echo "ERROR: /work is not mounted or is not writable!" >&2
    echo "Aborting build." >&2
    echo "=================================================" >&2
    exit 1
fi
rm -f /work/.write_test

# --- STEP 2: Parse arguments ---
COUNTRY=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --country)
            COUNTRY="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z "$COUNTRY" ]; then
    echo "ERROR: No --country argument supplied."
    exit 1
fi

COUNTRY_LOWER=$(echo "$COUNTRY" | tr '[:upper:]' '[:lower:]')

# Persistent cache directory on mounted volume
CACHE_DIR="/work/cache"
mkdir -p "$CACHE_DIR"

BUILD_DIR="/work/build"
mkdir -p "$BUILD_DIR"

# --- Calculate dynamic memory and thread allocation ---
MEM_KB=$(awk '/MemTotal:/ {print $2}' /proc/meminfo)
MEM_MB=$(( MEM_KB / 1024 ))
CPU_CORES=$(nproc)

# Target ~1500MB RAM per parallel rendering job to prevent OOM
SAFE_JOBS=$(( MEM_MB / 1500 ))
if [ "$SAFE_JOBS" -lt 1 ]; then SAFE_JOBS=1; fi
if [ "$SAFE_JOBS" -gt "$CPU_CORES" ]; then SAFE_JOBS=$CPU_CORES; fi

echo "=== Starting map build process for: ${COUNTRY} ==="
echo "System memory: ${MEM_MB} MB | Cores: ${CPU_CORES} | Allocating 85% RAM to Java JVM | Max Jobs: ${SAFE_JOBS}"

# --- STEP 3: Download OSM data (cached) ---
OSM_PBF="${CACHE_DIR}/${COUNTRY_LOWER}-latest.osm.pbf"
GEOFABRIK_URL="https://download.geofabrik.de/europe/${COUNTRY_LOWER}-latest.osm.pbf"

if [ -f "$OSM_PBF" ]; then
    echo "Found cached OSM data at ${OSM_PBF}. Checking for newer version..."
    wget -N --show-progress -P "$CACHE_DIR" "$GEOFABRIK_URL" || true
else
    echo "Downloading OSM data from ${GEOFABRIK_URL}..."
    if ! wget --show-progress -P "$CACHE_DIR" "$GEOFABRIK_URL"; then
        echo "Trying root Geofabrik URL..."
        GEOFABRIK_URL="https://download.geofabrik.de/${COUNTRY_LOWER}-latest.osm.pbf"
        wget --show-progress -P "$CACHE_DIR" "$GEOFABRIK_URL"
    fi
fi

cd "$BUILD_DIR"

# --- STEP 4: Extract bounding box & generate contours ---
echo "Calculating bounding box..."

parse_bbox() {
    python3 -c "
import sys, re
text = sys.stdin.read()
match = re.search(r'(?:Bounding\s+box|Box):[^\n]+', text, re.IGNORECASE)
if match:
    numbers = re.findall(r'[-+]?\d+\.?\d*', match.group(0))
    if len(numbers) >= 4:
        print(f'{numbers[0]}:{numbers[1]}:{numbers[2]}:{numbers[3]}')
        sys.exit(0)
sys.exit(1)
"
}

BBOX=$(osmium fileinfo "$OSM_PBF" | parse_bbox || true)

if [ -z "$BBOX" ]; then
    echo "Header bbox missing or unparseable. Scanning full file with osmium fileinfo -e..."
    BBOX=$(osmium fileinfo -e "$OSM_PBF" | parse_bbox)
fi

echo "Bounding box found: ${BBOX}"
echo "Generating 10m contour lines using pyhgtmap (ViewfinderPanoramas)..."
pyhgtmap --pbf \
    --step=10 \
    --line-cat=100,20 \
    -a "$BBOX" \
    --sources=view3,view1 \
    -o lonlat_contour

# --- STEP 5: Split OSM file only ---
echo "Splitting OSM PBF into tile sizes..."
java -XX:+UseContainerSupport -XX:MaxRAMPercentage=85.0 -jar /opt/splitter/splitter.jar \
    --output=pbf \
    --max-nodes=1200000 \
    "$OSM_PBF"

# --- STEP 6: Compile final Garmin .img with hiking/routing optimizations ---
echo "Compiling Garmin map image (OSM tiles + contour tiles)..."
java -XX:+UseContainerSupport -XX:MaxRAMPercentage=85.0 -jar /opt/mkgmap/mkgmap.jar \
    --max-jobs="$SAFE_JOBS" \
    --style-file=/app/style \
    --latin1 \
    --route \
    --add-pois-to-lines \
    --add-pois-to-areas \
    --index \
    --gmapsupp \
    --family-id=6500 \
    --product-id=1 \
    --series-name="OSM Topo Hiking - ${COUNTRY}" \
    --family-name="Topo ${COUNTRY}" \
    --area-name="${COUNTRY}" \
    --description="OSM ${COUNTRY} Topo Hiking" \
    --draw-priority=25 \
    --show-profiles \
    --process-destination \
    --process-exits \
    -c template.args lonlat_contour*.pbf /app/hiking.typ

# Move compiled map to /work root
OUTPUT_FILE="/work/${COUNTRY_LOWER}_topo_hiking.img"
mv gmapsupp.img "$OUTPUT_FILE"

# Cleanup build workspace (keep cache intact)
rm -rf "$BUILD_DIR"

echo "================================================="
echo "SUCCESS! Map compiled: ${OUTPUT_FILE}"
echo "================================================="
