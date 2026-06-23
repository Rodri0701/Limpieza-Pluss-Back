import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

SECRET_KEY = "La roca_no_tiene_pelo_o_el_pelo_es_muy_debil_para_la_roca"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


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


def crear_token_acceso(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)