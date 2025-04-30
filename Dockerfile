# Use the official Python image matching your version
FROM python:3.9.13-slim

# Set environment variables (equivalent to envVars in render.yaml)
ENV IMAGE_STORAGE=/data/images
ENV THUMBNAIL_STORAGE=/data/thumbnails

# Create directories for disk storage
RUN mkdir -p /data/images /data/thumbnails

# Set working directory
WORKDIR /app

# Copy requirements first (caching optimization)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY app .

# Expose the port Gunicorn will use
EXPOSE 10000

# Start command (equivalent to startCommand in render.yaml)
CMD ["gunicorn", "main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:10000"]