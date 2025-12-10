# DEPENDENCIES WITH YIELD — FastAPI örnek uygulama
# Bu dosya yield kullanılan dependency’lerin nasıl çalıştığını
# adım adım açıklayan bir örnek içerir.

from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI()


# 1) BASİT BİR VERİTABANI OTURUM SINIFI (SAHTE)
class FakeDB:
    def __init__(self):
        print("DB bağlantısı oluşturuldu.")

    def query(self):
        return "Veritabanından örnek veri"

    def close(self):
        print("DB bağlantısı kapatıldı.")


# 2) YIELD KULLANILARAK OLUŞTURULAN DEPENDENCY
# - yield öncesi → bağlantı oluşturulur
# - yield → endpoint'e db instance döner
# - yield sonrası (finally) → bağlantı kapatılır

async def get_db():
    db = FakeDB()  # → Bağlantı oluştur
    try:
        # Path operation bu nesneyi kullanacak
        yield db
    finally:
        # Response döndükten sonra cleanup işlemi yapılır
        db.close()


# 3) DEPENDENCY KULLANAN ENDPOINT
# Burada db nesnesi dependency tarafından sağlanır.

@app.get("/items/")
async def read_items(db: Annotated[FakeDB, Depends(get_db)]):
    result = db.query()
    return {"message": "Başarılı", "data": result}


# 4) EXCEPTION İLE ÖRNEK

class DangerousItemError(Exception):
    pass


@app.get("/danger/{name}")
async def get_dangerous_item(
    name: str,
    db: Annotated[FakeDB, Depends(get_db)]
):
    if name == "bomb":
        # Bu exception dependency'nin except bloğuna gider
        raise DangerousItemError("Tehlikeli bir eşya!")
    return {"item": name, "db_data": db.query()}


# 5) EXCEPTION’I YAKALAYIP HTTP HATASINA ÇEVİREN DEPENDENCY

async def get_username():
    try:
        yield "Rick"
    except DangerousItemError as e:
        # Hata burada yakalanır ve HTTPException'a çevrilir
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/secure/{item}")
async def secure_item(
    item: str,
    username: Annotated[str, Depends(get_username)] #usernmae rewuest tarafından göndeerilmez bu değer get_usernmae dependency den gelir
):
    if item != "portal-gun":
        raise DangerousItemError("Sadece portal-gun kullanılabilir")
    return {"owner": username, "item": item}

"""
Bu nasıl çalışıyor?

1 db = FakeDB() → Bağlantı açılır
2 yield db → endpoint fonksiyonuna db gönderilir
3 endpoint yanıtı döner
4 finally → db.close() → Bağlantı kapanır

Bu otomatik yapılır.
Sen kapatmayı unutamazsın → güvenli.
"""