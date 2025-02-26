# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

RUN mkdir /cache

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
