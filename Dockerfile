# Use Ubuntu as base image for better hardware support
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 inference && \
    mkdir -p /app/models && \
    chown -R inference:inference /app

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY inference.py .

# Make the script executable
RUN chmod +x inference.py

# Switch to non-root user
USER inference

# Create volume mount points for models and configs
VOLUME ["/app/models", "/app/configs"]

# Expose port for potential web interface (future enhancement)
EXPOSE 8000

# Default command - run inference with help
CMD ["python3", "inference.py", "--help"]