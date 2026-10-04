FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install base toolchain & Python GDAL/Matplotlib dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-bs4 \
    python3-matplotlib \
    python3-gdal \
    python3-numpy \
    gdal-bin \
    wget \
    curl \
    unzip \
    osmium-tool \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install pyhgtmap (actively maintained drop-in replacement for phyghtmap)
RUN pip3 install --break-system-packages pyhgtmap

# Download and install latest mkgmap and splitter
WORKDIR /opt
RUN MKGMAP_VER=$(curl -s https://www.mkgmap.org.uk/download/mkgmap.html | grep -oP 'mkgmap-r\d+' | head -1) && \
    wget -q https://www.mkgmap.org.uk/download/${MKGMAP_VER}.zip && \
    unzip -q ${MKGMAP_VER}.zip && \
    mv ${MKGMAP_VER} mkgmap && \
    rm ${MKGMAP_VER}.zip

RUN SPLITTER_VER=$(curl -s https://www.mkgmap.org.uk/download/splitter.html | grep -oP 'splitter-r\d+' | head -1) && \
    wget -q https://www.mkgmap.org.uk/download/${SPLITTER_VER}.zip && \
    unzip -q ${SPLITTER_VER}.zip && \
    mv ${SPLITTER_VER} splitter && \
    rm ${SPLITTER_VER}.zip

# Copy execution script inside the container image for isolated execution
WORKDIR /app
COPY build_map.sh /app/build_map.sh
RUN chmod +x /app/build_map.sh

COPY hiking.txt /app/hiking.txt
COPY style/ /app/style/
# Compile TYP file first if hiking.txt exists
RUN java -jar /opt/mkgmap/mkgmap.jar --family-id=6500 --product-id=1 hiking.txt

ENTRYPOINT ["/app/build_map.sh"]
