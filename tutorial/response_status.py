#FASTAPI – RESPONSE STATUS CODE
#  Bir endpoint'in döndüreceği HTTP durum kodunu ayarlama

from fastapi import FastAPI, status

app = FastAPI()


#1) Basit status_code kullanımı

@app.post("/items/", status_code=201)
async def create_item(name: str):
    """
    Bu endpoint yeni bir kaynak oluşturuyor gibi davranır.
    HTTP 201 Created döner.
    """
    return {"name": name}


#2) status.HTTP_201_CREATED kullanımı (önerilen yol)

@app.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product(name: str):
    """
    status modülü sayesinde kodu hatırlamak zorunda kalmayız.
    Autocomplete ile öneriler gelir.
    """
    return {"product": name}


#3) 204 NO CONTENT – body dönmeyen status

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    204 kodu 'No Content' demektir. 
    Bu durumda FastAPI otomatik olarak body göndermeyi engeller.
    """
    # normalde databaseden silme burada olur
    return None  # body gönderilmez!
#204 işlem başarılı ama sana body döndürmüyorum

#4) 404 – Manuel hata döndürme

from fastapi import HTTPException

database = {"foo": "Foo Item"}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    """
    Eğer item bulunamazsa 404 döndür.
    """
    if item_id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found!"
        )
    return {"item": database[item_id]}


#ÖZET
"""
✔ status_code dekoratöre yazılır, fonksiyona değil.
✔ Sayı veya status.HTTP_XXX şeklinde verilebilir.
✔ 204 gibi bazı kodlar body göndermez.
✔ HTTPException ile manuel hata kodu döndürebilirsin.
"""

