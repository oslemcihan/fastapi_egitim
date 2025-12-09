#FASTAPI - NESTED MODELS
#Bir modelin içinde başka bir model, liste, set veya dict kullanabiliyorsan → nested model kullanmışsındır.

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

# 1) BASİT ALT MODEL (Submodel)

class Image(BaseModel):
    """
    Bu model başka modeller içinde kullanılacak alt modeldir.
    İki alanı vardır:
    - url (HttpUrl → geçerli bir URL olmalı)
    - name (str)
    """
    url: HttpUrl
    name: str


# 2) NESTED MODEL KULLANIMI

class Item(BaseModel):
    """
    Item modeli birçok farklı türde alan içerir:
    - name → zorunlu string
    - description → opsiyonel
    - price → float
    - tags → set[str] (duplikeleri engeller)
    - images → list[Image] (birden fazla alt model)
    """
    name: str
    description: str | None = None
    price: float
    tags: set[str] = set()    # tekrar eden değerler otomatik silinir
    images: list[Image] | None = None   # Alt model listesi


# 3) BİR MODELİ İÇEREN BAŞKA BİR MODEL (Daha derin nested)

class Offer(BaseModel):
    """
    Offer modeli, içinde Item listesi barındırır.
    Bu, çok seviyeli nested model örneğidir.
    """
    name: str
    description: str | None = None
    price: float
    items: list[Item]     # Nested: Offer → Item → Image


# 4) BODY OLARAK NESTED MODEL ALAN ENDPOINT

@app.post("/offers/")
async def create_offer(offer: Offer):
    """
    Bu endpoint body'den Offer modeli alır.
    İçinde Item listesi,
    her Item içinde Image listesi olabilir.

    FastAPI/Pydantic otomatik:
    ✔ Doğrulama
    ✔ Veri dönüştürme
    ✔ JSON -> Python model
    ✔ Python model -> JSON
    ✔ OpenAPI dokümantasyonu
    sağlar.
    """
    return offer


# 5) BODY DOĞRUDAN LİSTE OLABİLİR

@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    """
    Bu endpoint doğrudan bir liste bekler:

    [
        { "url": "...", "name": "..." },
        { "url": "...", "name": "..." }
    ]

    Liste elemanları Image modeliyle doğrulanır.
    """
    return images


# 6) KEY = int, VALUE = float şeklinde dict body

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    """
    JSON anahtarları sadece string kabul eder,
    ama Pydantic bu stringleri int'e dönüştürür.

    Örnek body:
    {
        "1": 0.5,
        "2": 0.9
    }

    Python tarafında:
    {1: 0.5, 2: 0.9}
    olarak gelir.
    """
    return weights