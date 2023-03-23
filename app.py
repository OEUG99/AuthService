import datetime
import os
import jwt
from flask import Flask, request, Response
from FlaskServicesDependencies.DatabaseManager import DatabaseManager
from FlaskServicesDependencies.MySQLStrategy import MySQLStrategy
from FlaskServicesDependencies.AmazonSecretsManager import AmazonSecretsManager
from src.models.User import User
from src.repositories.UserRepository import UserRepository
from flask_redis import FlaskRedis
import json

app = Flask(__name__)
redis_password = os.environ.get('REDIS_PASSWORD')
app.config['REDIS_URL'] = f'redis://auth-redis:6379/0'
redis_store = FlaskRedis(app)


def generateToken(user) -> str:
    """Generates a JWT Token used for client authorization.

    :param user:
    :type user:
    :return: encoded JWT token
    :rtype:
    """
    # Getting values ready to be embedded in the JWT token
    userID = user.id
    expiration_date = datetime.datetime.today() + datetime.timedelta(days=1)  # 1 day expiration

    # Getting secret key from AWS
    secret_name = "prod/authservice/jwt"
    region = "us-east-1"

    secret_key = redis_store.get('JWT_SECRET_KEY') or None
    if not secret_key:
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key_name = os.environ.get('AWS_SECRET_KEY_NAME')
        secret_key = AmazonSecretsManager(secret_name,
                                          region,
                                          aws_secret_access_key,
                                          aws_session_token,
                                          aws_access_key_id,
                                          aws_secret_key_name).get_secret("JWT_SECRET_KEY")

        redis_store.set('JWT_SECRET_KEY', secret_key, ex=datetime.timedelta(days=1))

    token = jwt.encode({'user_id': userID, 'exp': expiration_date},
                       secret_key, algorithm="HS256")

    # Deleting secret key from memory to avoid memory attacks, or leakage w/ overflows.
    del secret_key

    return token


def getDatabase():
    """
    Determines the database connection based off of env variables.
    TODO: implement env variables for database connection.
    :return:
    :rtype:
    """
    strategy = MySQLStrategy(host="auth-mysql",
                             port=3306,
                             user="root",
                             password=str(os.getenv("MYSQL_ROOT_PASSWORD")),
                             database="auth")
    try:
        connection = DatabaseManager(strategy)
        print("Database connected successfully")
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None


@app.route('/health')
def health() -> Response:
    """The health endpoint is used to check the health of the service. This will be used by Consul.

    :return: HTTP Response
    :rtype: Response
    """
    return Response(response="Healthy!", status=200)


@app.route('/register', methods=['POST'])
def register() -> Response:
    """ The register endpoint is used to create a new user in the database.

    :return: HTTP Response
    :rtype: Response
    """
    status_code = 400
    data = request.get_json()
    username = data.get('username')
    raw_password = data.get('password')

    # validating the username and password exist & formatted properly
    if not (username and raw_password):
        print('Invalid username or password')
        return Response(status=status_code)

    db = getDatabase()

    # Checking if the username is already taken
    if UserRepository(db).get_by_username(username):
        return Response(response="Username already taken",
                        status=status_code)

    # Creating the user in the DB
    try:
        user = User(username, raw_password)
        UserRepository(db).add(user)
        token = generateToken(user)
        status_code = 200
        return Response(response=json.dumps({'token': token}),
                        status=status_code)
    except ValueError as e:
        return Response(response=str(e),
                        status=status_code)


@app.route('/login', methods=['POST'])
def login() -> Response:
    """The login endpoint is used to authenticate a user and return a JWT token.

    :return: HTTP Response
    :rtype: Response
    """
    status_code = 400
    data = request.get_json()
    username = data.get('username')
    raw_password = data.get('password')

    # validating the username and password exist & formatted properly
    if not (username and raw_password):
        print('Invalid username or password')
        return Response(status=status_code)

    db = getDatabase()

    # Check if the user exists in the database
    userTuple = UserRepository(db).get_by_username(username)

    if not userTuple:
        return Response(response="Invalid username or password",
                        status=status_code)

    user = User(id=userTuple[0],
                username=userTuple[1],
                password=userTuple[2])

    # Check if the password is correct
    hashed_password = user.password
    if not UserRepository(db).check_password(username, hashed_password):
        return Response(response="Invalid username or password",
                        status=status_code)
    try:
        token = generateToken(user)
        status_code = 200
        return Response(response=json.dumps({'token': token}),
                        status=status_code)
    except ValueError as e:
        return Response(response=str(e),
                        status=status_code)


@app.route('/validate', methods=['POST'])
def validate() -> Response:
    """ The validate endpoint is used to validate a JWT token.

    :return: HTTP Response
    :rtype: Response
    """
    status_code = 400
    data = request.get_json()
    token = data.get('token')

    # validating the token exists
    if not token:
        return Response(status=status_code)

    # Getting secret key from AWS
    secret_name = "prod/authservice/jwt"
    region = "us-east-1"
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key_name = os.environ.get('AWS_SECRET_KEY_NAME')

    secret_key = AmazonSecretsManager(secret_name,
                                      region,
                                      aws_secret_access_key,
                                      aws_session_token,
                                      aws_access_key_id,
                                      aws_secret_key_name).get_secret("JWT_SECRET_KEY")

    # Decoding the token, if it's valid, return a 200 response
    try:
        tokenDecoded = jwt.decode(token, secret_key, algorithms=["HS256"])

        # Deleting secret key from memory to avoid memory attacks, or leakage w/ overflows.
        del secret_key

        status_code = 200
        return Response(response=json.dumps(tokenDecoded), status=status_code)

    except jwt.ExpiredSignatureError:
        return Response(response="Token expired",
                        status=status_code)
    except jwt.DecodeError:
        return Response(response="Invalid token", status=status_code)


if __name__ == '__main__':
    servicePort = os.environ.get('SERVICE_PORT')
    app.run(host='0.0.0.0', port=servicePort)
