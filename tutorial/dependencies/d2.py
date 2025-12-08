# CLASSES AS DEPENDENCIES
# Sınıfları bağımlılık olarak kullanmanın tam örneği

from typing import Annotated
from fastapi import FastAPI, Depends

app = FastAPI()

# ÖRNEK VERİ TABANI

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]

# SINIF OLARAK BAĞIMLILIK
# Bu sınıf bir fonksiyon gibi çağrılır.
# FastAPI q, skip, limit parametrelerini çıkarır
# ve sınıftan bir instance oluşturur.

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q        # Sorgu filtresi
        self.skip = skip  # Kaç öğe atlanacak?
        self.limit = limit  # Max kaç öğe döndürülecek?

# ENDPOINT (PATH OPERATION)
# commons değişkenine CommonQueryParams sınıfının
# bir örneği otomatik olarak gelir.

@app.get("/items/")
async def read_items(
    commons: Annotated[CommonQueryParams, Depends()]
):
    response = {}

    # Eğer q gönderilmişse filtre bilgisini ekleyelim
    if commons.q:
        response["q"] = commons.q

    # Skip ve limit kullanarak ürünleri parçalayalım
    items = fake_items_db[commons.skip : commons.skip + commons.limit]

    response["items"] = items
    return response

# ÖZET:
# - Sınıf kullanmak daha okunabilir ve güçlüdür.
# - FastAPI sınıfın __init__ parametrelerini otomatik çözer.
# - Daha iyi autocomplete, daha iyi tip kontrolü sağlar.

