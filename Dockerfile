# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (adjust if needed)
EXPOSE 5000

# Run your app (adjust as per your app)
CMD ["python", "app.py"]
