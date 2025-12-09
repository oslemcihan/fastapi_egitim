#FASTAPI HEADER PARAMETRE MODELLERİ

from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

#HEADER MODELİ OLUŞTURMA

class CommonHeaders(BaseModel):
    """
    Bu model API'nin kabul ettiği header'ları tanımlar.

    host               → zorunlu header (HTTP Host bilgisi)
    save_data          → zorunlu header (True/False)
    if_modified_since  → opsiyonel header
    traceparent        → opsiyonel header (ör. dağıtık izleme için)
    x_tag              → birden çok header değeri alabilir
    """
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []   # Duplicate header desteği


#HEADER MODELİNİ ENDPOINT'TE KULLANMA

@app.get("/items/")
async def read_items(
    headers: Annotated[CommonHeaders, Header()]
):
    """
    ÖRNEK HEADER’LAR:
    Host: example.com
    Save-Data: on
    If-Modified-Since: Sat, 10 Feb 2024 12:00:00 GMT
    X-Tag: tag1
    X-Tag: tag2  ← List olur

    FastAPI bu header'ları otomatik olarak CommonHeaders
    modeline aktarır.
    """
    return headers


#EKSTRA HEADER’LARI ENGELLEME

class StrictHeaders(BaseModel):
    """
    extra="forbid" → Bu modelde olmayan header kabul edilmez.
    """
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool


@app.get("/strict-items/")
async def read_strict_items(
    headers: Annotated[StrictHeaders, Header()]
):
    """
    Eğer şu header gönderilirse:

    Tool: plumbus

    FastAPI şu hatayı döner:
    {
        "type": "extra_forbidden",
        "loc": ["header", "tool"],
        "msg": "Extra inputs are not permitted"
    }
    """
    return headers


#ALT ÇİZGİ → TİRE DÖNÜŞÜMÜNÜ KAPATMA

@app.get("/raw-headers/")
async def read_raw_headers(
    headers: Annotated[
        CommonHeaders,
        Header(convert_underscores=False)  # Dönüşüm kapalı
    ]
):
    """
    Normalde save_data → save-data şeklinde HTTP'de kullanılır.

    Bu endpoint'te underscore dönüşümü kapalıdır.
    Bu nedenle sadece save_data şeklinde header kabul edilir.

    UYARI:
    Birçok proxy alt çizgili header’ları engeller.
    """
    return headers



#ÖZET
"""
✔ Header() → Request header okur
✔ Pydantic model → Header grubunu tek parametreyle yönetir
✔ extra="forbid" → Fazladan header’ları reddeder
✔ convert_underscores=False → Alt çizgi dönüşümünü kapatır
"""

