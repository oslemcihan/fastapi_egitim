# main.py — FASTAPI + OAuth2 Password Flow + JWT + Argon2
# Bu dosya gerçek projelerde kullanılabilir güvenli bir örnektir.


from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt  # JWT üretme/doğrulama paketi
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash  # Argon2 tabanlı güvenli hashing kütüphanesi
from pydantic import BaseModel


# 1) GÜVENLİK AYARLARI


# SECRET_KEY token imzalamak için gereklidir.
# Terminalde şu komutla kendin üretmelisin:
#   openssl rand -hex 32
SECRET_KEY = "BURAYA_KENDI_SECRET_KEY_INI_TAM_OLARAK_YAZ"  

# JWT algoritması (HS256 en yaygın olanı)
ALGORITHM = "HS256"

# Token kaç dakika geçerli olacak?
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 2) SAHTE VERİTABANI — hashed_password artık Argon2 hash'i

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        # Argon2 ile hashlenmiş "secret" parolası
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}


# 3) PYDANTIC MODELLER

class Token(BaseModel):
    """Token endpoint'inin döndüğü JSON model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT içindeki sub alanındaki username'i tutar."""
    username: str | None = None


class User(BaseModel):
    """Frontend'e döndürülen kullanıcı modeli."""
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """Sadece veritabanında bulunan alanlar (hashed_password)."""
    hashed_password: str



# 4) PASSWORD HASHING (Argon2)

password_hash = PasswordHash.recommended()  # En güvenli Argon2 ayarları

def verify_password(plain_password, hashed_password):
    """Kullanıcı girdiği şifre doğru mu?"""
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Yeni kullanıcı oluştururken şifreyi hashler."""
    return password_hash.hash(password)



# 5) KULLANICI FONKSİYONLARI

def get_user(db, username: str):
    """DB’den kullanıcıyı çeker ve modele çevirir."""
    if username in db:
        return UserInDB(**db[username])


def authenticate_user(fake_db, username: str, password: str):
    """
    Login işleminde:
    - kullanıcı var mı?
    - şifre doğru mu?
    Kontrol eder.
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



# 6) JWT ÜRETME FONKSİYONU

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    data → {"sub": username}
    expires_delta → token süresi
    """
    to_encode = data.copy()

    # Bitiş zamanı hesapla
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    # Token üret
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# 7) OAuth2 PASSWORD FLOW

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 8) TOKEN'I DOĞRULAYAN DEPENDENCY

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Authorization: Bearer <token> header’ından token gelir.
    JWT çözülür → kullanıcı bulunur.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kimlik doğrulama hatası: token doğrulanamadı.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # JWT doğrula
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")  # JWT'deki kullanıcı adı
        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(fake_users_db, username)
    if not user:
        raise credentials_exception

    return user



# 9) KULLANICI AKTİF Mİ?

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Kullanıcı aktif değilse API’yi kullanamaz."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Kullanıcı pasif!")
    return current_user



# 10) LOGIN ENDPOINT — TOKEN ÜRETİR

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:

    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre yanlış!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Token süresi
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # JWT üret
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=expires,
    )

    return Token(access_token=access_token, token_type="bearer")



# 11) TOKEN İLE KULLANICI BİLGİSİ ALMA

@app.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user



# 12) ÖRNEK: SADECE TOKEN İLE ERİŞİLEBİLEN ENDPOINT

@app.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Item1", "owner": current_user.username}]
