#FASTAPI — QUERY PARAMETERS & VALIDATIONS

from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()


# 1) Basit bir sorgu parametresi

"""
q: str | None = None → q isteğe bağlı bir parametre
Bu URL'yi çağırırsan:
    /items/?q=hello
'q' değeri fonksiyona aktarılır.
"""

@app.get("/items/basic")
async def read_basic_items(q: str | None = None):
    return {"received_q": q}



# 2) Query doğrulaması — maksimum uzunluk

"""
Annotated ve Query kullanarak q parametresine ek doğrulama ekleyebiliriz.
Bu örnekte:
    - q isteğe bağlıdır
    - q verildiyse en fazla 50 karakter olabilir

Annotated, Python’da bir değişkene hem tip hem de ekstra 
bilgi (açıklama, validasyon, metadata vb.) eklemek için kullanılan bir yapıdır.
"""

@app.get("/items/validated")
async def read_validated_items(
    q: Annotated[str | None, Query(max_length=50)] = None
):
    return {"q": q}



# 3) Minimum ve maksimum uzunluk kontrolü

@app.get("/items/length")
async def read_items_length(
    q: Annotated[str | None, Query(min_length=3, max_length=20)] = None
):
    return {"q": q}



# 4) Regex (normal ifade) doğrulaması

"""
pattern="^fixedquery$" → q sadece "fixedquery" olabilir.
"""

@app.get("/items/regex")
async def read_items_regex(
    q: Annotated[str | None, Query(pattern="^fixedquery$")] = None
):
    return {"q": q}



# 5) Alias kullanımı

"""
URL'deki değişken adı Python değişken adı olamazsa alias kullanırız.
URL:
    /items/?item-query=value
"""

@app.get("/items/alias")
async def read_items_alias(
    q: Annotated[str | None, Query(alias="item-query")] = None
):
    return {"received_alias_q": q}



# 6) Deprecated (kullanımdan kalkmış) parametre

"""
Dokümantasyonda bu parametre "deprecated" olarak görünür.
deprecated=True olursa artık bu parametre artık kullanılmamalı. İleride kaldırılabilir.
"""

@app.get("/items/deprecated")
async def read_items_deprecated(
    q: Annotated[str | None, Query(deprecated=True)] = None
):
    return {"q": q}



# 7) OpenAPI dokümanında görünmeyen (gizli) parametre
"""
Swagger UI’da görünmez
APIDocs sayfasında listelenmez
Kullanıcı bu parametrenin varlığını dokümandan göremez

Ama:
Parametre API tarafından kabul edilir
Gönderilirse çalışır
"""

@app.get("/items/hidden")
async def read_items_hidden(
    hidden: Annotated[str | None, Query(include_in_schema=False)] = None
):
    return {"hidden": hidden}



# 8) Liste sorgu parametresi (multiple query params)

"""
URL:
    /items/list?q=foo&q=bar
Sonuç:
    {"q": ["foo", "bar"]}

URL de tek bir q gönderilirse JSON tarafında yine liste içeerisinde gelicektir.
"""

@app.get("/items/list")
async def read_items_list(
    q: Annotated[list[str] | None, Query()] = None
):
    return {"q": q}



# 9) Varsayılan liste değeri
"""Tabi kullanıcı kendi değerini gönderrise varsayılan değer ezilicektir."""

@app.get("/items/list-default")
async def read_items_list_default(
    q: Annotated[list[str], Query()] = ["foo", "bar"]
):
    return {"q": q}



# 10) Custom validation - özel doğrulayıcı

"""
Bu doğrulayıcı sadece "isbn-" veya "imdb-" ile başlamasına izin verir.
"""

def validate_id(value: str):
    if not value.startswith(("isbn-", "imdb-")):
        raise ValueError("Geçersiz ID → 'isbn-' veya 'imdb-' ile başlamalı")
    return value


@app.get("/items/custom")
async def read_items_custom(
    item_id: Annotated[str | None, AfterValidator(validate_id)] = None
):
    return {"validated_id": item_id}

