FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    cmake \
    build-essential \
    libxml2-dev \
    libzip-dev \
    zlib1g-dev

RUN git clone https://github.com/brandl-muc/ggz-tools.git /ggz-tools
RUN chmod +x /ggz-tools/ggz_verify.py /ggz-tools/gpx2ggz.py
ENV PATH="$PATH:/ggz-tools"
#RUN ggz_verify.py -h

# Copy python script
COPY src/converter.py /app/converter.py

# Set non-buffered output for real-time logging
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "/app/converter.py"]
