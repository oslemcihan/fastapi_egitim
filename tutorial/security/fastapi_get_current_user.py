# GET CURRENT USER - FASTAPI SECURITY ÖRNEĞİ
# Bu dosya, OAuth2 ile alınan bearer token'dan
# nasıl "mevcut kullanıcı" elde edildiğini gösterir.


from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Uygulamayı oluştur
app = FastAPI()

# 1) OAuth2PasswordBearer
# Bu, Header'daki Authorization: Bearer <token> değerini okur.
# tokenUrl="token" -> kullanıcının kullanıcı adı + şifre göndererek
# token talep edeceği endpoint (sonraki bölümde yazacağız)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 2) Kullanıcı modeli
# Bu, endpoint'te otomatik dönüşüm sağlamak için kullanılır.

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# 3) Sahte token decode fonksiyonu
# Gerçekte JWT decode edilir. Biz burada örnek amaçlı
# token + "fakedecoded" ekleyip User modeli döndürüyoruz.

def fake_decode_token(token: str) -> User:
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe",
        disabled=False
    )


# 4) get_current_user
# - oauth2_scheme sayesinde token alır
# - token'ı decode ederek kullanıcıyı üretir
# - kullanıcı modelini döner
# Bu dependency, gerçek uygulamalarda:
# 1) token doğrulama
# 2) token expiration kontrolü
# 3) kullanıcıyı DB'den çekme
# gibi işlemleri yapar.

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    user = fake_decode_token(token)
    return user


# 5) Kullanıcıyı path fonksiyonuna "current_user" olarak enjekte et

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Artık kullanıcının bilgileri burada
    return current_user
