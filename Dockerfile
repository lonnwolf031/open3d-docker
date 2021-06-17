# syntax=docker/dockerfile:1
# This could also be another ubuntu or debian based distributions
FROM ubuntu:20.10
WORKDIR /app
# Install Open3D system dependencies and pip
RUN apt-get update && apt-get install --no-install-recommends -y \
    libgl1 \
    libgomp1 \
    libusb-1.0-0 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Open3D from the pypi repositories
RUN python3 -m pip install --no-cache-dir --upgrade open3d

# RUN make /app
 #CMD ["python", "app/app.py"]
