FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code and CSV file
COPY university-list-service.py /app/
COPY universities.csv /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

# Expose port
EXPOSE 4200

# Run
CMD ["python", "university-list-service.py"]