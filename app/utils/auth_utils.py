from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def verify_password(plain_passowrd: str, hashed_password: str):
    return password_hash.verify(plain_passowrd, hashed_password)


def get_hashed_password(plain_password):
    return password_hash.hash(plain_password)
