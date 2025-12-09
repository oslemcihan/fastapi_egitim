#FASTAPI — PATH PARAMETERS & VALIDATIONS 

from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

# 1) Basit Path Parametresi Kullanımı

"""
item_id → path parametresidir. URL'den alınır:
    /items/10
Path parametreleri her zaman zorunludur.
"""

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}



# 2) Path Parametresine Metadata Ekleme (title)

"""
Path() ile açıklama, başlık ekleyebiliriz.
Bu bilgi otomatik olarak dokümantasyonda görünür.
"""

@app.get("/items/info/{item_id}")
async def get_item_with_title(
    item_id: Annotated[int, Path(title="The ID of the item to retrieve")]
):
    return {"item_id": item_id}



# 3) Path + Query Birlikte Kullanımı

"""
Query parametresine alias ekliyoruz: item-query
URL:
    /items/5?item-query=hello
"""

@app.get("/items/query/{item_id}")
async def get_item_with_query(
    item_id: Annotated[int, Path(title="Item ID")],
    q: Annotated[str | None, Query(alias="item-query")] = None
):
    result = {"item_id": item_id}
    if q:
        result["q"] = q
    return result



# 4) Sayısal Doğrulama — ge (greater or equal)

"""
item_id >= 1 olmalıdır.
Yani 0, -1, -5 gibi değerler kabul edilmez.
"""

@app.get("/items/min/{item_id}")
async def get_item_min(
    item_id: Annotated[int, Path(ge=1)]
):
    return {"item_id": item_id}



# 5) Sayısal Doğrulama — gt & le (büyük, küçük veya eşit)

"""
item_id > 0 ve item_id <= 1000 olmalıdır.
"""

@app.get("/items/range/{item_id}")
async def get_item_range(
    item_id: Annotated[int, Path(gt=0, le=1000)]
):
    return {"item_id": item_id}



# 6) Float Değerlerde Doğrulama

"""
size parametresi float olmalı,
0 < size < 10.5 olmalıdır.
"""

@app.get("/items/{item_id}/size")
async def get_item_with_size(
    *,
    item_id: Annotated[int, Path(ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)]
):
    result = {"item_id": item_id, "q": q, "size": size}
    return result

"""
Bu yukarıdaki * ın anlamı;
Bu yıldızdan sonra gelen parametreler KUVVETLE query parametresi olmak zorundadır.
Yani:
item_id → path parametresi
q → query param
size → query param
Eğer * olmazsa Python q ve size'i positional olarak algılayabilir.
"""


# 7) Parametre Sırası Önemsizdir

"""
FastAPI parametreleri adıyla tanır.
O yüzden sıralama önemli değildir.
Aşağıdaki gibi yazmak tamamen geçerlidir:
"""

@app.get("/items/order/{item_id}")
async def order_example(
    q: str,
    item_id: Annotated[int, Path(title="Order example ID")]
):
    return {"item_id": item_id, "q": q}

