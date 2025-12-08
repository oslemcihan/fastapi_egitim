#FASTAPI COOKIE PARAMETER MODELLERI


from typing import Annotated
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()

#COOKIE MODELİ OLUŞTURMA

class Cookies(BaseModel):
    """
    Bu model API'nin kabul ettiği çerezleri tanımlar.
    Her alan bir cookie'ye karşılık gelir.

    session_id         → zorunlu cookie
    fatebook_tracker   → opsiyonel cookie
    googall_tracker    → opsiyonel cookie
    """
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


#COOKIE MODELİNİ ENDPOINT'TE KULLANMA

@app.get("/items/")
async def read_items(
    # Tüm cookie’ler tek parametre ile alınır.
    cookies: Annotated[Cookies, Cookie()]
):
    """
    COOKIE ÖRNEKLERİ:
    session_id=abc123
    fatebook_tracker=track-001
    googall_tracker=experiment-12

    FastAPI bu cookie değerlerini Cookies modeline aktarır.
    Fonksiyon içinde cookies.session_id şeklinde erişebilirsin.
    """
    return cookies


#EKSTRA COOKIE'LERİ YASAKLAMA (Güvenlik)

class StrictCookies(BaseModel):
    """
    extra="forbid" → Bu modelde tanımlı olmayan cookie alınamaz.
    """
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None


@app.get("/strict-items/")
async def strict_read_items(
    cookies: Annotated[StrictCookies, Cookie()]
):
    """
    Eğer kullanıcı şu cookie'yi gönderirse:

    santa_tracker = "good-list-please"

    FastAPI şu hatayı döner:
    {
        "detail": [
            {
                "type": "extra_forbidden",
                "loc": ["cookie", "santa_tracker"],
                "msg": "Extra inputs are not permitted"
            }
        ]
    }
    """
    return cookies


#ÖZET
"""
✔ Cookie() → Cookie okur
✔ Pydantic model → Cookie grubunu tek yerde tanımlar
✔ model_config={"extra": "forbid"} → fazladan cookie’leri engeller
✔ FastAPI cookie'leri otomatik olarak modele eşler
"""

