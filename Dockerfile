# Use the official Python base image (requirement)
FROM python:3.12-slim

# Install system fonts needed by Pillow to draw text
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Set working directory (requirement)
WORKDIR /app

# Copy dependency list first (important for caching)
COPY requirements.txt .

# Install Python dependencies (requirement)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container (requirement)
COPY . .

# Set environment variables (requirement)
ENV PORT=5000

# Expose the port the Flask app uses (requirement)
EXPOSE 5000

# Run the application (requirement)
CMD ["python", "app.py"]
