# Use an official Python image
FROM python:3.9

# Switch to root for installing packages
USER root

# Add docker group and add jenkins user to it
RUN groupadd -g 1001 docker && usermod -aG docker jenkins

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the cloned repo to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch back to jenkins user for running the application
USER jenkins

# Set the default command to run the script
CMD ["python", "match_script.py"]
