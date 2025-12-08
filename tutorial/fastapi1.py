
"""
Bu dosya FastAPI’nin temel çalışma mantığını öğretmek içindir.

İçerik:

1) FastAPI import edilir
2) Bir FastAPI app örneği oluşturulur
3) Bir yol (path) ve operasyon (GET) tanımlanır
4) Fonksiyon istek gelince nasıl çalışır gösterilir
5) Açıklamalar: Swagger UI, ReDoc, openapi.json


Bunları bil;
Python'da @something sözdizimi "dekoratör" olarak adlandırılır.

yol: /
operasyon: get
fonksiyon: "dekoratör"ün (@app.get("/")'in) altındaki fonksiyondur.

HTTP Metodları (Operations):
POST
GET
PUT
DELETE
...veya daha az kullanılan diğerleri:

OPTIONS
HEAD
PATCH
TRACE

"""

# 1) FastAPI modülünü içe aktar
from fastapi import FastAPI


# 2) FastAPI "app" örneği oluşturma

"""
FastAPI(), API’nizin çekirdeği olan bir sınıftır.
Bu sınıftan “app” adında bir örnek oluşturuyoruz.
Uvicorn bu değişkeni kullanarak sunucuyu çalıştırır.

Komut:
    uvicorn main:app --reload

main → modül adı (main.py)
app  → bu dosyadaki app değişkeni
"""
app = FastAPI()


# 3) Bir Yol (Path) ve Yol Operasyonu (Operation) Tanımlama

"""
@app.get("/") → bir "yol operasyonu dekoratörüdür".
FastAPI'ye şunu söyler:

- Bu fonksiyon, HTTP GET metodunda
- "/" yoluna gelen istekleri karşılasın

Yani tarayıcıda:
    http://127.0.0.1:8000/

Bu fonksiyon çalışır.
"""

@app.get("/")  # GET işlemine sahip "/" yolu
async def root():
    """
    Bu fonksiyon bir HTTP isteği geldiğinde çalışır.
    Geriye bir Python dict döner → FastAPI bunu JSON'a çevirir.
    
    Dönen JSON:
        {"message": "Hello World"}

    Not:
    Fonksiyon async def olarak tanımlandı.
    Böylece FastAPI, eşzamanlı (concurrent) şekilde yüksek performans sağlar.
    """
    return {"message": "Hello World"}


# 4) Ek Yol Örneği 

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Bu örnek:
    - Dinamik bir yol parametresi alır (/items/10 gibi)
    - Tip belirtecini (int) kullanır
    - JSON döner

    Örnek istek:
        http://127.0.0.1:8000/items/5

    Dönen JSON:
        {"item_id": 5}
    """
    return {"item_id": item_id}


# 5) Swagger, ReDoc ve OpenAPI Açıklamaları

"""
FASTAPI OTO-DOKÜMANTASYON ÖZELLİKLERİ:

1) Swagger UI → etkileşimli API test arayüzü
   Aç: http://127.0.0.1:8000/docs

2) ReDoc → Alternatif bir dokümantasyon arayüzü
   Aç: http://127.0.0.1:8000/redoc

3) OpenAPI JSON Şeması → API'nin tüm tanımı
   Aç: http://127.0.0.1:8000/openapi.json

OpenAPI nedir?
- API'nizin tüm yollarını, parametrelerini ve veri yapılarını anlatan bir şemadır.
- FastAPI bu şemayı otomatik yaratır.
- Dokümantasyon araçları bu OpenAPI şemasını kullanır.
"""

# 6) SUNUCUYU ÇALIŞTIRMA BİLGİ NOTU

"""
Bu dosyayı (main.py) çalıştırmak için terminalde:

    uvicorn main:app --reload

--reload → kodu değiştirdikçe sunucu otomatik yeniden başlar
           Sadece geliştirme ortamında kullanılır.

Sunucu açıldığında terminalde şunu görürsün:

INFO: Uvicorn running on http://127.0.0.1:8000

Tarayıcıda:
    http://127.0.0.1:8000/          → JSON cevabı
    http://127.0.0.1:8000/docs      → Swagger UI
    http://127.0.0.1:8000/redoc     → ReDoc dokümantasyonu
"""
