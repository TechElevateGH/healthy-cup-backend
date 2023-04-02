# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=/app/app/main.py
ENV FLASK_ENV=development
ENV DATABASE_URL=postgres://healthycup:password@postgres:5432/healthycup

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
