# Use the official Python image from the Docker Hub
FROM python:3.12.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright chromium
RUN on_startup.sh

# Copy the rest of the application code into the container
COPY . .

# Expose the port the application runs on
EXPOSE 8080

# Specify the command to run the application
CMD ["fastapi", "run", "main.py", "--port", "8080"]