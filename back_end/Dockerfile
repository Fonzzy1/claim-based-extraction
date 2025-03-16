# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app


RUN apt-get update && apt-get install -y wget tar xz-utils
RUN wget https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz -O /tmp/ffmpeg.tar.xz 
RUN tar -xf /tmp/ffmpeg.tar.xz -C /tmp 
RUN mv /tmp/ffmpeg-master-latest-linux64-gpl/bin/ffmpeg /usr/local/bin/ 
RUN mv /tmp/ffmpeg-master-latest-linux64-gpl/bin/ffplay /usr/local/bin/ 
RUN mv /tmp/ffmpeg-master-latest-linux64-gpl/bin/ffprobe /usr/local/bin/

RUN rm -rf /tmp/ffmpeg /tmp/ffmpeg.tar.xz 

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install  --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
