#FASTAPI — QUERY PARAMETER MODELLERİ (EĞİTİM DOSYASI)

from fastapi import FastAPI, Query
from typing import Annotated, Literal
from pydantic import BaseModel, Field

app = FastAPI()

# 1) QUERY PARAMETRELERİNİ MODELE ALMA

"""
FilterParams modeli, bir endpoint için gerekli olan tüm 
sorgu parametrelerini toplu olarak tanımlar.

Avantajları:
 - Tüm doğrulamalar tek yerde yapılır.
 - Endpoint fonksiyonu aşırı kalabalık olmaz.
 - Model birden fazla yerde tekrar kullanılabilir.
"""


class FilterParams(BaseModel):
    # limit > 0 ve limit <= 100 olmalı
    limit: int = Field(100, gt=0, le=100)

    # offset >= 0 olmalı
    offset: int = Field(0, ge=0)

    # order_by sadece bu iki değerden biri olabilir
    order_by: Literal["created_at", "updated_at"] = "created_at"

    # tag listesi (URL'de birden fazla tag geçebilir)
    tags: list[str] = []


# 2) ENDPOINT İÇİNDE MODELİ KULLANMA

"""
query parametreleri otomatik olarak modele doldurulur.
Kullanıcı şu şekilde istek atabilir:

    /items/?limit=20&offset=5&order_by=updated_at&tags=a&tags=b

FastAPI bu verileri otomatik olarak FilterParams modeline doldurur.
"""

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    # FastAPI otomatik olarak modeli doldurduğu için
    # burada ekstra işleme gerek yok.
    return {
        "received_params": filter_query
    }



# 3) FAZLA QUERY PARAMETRESİNİ YASAKLAMA

"""
Modelde tanımlı olmayan hiçbir query parametresinin gelmesini istemiyorsak
'model_config = {"extra": "forbid"}' ekleriz.

Böylece:
    /items/?limit=10&tool=plumbus
hatası alınır çünkü 'tool' modeli yok.
"""


class StrictFilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # fazlalık parametreleri yasakla

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/strict-items/")
async def read_items_strict(filter_query: Annotated[StrictFilterParams, Query()]):
    return {
        "received_params": filter_query
    }
