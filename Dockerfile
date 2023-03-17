FROM python:3.9

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN
ARG AWS_REGION
ARG AWS_OUTPUT
ARG GIT_TOKEN

ARG AWS_SECRET_KEY_NAME
ENV AWS_SECRET_KEY_NAME=$AWS_SECRET_KEY_NAME

ARG MYSQL_ROOT_PASSWORD
ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD

ARG MYSQL_USER
ENV MYSQL_USER=$MYSQL_USER

ARG MYSQL_PASSWORD
ENV MYSQL_PASSWORD=$MYSQL_PASSWORD

RUN echo $MYSQL_USER


# Install the AWS CLI.
RUN pip install awscli

# Set the working directory and copy the application code
WORKDIR /app
COPY . .

# Set the AWS configuration using environment variables.

RUN chmod 777 install.sh

# setting up git credientials
RUN git config --global URL."https://$GIT_TOKEN:@github.com/".insteadOf "https://github.com/"

# Run the installation script.
RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
RUN aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY

# Install the Python dependencies.
RUN pip install -r requirements.txt

# Expose the application port.
EXPOSE 8001

# Start the application using Gunicorn.
CMD ["gunicorn", "-b", "0.0.0.0:8001", "--workers", "2", "app:app"]
