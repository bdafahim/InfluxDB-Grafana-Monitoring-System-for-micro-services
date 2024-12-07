FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code and CSV file
COPY top-n-university-service.py /app/
COPY requirements.txt /app/

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install -r requirements.txt

# Expose port
EXPOSE 4201
EXPOSE 8086


CMD ["python", "top-n-university-service.py"]