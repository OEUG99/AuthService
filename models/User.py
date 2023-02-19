import uuid
import bcrypt
from libraries.FlaskRESTServiceLayer.models.AbstractEntity import AbstractEntity
import re


class User(AbstractEntity):
    id = None
    username = None
    raw_password = None

    def __init__(self, username, password, id=None):

        if id is not None:
            # if an id is provided, we can assume the password is hashed.
            # This is used when we are getting a user from the database.
            self.id = id
            self.username = username
            self.password = password
            return

        if not self.validateUsername(username):
            raise ValueError("Username does not meet the minimum requirements.")

        if self.validatePassword(password):
            raise ValueError("Password does not meet the minium requirements. Passwords Must have at least 8 "
                             "characters, one uppercase letter, one lowercase letter, one number, and one special "
                             "character. It also can not be longer then 100 characters.")

        self.id = str(uuid.uuid4())
        self.username = username
        self.password = self.__hashPassword(password)

    def validateUsername(self, username) -> bool:
        """
        Validates the username meets the minimum requirements.
        :param username:
        :type username:
        :return:
        :rtype:
        """
        # default return value for now since no requirements are set.
        return True

    def validatePassword(self, raw_password) -> bool:

        print(len(raw_password))

        # Password must be at least 8 characters long
        if len(raw_password) >= 8:
            return False

        # Password not be longer then 50 characters
        if len(raw_password) > 50:
            return False

        # Password must contain at least one uppercase letter and one lowercase letter and one number
        # and one special character
        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        return password_pattern.match(raw_password) is not None

    def __hashPassword(self, raw_password) -> str:
        # Hashing passwords with random salt for extra security.
        password_hash = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())
        return password_hash.decode()  # returning hash with salt.

    def __repr__(self):
        return '<User %r>' % self.username
