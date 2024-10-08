from passlib.hash import bcrypt


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def get_password_hashed(password):

    return bcrypt.hash(password)
