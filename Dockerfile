# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
# COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 5000 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV NAME HealthyCup

# Run app.py when the container launches
CMD ["flask", "run"]
