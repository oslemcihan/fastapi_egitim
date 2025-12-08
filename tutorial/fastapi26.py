#JSONABLE_ENCODER - DETAYLI AÇIKLAMALI ÖRNEK
# Bu dosya, FastAPI'nin jsonable_encoder() fonksiyonunun
# ne zaman ve neden kullanıldığını öğretmek için hazırlanmıştır.

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4


app = FastAPI()

# Pydantic modelimiz JSON tarafından direkt desteklenmeyen
# tipler içeriyor (datetime, UUID, set)


class Product(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    tags: set[str]


# Fake veritabanı sadece JSON uyumlu veri kabul ediyor.
# (örneğin NoSQL bir DB veya bir dış API)

fake_db = {}


# jsonable_encoder Kullanımı

@app.post("/products/")
async def create_product(product: Product):

    # Pydantic modeli JSON uyumlu hale dönüştür
    json_product = jsonable_encoder(product)

    # Artık DB'nin kabul ettiği biçimde:
    # - UUID → string
    # - datetime → ISO string
    # - set → list
    fake_db[str(product.id)] = json_product

    return {
        "saved_data": json_product,
        "notice": "Product JSON-compatible format saved successfully."
    }



# Neden jsonable_encoder gerekli?
# Çünkü normalde şu çalışmaz:
#    fake_db["x"] = product     (Pydantic model doğrudan JSON değil)
# Şu da çalışmaz:
#    fake_db["x"] = product.dict()   (datetime JSON'a uygun değil)
# Ama jsonable_encoder hepsini dönüştürür:
#    fake_db["x"] = jsonable_encoder(product)  
