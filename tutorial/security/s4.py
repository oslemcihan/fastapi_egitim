# SIMPLE OAUTH2 PASSWORD FLOW + BEARER TOKEN ÖRNEĞİ
# Tamamen eğitim amaçlıdır. Güvenli değildir.
# Bir sonraki bölümde JWT kullanarak gerçek güvenlik ekleyeceğiz.


from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# 1) SAHTE VERİTABANI

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",  # aslında secret parolasının hashlenmiş hali
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2", # aslında secret2 parolasının hashlenmiş hali
        "disabled": True,  # bu kullanıcı pasif
    },
}

app = FastAPI()

# 2) PAROLA HASH FONKSİYONU (SAHTE)

def fake_hash_password(password: str):
    # Gerçek uygulamada bcrypt veya argon2 kullanılacak!
    return "fakehashed" + password

# 3) OAuth2 şeması — token istemek için /token endpoint'i kullanılacak

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 4) Kullanıcı Modelleri

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str  # sadece DB'de bulunur


# 5) Veritabanından kullanıcıyı alma fonksiyonu

def get_user(db, username: str):
    if username in db:
        return UserInDB(**db[username])


# 6) Token çözme (fake)
# Token olarak username gönderiyoruz, o yüzden username geri dönüyor

def fake_decode_token(token: str):
    return get_user(fake_users_db, token)


# 7) Geçerli kullanıcıyı token üzerinden bul

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)

    if not user:
        # Token geçersiz → kullanıcı yok
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


# 8) Kullanıcı aktif mi?

async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



# 9) /token — kullanıcı adı ve şifreyle giriş yapılır

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # username DB’de var mı?
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserInDB(**user_dict)

    # Parola hashleri eşleşiyor mu?
    hashed_password = fake_hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    
    # BAŞARILI LOGIN → TOKEN DÖNDERİLİR
    # Bu örnekte token = username'dir (güvenli değil ama öğretici)
    
    return {"access_token": user.username, "token_type": "bearer"}



# 10) /users/me — giriş yapmış kullanıcı bilgilerini döner

@app.get("/users/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
