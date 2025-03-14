FROM python:3.9-slim

# Install necessary system packages and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends libexpat1 && \
    pip install geopandas rasterio && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY ras2vec.py /app/ras2vec.py

# Set the ENTRYPOINT to the Python script
ENTRYPOINT ["python", "/app/ras2vec.py"]
