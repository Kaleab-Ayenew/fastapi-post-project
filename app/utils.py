from passlib.context import CryptContext
hasher = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash(password):
    return hasher.hash(password)


def verify(plain_password, hashed_password):
    return hasher.verify(plain_password, hashed_password)
