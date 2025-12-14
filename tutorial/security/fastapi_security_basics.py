# FASTAPI SECURITY — TEMEL GÜVENLİK KAVRAMLARININ ÖRNEĞİ
# Bu dosya OAuth2, Bearer Token, OpenAPI güvenlik şemalarının
# nasıl çalıştığını en basit örneklerle açıklar.


from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# 1) OAuth2PasswordBearer -> Authorization: Bearer <token>. header' ını okumak için hazır bir sınıf
# Bu, "Authorization: Bearer <token>" header'ından token alır.
# Bir login endpoint'i ileride token üretecek.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #token /login endpointidnde aınacağını söyler aynı zamanda Swagger de "Authorize" butonunun çalışmasını sağlar.


# 2) TOKEN DOĞRULAMA DEPENDENCY'Sİ
# Bir token alır ve doğrular gibi davranır.
# Gerçek doğrulama JWT vb. sonraki bölümlerde yapılır.

async def verify_token(token: str = Depends(oauth2_scheme)):
    if token != "super-secret-token":
        raise HTTPException(status_code=401, detail="Token geçersiz")
    return token


# 3) KORUNMUŞ ENDPOINT
# Bu endpoint'e sadece geçerli token ile erişilir.

@app.get("/secure-data")
async def secure_data(token: str = Depends(verify_token)):
    return {
        "message": "Gizli veriye eriştin!",
        "token": token
    }


# 4) LOGIN ENDPOINT (sonraki bölümlerde detaylandıracağız)
# Bu endpoint kullanıcıdan şifre alıp token dönecek.

@app.post("/login")
async def login():
    # Normalde username/password kontrol edilir
    return {"access_token": "super-secret-token", "token_type": "bearer"}
