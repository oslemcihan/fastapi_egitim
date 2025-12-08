"""
Bu dosya FastAPI'de statik dosyaların nasıl sunulduğunu gösterir.

Amaç:
- /static yolu altındaki tüm istekler StaticFiles tarafından karşılanır.
- Yani /static/logo.png → static/logo.png dosyasını döner.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# FastAPI uygulamasını oluşturuyoruz
app = FastAPI()

# ----------------------------------------------------------
# STATIC FILES MOUNT (BAĞLAMA)
# ----------------------------------------------------------
# StaticFiles, belirttiğimiz klasördeki dosyaları olduğu gibi sunan
# bağımsız bir mini uygulamadır.
#
# 1. "/static" → URL yolu
# 2. directory="static" → sunulacak klasör adı
# 3. name="static" → uygulama içinde referans ismi
#
# Örnek:
# /static/logo.png → static/logo.png dosyasını verir
# /static/style.css → static/style.css dosyasını verir
# ----------------------------------------------------------
app.mount(
    "/static",                  # kullanıcı buradan erişecek
    StaticFiles(directory="static"),  # dosyaların bulunduğu klasör
    name="static"
)


# ----------------------------------------------------------
# NORMAL FASTAPI ENDPOINT
# Bu endpoint sadece örnektir.
# ----------------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "Statik dosya örneği çalışıyor!",
        "static_file_example": "http://localhost:8000/static/logo.png"
    }

