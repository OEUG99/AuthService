FROM python:3.9

# Safely setting the environment variables to avoid them being exposed in the image
ARG AWS_SECRET_KEY_NAME
ENV AWS_SECRET_KEY_NAME=$AWS_SECRET_KEY_NAME

ARG MYSQL_ROOT_PASSWORD
ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD

ARG MYSQL_USER
ENV MYSQL_USER=$MYSQL_USER

ARG MYSQL_PASSWORD
ENV MYSQL_PASSWORD=$MYSQL_PASSWORD

ARG CONSUL_IP
ENV CONSUL_IP=$CONSUL_IP

ARG SERVICE_IP
ENV SERVICE_IP=$SERVICE_IP

ARG SERVICE_PORT
ENV SERVICE_PORT=$SERVICE_PORT

# Installing the AWS CLI package and setting up the credentials
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN
ARG AWS_REGION
ARG AWS_OUTPUT

RUN pip install awscli
RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
RUN aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY

# Setting up git credientials to access private repos, via environment variable from host machine as build argument
ARG GIT_TOKEN

RUN git config --global URL."https://$GIT_TOKEN:@github.com/".insteadOf "https://github.com/"

# Setting the working directory and copy the application code from the host machine.
COPY ./src/ ./app/src/
COPY ./requirements.txt ./app/requirements.txt
WORKDIR /app/

# Installing the Python dependencies.
RUN pip install -r requirements.txt

# Exposing the application port.
EXPOSE $SERVICE_PORT

# Start the application using Gunicorn.
WORKDIR /app/src/
CMD gunicorn -b 0.0.0.0:$SERVICE_PORT --workers 4 app:app
