# FastAPI'de middleware kullanımını gösteren tam açıklamalı örnek
#Middleware bir istek geldiğinde: Endpoint çalışmadan ÖNCE devreye girer, Endpoint çalıştıktan SONRA tekrar devreye girer
import time
from fastapi import FastAPI, Request

app = FastAPI()

# 1) Middleware oluşturma
# Her HTTP isteğinde otomatik olarak çalışır
@app.middleware("http")
async def add_process_time_header(request: Request, call_next): #call_next → İsteği asıl endpoint’e ileten fonksiyon
    """
    Bu middleware:
    - İstek geldiğinde zamanı kaydeder
    - İsteği route'a gönderir
    - Route cevabı oluşturur
    - Middleware o cevabı yakalar
    - Cevaba 'X-Process-Time' header'ı ekler
    - Cevabı geri döndürür
    """

    # İsteğin başlangıç zamanını al
    start_time = time.perf_counter()

    # İstek route'a iletiliyor
    response = await call_next(request)

    # Toplam geçen süre
    process_time = time.perf_counter() - start_time

    # Response header'a süre bilgisini ekle
    response.headers["X-Process-Time"] = str(process_time)

    # Cevabı geri döndür
    return response


# 2) Normal bir endpoint
# Middleware bu endpoint çalışmadan ÖNCE ve SONRA devreye girer

@app.get("/hello")
async def hello():
    return {"message": "Merhaba! Middleware çalıştı mı? Headerlara bak!"}

