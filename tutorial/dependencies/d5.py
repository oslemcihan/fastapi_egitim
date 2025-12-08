# GLOBAL DEPENDENCIES
# Tüm uygulama için geçerli dependency tanımlama


from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated

# 1) TOKEN DOĞRULAMA FONKSİYONU
# - Header'dan X-Token değerini alır.
# - Eğer beklenen değer değilse hata fırlatır.
# - Bu fonksiyonun return değerine ihtiyacımız yoktur.

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=400,
            detail="X-Token header invalid"
        )

# 2) KEY DOĞRULAMA FONKSİYONU
# - Header'dan X-Key değerini alır.
# - Eğer yanlışsa hata fırlatır.
# - return değeri var ama kullanılmayacak.

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(
            status_code=400,
            detail="X-Key header invalid"
        )
    return x_key  # Yine de dönebilir; global dependency olduğu için kullanılmayacak.


# 3) GLOBAL DEPENDENCY TANIMI
# FastAPI'nin constructor'ına dependencies parametresi veriliyor.
# Burada verilen dependency'ler uygulamadaki HER endpoint için çalışır.
# Artık her endpoint girişinde:
#   - verify_token()
#   - verify_key()
# fonksiyonları çalışır.

app = FastAPI(
    dependencies=[
        Depends(verify_token),
        Depends(verify_key)
    ]
)

# 4) ENDPOINT'LER
# Dikkat edersen fonksiyonlarda dependency yok.
# Yine de global dependency sayesinde her request kontrol edilecektir.

@app.get("/items/")
async def read_items():
    return [
        {"item": "Portal Gun"},
        {"item": "Plumbus"}
    ]


@app.get("/users/")
async def read_users():
    return [
        {"username": "Rick"},
        {"username": "Morty"}
    ]

# ÖZET:
#
# - Bu yapı, tüm API genelinde güvenlik, doğrulama, logging gibi
#   işlemleri zorunlu kılmak için mükemmeldir.
#
# - Yeni eklenen tüm endpoint'lerde otomatik olarak çalışır.
#

