from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def filter_nones(body):
    """Filter out keys with values as None
    body - a pydantic schema
    """
    result = {}
    for key in body:
        if body[key] is not None:
            result[key] = body[key]

    return result


def hashed(password: str):
    return pwd_context.hash(password)


def verify(attempted_password, usr_password):
    return pwd_context.verify(attempted_password, usr_password)


# print(hashed("12345pass"))
