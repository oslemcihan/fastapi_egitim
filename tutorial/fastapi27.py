# FastAPI - PUT ve PATCH ile Güncelleme İşlemleri
# Açıklamalı Örnek Kod

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

# Model Tanımı
# Tüm alanları opsiyonel yaptık, çünkü PATCH sırasında
# bazı alanlar gönderilmeyebilir.


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


# Fake veritabanı

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
}

# PUT → Kaydı tamamen değiştirir!

@app.put("/items/{item_id}", response_model=Item)
async def update_item_put(item_id: str, item: Item):
    # Gelen modeli JSON uyumlu veriye çeviriyoruz
    encoded = jsonable_encoder(item)

    # Tüm eski kayıt silinir, yerine yeni kayıt yazılır
    items[item_id] = encoded

    return encoded


# PATCH → Kısmi güncelleme yapar

@app.patch("/items/{item_id}", response_model=Item)
async def update_item_patch(item_id: str, item: Item):

    # Önce eski kaydı alın
    stored_item_data = items[item_id]

    # Pydantic modele dönüştür
    stored_item_model = Item(**stored_item_data)

    # Gönderilmeyen alanları dışarıda bırak (exclude_unset)
    update_data = item.dict(exclude_unset=True)

    # Eski model üzerinde sadece gönderilen alanları güncelle
    updated_item = stored_item_model.copy(update=update_data)

    # JSON uyumlu hale getirip kaydet
    items[item_id] = jsonable_encoder(updated_item)

    return updated_item


# Özet:
# PUT → “kaydı tamamen sıfırla ve yenisiyle değiştir”
# PATCH → “sadece gönderilen alanları güncelle”
