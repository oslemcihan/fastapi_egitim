# FastAPI Dependency Injection
# Bağımlılıkların nasıl çalıştığını gösteren açıklamalı örnek

from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

# Bağımlılık Fonksiyonu
# Bu fonksiyon query parametrelerinden q, skip, limit
# değerlerini alır ve bir sözlük döner.

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# Annotated alias ile bağımlılığı daha kısa kullanıyoruz
#commons: dict = Depends(common_parameters) -> bunu yapmak yerine:
CommonsDep = Annotated[dict, Depends(common_parameters)]

# Endpoint 1
# FastAPI önce bağımlılığı çalıştırır, sonra endpoint'i.

@app.get("/items/")
async def read_items(commons: CommonsDep):
    """
    commons değişkeni:
    {
        "q": "...",
        "skip": ...,
        "limit": ...
    }
    şeklinde gelir.
    """
    return {"received": commons}


# Endpoint 2
# Aynı bağımlılık tekrar kullanılabiliyor.

@app.get("/users/")
async def read_users(commons: CommonsDep):
    return {"received": commons}


# Bağımlılık Enjeksiyonunun Mantığı:
# 1) İstek gelir
# 2) FastAPI bağımlılık fonksiyonunu çağırır
# 3) Sonucunu endpoint içindeki parametreye verir
# 4) Endpoint çalıştırılır
# Böylece tekrar eden kodlardan kurtulmuş oluruz.