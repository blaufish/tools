# Garmin Map Builder

Containerized tool for building topographic Garmin GPS map files (`.img`) with routing optimizations and 10m contour lines using OpenStreetMap and DEM elevation data (`pyhgtmap`, `splitter`, `mkgmap`).

## Requirements

* Podman or Docker
* Bash

## Usage Examples

### 1. Build Container Image

```bash
./run.sh --build
```

### 2. Generate Map for a Country

Specify an output directory and the target Geofabrik country name:


```bash
# Sweden
./run.sh out/sweden --country Sweden

# Norway
./run.sh out/norway --country Norway

# Germany
./run.sh out/germany --country Germany
```

Example success generating Sweden (takes a lot of time):

```plain
Thread worker-25 has finished
Distribution pass(es) took 19500 ms
temporary file /work/build/./node10671689651697369282.tmp was deleted
temporary file /work/build/./way11975075349058735266.tmp was deleted
temporary file /work/build/./rel7765700838131530225.tmp was deleted
Time finished: Sat Oct 03 20:12:44 UTC 2026
Total time taken: 1 minute 12 seconds
Compiling Garmin map image (OSM tiles + contour tiles)...
Mkgmap version 4924
Time started: Sat Oct 03 20:12:44 UTC 2026
Number of MapFailedExceptions: 0
Number of ExitExceptions: 0
Time finished: Sat Oct 03 20:14:07 UTC 2026
Total time taken: 1 minute 23 seconds
=================================================
SUCCESS! Map compiled: /work/sweden_topo_hiking.img
=================================================
```

```bash
du -sh out/sweden/sweden_topo_hiking.img
883M    out/sweden/sweden_topo_hiking.img
```

## Output & Caching

* **Compiled Map:** Output is saved to `out/<country>/<country_name>_topo_hiking.img`.
* **OSM Data Cache:** Input files are cached at `out/<country>/cache/` so subsequent builds avoid re-downloading unchanged PBFs.

## Note

Older Garmin GPS:es prefer FAT32 formatting of SD-cards.
