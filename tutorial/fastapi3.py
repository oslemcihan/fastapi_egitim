#FASTAPI – SORGU PARAMETRELERİ

from fastapi import FastAPI
from typing import Union

app = FastAPI()

# Fake database listesi (örnek)
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
    {"item_name": "Qux"},
]


# 1) BASİT SORGU PARAMETRELERİ

"""
skip ve limit parametreleri URL'de ? işaretinden SONRA gelen
değerlerdir. Yani bunlar bir PATH parametresi değil,
QUERY parametresidir.

Örnek URL:
    /items/?skip=1&limit=2
"""

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    """
    skip -> kaç eleman atlanacak
    limit -> kaç eleman gösterilecek
    İkisi de QUERY parametresidir.
    Varsayılan değerleri olduğu için zorunlu değildir.
    """
    return fake_items_db[skip: skip + limit]
"""Bu fonksiyon: Bir listeden belirli aralıktaki elemanları döndür."""

# 2) İSTEĞE BAĞLI (OPTIONAL) PARAMETRELER

"""
q parametresi QUERY parametresidir.
Varsayılanı None olduğu için isteğe bağlıdır.

Örnek:
    /items/abc?q=hello
veya sadece:
    /items/abc
"""

@app.get("/items/{item_id}")
async def read_item_optional(item_id: str, q: Union[str, None] = None):
    """
    item_id -> PATH parametresi
    q -> QUERY parametresi (isteğe bağlı)
    """
    if q:
        return {"item_id": item_id, "query_param": q}
    return {"item_id": item_id}


# 3) BOOL TİPİNDE SORGU PARAMETRESİ

"""
short parametresi bool türündedir. FastAPI aşağıdaki tüm
değerleri True olarak yorumlar:

1, true, True, on, yes, y, t
ve bunların büyük-küçük harf varyasyonları.

Ör:
    /items/test?short=1
    /items/test?short=true
"""

"""Bilgi:
    /items-bool/5
    Burada 5 → path param’tır.

    /items-bool/5?q=hello
    Burada:
    q = hello → query parametredir.

    Eğer URL’de q varsa → onu JSON’a ekle
"""

@app.get("/items-bool/{item_id}")
async def read_item_bool(
    item_id: str,
    q: Union[str, None] = None,
    short: bool = False
):
    item = {"item_id": item_id}

    if q:
        item["query"] = q

    if not short:
        item["description"] = "Bu eşyanın çok uzun bir açıklaması var."

    return item


############################################################
# 4) ÇOKLU PATH + QUERY PARAMETRESİ
############################################################
"""
FastAPI PATH ve QUERY parametrelerini isimlerine göre ayırt eder.
Sıranın bir önemi yoktur.

Örnek URL:
    /users/7/items/abc?q=test&short=true
"""

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_items(
    user_id: int,
    item_id: str,
    q: Union[str, None] = None,
    short: bool = False
):
    result = {"owner_id": user_id, "item_id": item_id}

    if q:
        result["query"] = q

    if not short:
        result["description"] = "Bu item uzun açıklamalı bir itemdir."

    return result


# 5) ZORUNLU QUERY PARAMETRESİ

"""
Bir QUERY parametresi zorunlu olsun istiyorsan varsayılan
değer vermeyeceksin.

Örnek URL (doğru kullanım):
    /items-required/test?needy=merhaba

Yanlış:
    /items-required/test    -> HATA döner!
"""

@app.get("/items-required/{item_id}")
async def read_required_param(item_id: str, needy: str):
    """
    needy -> zorunlu QUERY parametresidir.
    """
    return {"item_id": item_id, "needy": needy}


# 6) ZORUNLU + İSTEĞE BAĞLI + VARSAYILAN QUERY PARAMETRESİ

"""
needy  -> zorunlu
skip   -> varsayılanı 0
limit  -> isteğe bağlı (None olabilir)
"""

@app.get("/items-mixed/{item_id}")
async def read_mixed_params(
    item_id: str,
    needy: str,                 # ZORUNLU
    skip: int = 0,              # Varsayılan 0
    limit: Union[int, None] = None  # İsteğe bağlı
):
    return {
        "item_id": item_id,
        "needy": needy,
        "skip": skip,
        "limit": limit
    }
