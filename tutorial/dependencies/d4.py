# DEPENDENCIES IN PATH OPERATION DECORATORS
# Yani:
# "Dependency çalışsın ama fonksiyona parametre olarak geçmesin"

from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

# 1) TOKEN DOĞRULAMA DEPENDENCY'Sİ
# Bu fonksiyon, request header'ındaki X-Token değerini kontrol eder.
# Eğer değer yanlışsa hata fırlatır.
# Bu fonksiyon bir şey döndürmez — yalnızca kontrol yapar.

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")



# 2) KEY DOĞRULAMA DEPENDENCY'Sİ
# Bu da X-Key header'ını kontrol eder.
# Dönerken bir değer döndürür ama decorator kullanımında bu değer kullanılmaz.

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# 3) ENDPOINT — DECORATOR'DA DEPENDENCIES KULLANIMI
# Bu endpoint'in kendisi hiçbir parametre almaz.
# Ama decorator içindeki dependencies listesi sayesinde:
#   - verify_token()
#   - verify_key()
# endpoint çalışmadan ÖNCE çalıştırılır.
# Eğer bir tanesi hata fırlatırsa, fonksiyon hiç çağrılmaz.

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    # Burada artık token veya key kontrolünden geçmiş oluyoruz.
    return [{"item": "Foo"}, {"item": "Bar"}]


# NOT:
# Bu yöntem, özellikle token/key doğrulama gibi "kontrol" amaçlı
# dependency'lerde çok işe yarar.
# Çünkü dependency'nin döndürdüğü değeri kullanmıyoruz,
# sadece çalışmasını istiyoruz.
