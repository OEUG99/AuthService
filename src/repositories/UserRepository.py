from FlaskServicesDependencies.AbstractRepoistory import AbstractRepository


class UserRepository(AbstractRepository):

    def __init__(self, db):
        self.db = db

        self.create_table()


    def create_table(self):
        try:
            self.db.query("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(255) PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """)
        except Exception as e:
            print("Error while creating the 'users' table:", e)

    def add(self, user):
        self.db.query("""
            INSERT INTO users (id, username, password)
            VALUES (%s, %s, %s)
        """, (user.id, user.email, user.password))


    def update(self, user):
        pass

    def delete(self, user):
        pass

    def get(self, id):
        pass

    def get_all(self):
        pass

    def get_by_username(self, username):
        result = self.db.query("""
            SELECT * FROM users WHERE username = %s
        """, (username,))

        if result:
            return result[0]
        else:
            return None

    def check_password(self, username, password):

        result = self.db.query("""
            SELECT * FROM users WHERE username = %s AND password = %s
        """, (username, password))

        return result


