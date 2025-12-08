#FASTAPI – REQUEST BODY (İSTEK GÖVDESİ)

from fastapi import FastAPI
from pydantic import BaseModel


# 1) Pydantic Modeli Tanımlama

"""
Request Body, API'nin beklediği veri yapısını ifade eder.
Pydantic modelleri JSON verisini otomatik doğrular.

Bu model şu JSON yapısını temsil eder:

{
    "name": "Kalem",
    "description": "Mavi kalem",
    "price": 10.5,
    "tax": 1.5
}
"""

class Item(BaseModel):
    name: str                         # Zorunlu alan
    description: str | None = None    # İsteğe bağlı alan
    price: float                      # Zorunlu alan
    tax: float | None = None          # İsteğe bağlı alan


app = FastAPI()


# 2) POST İsteği ile Request Body Alma
"""
item: Item → FastAPI'ye "Bu parametre bir request body'dir"
demek anlamına gelir.

Artık POST /items/ çağrıldığında JSON body okunur,
Item modeline dönüştürülür, doğrulama yapılır.
"""

@app.post("/items/")
async def create_item(item: Item):
    # item artık bir Pydantic modelidir, dict değildir.
    return {
        "message": "Item başarıyla oluşturuldu!",
        "data": item
    }


# 3) Model Verisini Kullanmak (Hesaplama, Kontrol, etc.)

"""
item.dict() → Pydantic modelini dict'e dönüştürür.
"""

@app.post("/items/with-tax/")
async def create_item_with_tax(item: Item):
    item_dict = item.dict()

    # Eğer tax verilmişse fiyat + vergi hesabı yap
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict["price_with_tax"] = price_with_tax

    return item_dict


# 4) Request Body + Path Parametresi Birlikte

"""
item_id → PATH parametresi
item → BODY parametresi

FastAPI bunları otomatik olarak ayırır.
"""


"""
Pydantic modeli bir Python nesnesidir → JSON’a dönüşmesi için önce dict olmalı.
item.dict() -> API JSON olarak cevap dönebilir
"""

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id, 
        "updated_item": item.dict()
    }


# 5) Request Body + Path + Query Parametreleri Birlikte

"""
q → QUERY parametresi (isteğe bağlı)
item_id → PATH parametresi
item → BODY parametresi
"""

@app.put("/items/{item_id}/details")
async def update_item_details(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    
    if q:
        result["query_message"] = q

    return result
