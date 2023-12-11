from databases import Database

INSERT_APPLICATION_USER = """
INSERT INTO application_user (username, password) VALUES (:username, :password) RETURNING *
"""

SELECT_APPLICATION_USER_BY_USERNAME = """
SELECT * FROM application_user WHERE username = :username
"""

url = f"postgresql://postgres:damika@localhost:5432/developer-iq"

connection = Database(url)