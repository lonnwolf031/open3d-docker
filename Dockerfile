# syntax=docker/dockerfile:1
# Distro could also be another ubuntu or debian based
FROM ubuntu:20.10
WORKDIR /usr/src/app
COPY /src /usr/src/app
# Install Open3D system dependencies and pip
RUN apt-get update && apt-get install --no-install-recommends -y \
    libgl1 \
    libgomp1 \
    libusb-1.0-0 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Open3D from the pypi repositories
RUN python3 -m pip install --no-cache-dir --upgrade open3d
#CMD ["/bin/sh"]
#CMD "python main.py"
#ENTRYPOINT ["python3"]
CMD ["python", "src/main.py"]
# Replacing CMD with ENTRYPOINT
#ENTRYPOINT ["/usr/local/bin/youtube-dl"]

