import datetime
import json
import jwt
from flask import Flask, request, Response
from src.connectors.AmazonSecretsManager import AmazonSecretsManager
from src.connectors.AuthDBConnection import AuthDBConnection
from src.models.User import User
from src.repositories.UserRepository import UserRepository
from flask_cors import CORS

allowed_origins = ['http://localhost:3000']
app = Flask(__name__)
CORS(app, origins=allowed_origins)


def generateToken(user):
    # Getting values ready to be embedded in the JWT token
    userID = user.id
    expiration_date = datetime.datetime.today() + datetime.timedelta(days=1)  # 1 day expiration

    # Getting secret key from AWS
    secret_name = "prod/authservice/jwt"
    region = "us-east-1"
    secret_key = AmazonSecretsManager(secret_name, region).get_secret("JWT_SECRET_KEY")

    token = jwt.encode({'user_id': userID, 'exp': expiration_date},
                       secret_key, algorithm="HS256")

    # Deleting secret key from memory to avoid memory attacks, or leakage w/ overflows.
    del secret_key

    return token


@app.route('/api/v1/auth/register', methods=['POST'])
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

    # Checking if the username is already taken
    if UserRepository(AuthDBConnection()).get_by_username(username):
        return Response(response="Username already taken",
                        status=status_code)

    # Creating the user in the DB
    try:
        user = User(username, raw_password)
        UserRepository(AuthDBConnection()).add(user)
        token = generateToken(user)
        status_code = 200
        return Response(response=json.dumps({'token': token}),
                        status=status_code)
    except ValueError as e:
        return Response(response=str(e),
                        status=status_code)


@app.route('/api/v1/auth/login', methods=['POST'])
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

    # Check if the user exists in the database
    userTuple = UserRepository(AuthDBConnection()).get_by_username(username)

    if not userTuple:
        return Response(response="Invalid username or password",
                        status=status_code)

    user = User(id=userTuple[0],
                username=userTuple[1],
                password=userTuple[2])

    # Check if the password is correct
    hashed_password = user.password
    if not UserRepository(AuthDBConnection()).check_password(username, hashed_password):
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


@app.route('/api/v1/auth/validate', methods=['POST'])
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
    secret_key = AmazonSecretsManager(secret_name, region).get_secret("JWT_SECRET_KEY")

    # Decoding the token, if it's valid, return a 200 response
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])

        # Deleting secret key from memory to avoid memory attacks, or leakage w/ overflows.
        del secret_key

        status_code = 200
        return Response(status=status_code)

    except jwt.ExpiredSignatureError:
        return Response(response="Token expired",
                        status=status_code)
    except jwt.DecodeError:
        return Response(response="Invalid token", status=status_code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
