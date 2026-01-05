FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Pillow and ReportLab
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    fontconfig \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables should be passed at runtime
# CMD runs the Polling Bot
CMD ["python", "run_bot.py"]
