FROM python:3.10.4-slim-buster

# Set the working directory in the container
WORKDIR /home/user

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5973

# Copy the content of the local src directory to the working directory
COPY *.py ./

# Command to run on container start #CMD ["sh"]
CMD [ "waitress-serve", "--port=5973", "--call", "main:create_app" ]

