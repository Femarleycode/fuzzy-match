#Docker sudo conflict

USER root  
RUN groupadd -g 1001 docker && usermod -aG docker jenkins  
USER jenkins 

# Use an official Python image
FROM python:3.9


# Set the working directory inside the container
WORKDIR /app

# Copy everything from the cloned repo to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the script
CMD ["python", "match_script.py"]
