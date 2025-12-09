#FASTAPI – PATH OPERATION CONFIGURATION
# Bu dosya, path operation'ların nasıl yapılandırıldığını açıklar
# TAG: Sadece ve sadece dokümantasyon görünümü için vardır.Sadece Swagger UI (docs) içinde klasör oluşturur.
from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

# MODELLER

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


# TAG ENUM – Büyük projelerde düzen sağlar

class Tags(Enum):
    items = "items"
    users = "users"


# 1) STATUS CODE – Endpoint HTTP kodu belirleme

@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,  # 201 = Created
    tags=[Tags.items],
    summary="Create an item",
    description="This endpoint creates an item with full details."
)
async def create_item(item: Item):
    """
    ### Create an Item  
    Markdown destekli açıklama:

    - **name**: zorunlu
    - **description**: opsiyonel
    - **price**: zorunlu
    - **tax**: opsiyonel
    - **tags**: benzersiz string kümesi
    """
    return item


# 2) BASİT TAG KULLANIMI

@app.get("/items/", tags=[Tags.items])
async def read_items():
    return [{"name": "Foo", "price": 42}]


# 3) USERS TAG

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username": "johndoe"}]


# 4) DEPRECATED ENDPOINT
# Artık kullanılmıyor, ama silinmedi.
# Dokümantasyonda "deprecated" olarak işaretlenir.

@app.get("/elements/", tags=[Tags.items], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]


# 5) RESPONSE DESCRIPTION

@app.get(
    "/info",
    response_description="General information response"
)
async def info():
    return {"message": "Hello World"}

# ÖZET
#
# ✔ status_code → HTTP yanıt kodu
# ✔ tags → dokümantasyonu kategorize eder
# ✔ summary → kısa açıklama
# ✔ description → uzun açıklama (Markdown destekli)
# ✔ response_description → yanıt açıklaması
# ✔ deprecated → endpoint kullanım dışı işareti
