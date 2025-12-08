# SECURITY - FIRST STEPS
# Bu dosya OAuth2 Password Flow ile Bearer token alan
# temel güvenlik sisteminin nasıl çalıştığını gösterir.


from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

# FastAPI uygulaması
app = FastAPI()

# 1) OAuth2PasswordBearer
# tokenUrl="token" -> Frontend kullanıcı adı + şifreyi bu
# adrese göndererek token isteyecek.
# Bu endpointi daha sonra yazacağız.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 2) Bu endpoint'e erişebilmek için Bearer token gerekli.
# FastAPI gelen isteğin Authorization header'ını kontrol eder:
#   Authorization: Bearer <token>
# Token varsa "token" parametresine string olarak gelir.
# Token yoksa API otomatik olarak 401 döndürür.

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):

    # Burada token doğrulaması yapılmadı.
    # Sadece token'ı okuyup geri döndürüyoruz.
    return {"token": token}