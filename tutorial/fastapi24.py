#FASTAPI – ERROR HANDLING
# Bu dosya FastAPI'de hata yönetiminin nasıl yapıldığını
# örnekleriyle ve detaylı yorumlarla açıklar.


from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# Basit veri kaynağı
items = {"foo": "The Foo Wrestlers"}


# 1) Basit HTTPException kullanımı

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """
    Eğer item mevcut değilse 404 hatası gönder.
    HTTPException return edilmez -> raise edilir.
    """
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"item": items[item_id]}


# 2) Özel header eklenmiş HTTPException

@app.get("/items-header/{item_id}")
async def read_item_with_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


# 3) Özel exception sınıfı ve handler

class UnicornException(Exception):
    """Kendi özel hata sınıfımız."""
    def __init__(self, name: str):
        self.name = name


# Bu handler UnicornException yakalanınca çalışır
@app.exception_handler(UnicornException)
async def unicorn_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,  # I'm a teapot :)
        content={"message": f"Oops! {exc.name} did something."}
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name)
    return {"unicorn_name": name}


# 4) Validation (geçersiz veri) hatalarını özelleştirme

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    """
    Geçersiz veri geldiğinde JSON yerine düz metin döndür.
    """
    return PlainTextResponse(str(exc), status_code=400)


# 5) FastAPI + Starlette HTTPExceptions override

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    JSON yerine düz metin dön. Varsayılan davranışı ez.
    """
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# 6) Endpoint test

@app.get("/numbers/{num}")
async def number_test(num: int):
    """
    Validasyon hatası görmek için /numbers/test gibi bir şey dene.
    """
    if num == 3:
        raise HTTPException(status_code=418, detail="I don't like number 3.")
    return {"number": num}

# ÖZET
#
# ✔ HTTPException → API hatası fırlatma
# ✔ Özel exception sınıfları yazıp yakalama
# ✔ ValidationError davranışını değiştirme
# ✔ Hatalara özel header ekleme
# ✔ Varsayılan FastAPI handler'larını override etme

