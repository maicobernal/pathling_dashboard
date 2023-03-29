# Use Python 3.8.16-bullseye as base image
FROM python:3.8.16-bullseye

# Set the working directory
WORKDIR /

# Update APT and install required system packages
RUN apt-get update
RUN apt-get install -y git wget openjdk-11-jdk


# Update pip and install required Python libraries
RUN python -m pip install --upgrade pip

# Install required Python libraries from requirements.txt
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Clone the Synthea repository
WORKDIR /
RUN git clone https://github.com/synthetichealth/synthea.git
RUN wget -O synthea/synthea-with-dependencies.jar https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar

# Clean up APT
RUN apt-get clean

# Set the command to run the Dash app
CMD ["python", "dash/app.py"]
