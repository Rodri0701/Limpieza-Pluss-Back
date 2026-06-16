import bcrypt

def get_password_hash(password: str) -> str:
    # bcrypt requiere bytes, así que codificamos el string
    pwd_bytes = password.encode('utf-8')
    # Generamos la "sal" (salt) aleatoria
    salt = bcrypt.gensalt()
    # Hasheamos la contraseña
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Lo regresamos como string normal para guardarlo en tu BD
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convertimos ambos strings a bytes para compararlos
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)