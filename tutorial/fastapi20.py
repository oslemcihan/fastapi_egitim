#FASTAPI – FORM VERİSİ KULLANIMI
# Bu dosya Form() kullanımını adım adım açıklar.
# Form verisi JSON değildir. Özel olarak kodlanır.
# Bu yüzden Form() kullanmazsan FastAPI form verisini çözemez.
# NOT:
# Form alanlarını kullanabilmek için aşağıdaki paketi kurmalısın:
#     pip install python-multipart

from typing import Annotated
from fastapi import FastAPI, Form

app = FastAPI()

# 1) BASİT FORM ÖRNEĞİ (username + password)

@app.post("/login/")
async def login(
    # Form() → Bu parametrelerin form verisi olduğunu tanımlar.
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    """
    Bu endpoint form verisi kabul eder.
    Eğer Form() kullanmazsan, FastAPI bunları query parametresi sanır.
    """
    return {"username": username}


# 2) Form verisinin JSON’dan farkı
# JSON formatı:
# {
#   "username": "alice",
#   "password": "secret"
# }
# Form formatı:
# username=alice&password=secret
# HTML form veya OAuth2 login işlemleri zorunlu olarak bu formatı kullanır.


# 3) FORM İLE JSON BERABER KULLANILAMAZ


# Aşağıdaki gibi bir şey YAPAMAZSIN:
# async def example(data: Annotated[User, Body()], name: Annotated[str, Form()])
# Çünkü HTTP body aynı anda hem JSON hem Form olamaz.


# 4) Form alanlarında validasyon da yapabilirsin

@app.post("/register/")
async def register(
    email: Annotated[str, Form(min_length=5, max_length=50)],
    password: Annotated[str, Form(min_length=6)]
):
    """
    Form() da Body() ile aynı validasyon özelliklerine sahiptir.
    min_length, max_length, regex vb. ekleyebilirsin.
    """
    return {"email": email}


# 5) TEKNİK DETAYLAR (Özet)
# - Form verisi genelde şu türde gönderilir:
#   application/x-www-form-urlencoded
# - Eğer formda DOSYA varsa:
#   multipart/form-data
#   (Bir sonraki bölüm File Upload bunu anlatır.)
# - Form sınıfı Body() sınıfını miras alır → aynı özellikleri taşır.

