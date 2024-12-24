# Use Python 3.11 slim image as the base
FROM python:3.11-slim

# Install dependencies required for Playwright and Xvfb
RUN apt-get update && \
    apt-get install -y \
    wget \
    ca-certificates \
    xvfb \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Install Playwright dependencies
RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install --with-deps  # This installs Chromium for Playwright

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app/API

# Copy the requirements file to the working directory
COPY backend/requirements.txt /app/API/

# Install dependencies from the requirements.txt
RUN pip install -r requirements.txt

# Copy the entire backend folder into the container's /app/API directory
COPY backend/ /app/API

# Set the working directory to /app (where start.sh is located)
WORKDIR /app/API

# Copy start.sh from the same directory as the docker-compose.yml file (not inside /backend)
COPY start.sh /start.sh

# Make the script executable
RUN chmod +x /start.sh
RUN sed -i 's/\r$//' /start.sh

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run service dbus to start the message bus (if needed)
RUN service dbus start

# Use xvfb to run the browser in headed mode with Playwright
CMD ["xvfb-run", "-a", "/start.sh"]
