#FASTAPI COOKIE (ÇEREZ) ÖRNEĞİ

from typing import Annotated
from fastapi import FastAPI, Cookie

"""
Bu dosya FastAPI'de cookie (çerez) parametresi nasıl okunur
ve nasıl kullanılır gösteren eğitim örneğidir.

FastAPI çerezleri otomatik olarak:
- okur
- doğrular
- tipine dönüştürür
- Swagger UI'da gösterir
"""

app = FastAPI()

#COOKIE PARAMETRESİ OKUMA

@app.get("/items/")
async def read_items(
    # Cookie değerini okumak için Cookie() kullanıyoruz.
    # Eğer Cookie() kullanmasaydık FastAPI bunu Varsayılan QUERY parametresi sanacaktı.
    ads_id: Annotated[str | None, Cookie()] = None
):
    """
    Bu fonksiyon gelen isteğin Cookie başlığındaki
    'ads_id' değerini okur.

    ÖRNEK HTTP İSTEĞİ:
    GET /items/
    Cookie: ads_id=ABC123

    Fonksiyon ads_id="ABC123" şeklinde alır.
    """
    return {"ads_id": ads_id}
