FROM python:3.9-slim

# Install system dependencies first
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    gcc \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Rust using rustup (latest stable)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy your application
COPY . .
# Copy the rules directory
COPY packages /app/packages

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if needed)
EXPOSE 80

# Command to run your app (example)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
