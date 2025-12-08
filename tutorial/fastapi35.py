#main.py
"""
Bu dosya test yazmayı öğrenmen için tasarlanmış küçük bir FastAPI uygulamasıdır.

Özellikler:
- /items/{item_id} → GET
- /items/ → POST
- X-Token header doğrulaması
- Bazı hatalı durumları test etmek için bilerek fake hata döndürür
"""

from typing import Annotated
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

# Testlerde kullanılacak fake değerler
fake_secret_token = "coneofsilence"

# Basit bir fake database (dict)
fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"}
}

app = FastAPI()

# Pydantic model
class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@app.get("/items/{item_id}", response_model=Item)
async def read_item(
    item_id: str,
    x_token: Annotated[str, Header()]
):
    """
    item_id fake_db içinde yoksa 404 döner.
    Header X-Token yanlışsa 400 döner.
    """
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")

    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(
    item: Item,
    x_token: Annotated[str, Header()]
):
    """
    Yeni item oluşturur.
    - Aynı id zaten varsa 409 döner.
    - Header hatalıysa 400 döner.
    """
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    if item.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")

    fake_db[item.id] = item
    return item


###################################################################################################################
#test_main.py

"""
Bu dosya uygulamanın tüm endpoint'lerini test eder.

TestClient → gerçek bir API'ye istek atıyormuşsun gibi davranır
Ama aslında FastAPI uygulaması test modunda çalışır, sunucu açılmaz!
"""

from fastapi.testclient import TestClient
from .main import app

# TestClient örneği
client = TestClient(app)


def test_read_item_success():
    """Doğru token + var olan item → başarılı"""
    response = client.get(
        "/items/foo",
        headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero"
    }


def test_read_item_bad_token():
    """Hatalı token → 400"""
    response = client.get(
        "/items/foo",
        headers={"X-Token": "wrongtoken"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_item_not_found():
    """Var olmayan item → 404"""
    response = client.get(
        "/items/ghost",
        headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item_success():
    """Yeni item başarıyla oluşturulmalı"""
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "newitem",
            "title": "New Item",
            "description": "Created via test"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "newitem",
        "title": "New Item",
        "description": "Created via test"
    }


def test_create_item_bad_token():
    """Hatalı token → 400"""
    response = client.post(
        "/items/",
        headers={"X-Token": "invalid"},
        json={
            "id": "badtoken",
            "title": "Bad Token",
            "description": "Should fail"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_item_existing():
    """Zaten var olan item → 409"""
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",  # zaten var!
            "title": "Duplicate",
            "description": "Should not overwrite"
        }
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
