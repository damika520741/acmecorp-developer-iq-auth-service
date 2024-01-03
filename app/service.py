from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import encode
from fastapi import HTTPException, status
from model import User
from database import connection
from database import INSERT_APPLICATION_USER, SELECT_APPLICATION_USER_BY_USERNAME

KEY = "acmecorp-developer-iq-secret-key"

ALGORITHM = "HS256"

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def signup(user: User):
    try:
        await connection.connect()
        result = await connection.fetch_one(
            SELECT_APPLICATION_USER_BY_USERNAME, values=dict(username=user.username)
        )
        if result:
            return dict(
                is_success=False,
                status_code=status.HTTP_200_OK,
                message="This username already exists.",
                data=None
            )
        else:
            password = hash_password(user.password)
            result = await connection.fetch_one(
                INSERT_APPLICATION_USER, values=dict(username=user.username, password=password)
            )
            if result:
                return dict(
                    is_success=True,
                    status_code=status.HTTP_200_OK,
                    message="You have registerd successfuly.",
                    data=user.username
                )
    except HTTPException as e:
        return dict(
            is_success=False,
            status_code=e.status_code,
            message=e.args[1-1] if e.args else None,
            data=None
        )
    finally:
        await connection.disconnect()

async def signin(user: User):
    try:
        await connection.connect()
        result = await connection.fetch_one(
            SELECT_APPLICATION_USER_BY_USERNAME, values=dict(username=user.username)
        )
        if result:
            if verify_password(user.password, result["password"]):
                token = generate_token(user.username)
                return dict(
                    is_success=True,
                    status_code=status.HTTP_200_OK,
                    message="You have logged in successfuly.",
                    data=dict(token=token, type="bearer")
                )
            else:
                return dict(
                    is_success=False,
                    status_code=status.HTTP_200_OK,
                    message="Password is incorrect.",
                    data=None
                )
        else:
            return dict(
                is_success=False,
                status_code=status.HTTP_200_OK,
                message="Username is incorrect.",
                data=None
            )
    except HTTPException as e:
        return dict(
            is_success=False,
            status_code=e.status_code,
            message=e.args[1-1] if e.args else None,
            data=None
        )
    finally:
        await connection.disconnect()

def hash_password(secret: str):
    return crypt.hash(secret)

def verify_password(secret: str, hash: str):
    return crypt.verify(secret, hash)

def generate_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=21)
    payload = dict(sub=username, exp=expire)
    return encode(payload, KEY, ALGORITHM)