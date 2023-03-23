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

ARG CONSUL_IP
ENV CONSUL_IP=$CONSUL_IP

ARG SERVICE_IP
ENV SERVICE_IP=$SERVICE_IP

ARG SERVICE_PORT
ENV SERVICE_PORT=$SERVICE_PORT

# Install the AWS CLI.
RUN pip install awscli

# Set the working directory and copy the application code
WORKDIR /app
COPY . .
#COPY /configs/* /app/configs/

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
CMD ["python", "service_registry.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8001", "--workers", "4", "app:app", "--preload"]
