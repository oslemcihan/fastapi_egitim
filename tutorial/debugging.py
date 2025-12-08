"""
Bu dosya, FastAPI uygulamasını debugging (hata ayıklama) modunda
çalıştırmanın en doğru şeklini gösterir.

Amaç:
- Uvicorn'u direkt bu dosya içinden çalıştırmak.
- Böylece VSCode veya PyCharm debuggerı ile satır satır kod incelemek.
"""

import uvicorn
from fastapi import FastAPI

# -------------------------------------------------------
# FastAPI uygulaması
# -------------------------------------------------------
app = FastAPI()


@app.get("/")
def root():
    # Debugging için örnek değişkenler
    a = "a"
    b = "b" + a  # Buraya breakpoint koyabilirsin
    return {"hello world": b}


# -------------------------------------------------------
# Bu blok neden önemlidir?
# -------------------------------------------------------
# Bu blok sadece:
#   python main.py
# şeklinde çalıştırıldığında aktif olur.
#
# Eğer başka bir dosya:
#   from main import app
# diyerek bu dosyayı import ederse,
# bu blok çalışmaz. Yani uvicorn sunucusu otomatik başlamaz.
#
# Debugging için gereklidir çünkü debug sırasında dosya
# direkt çalıştırılır ve bu blok sayesinde sunucu açılır.
# -------------------------------------------------------
if __name__ == "__main__": #bu satır Python dosyasının doğrudan çalıştırılıp çalıştırılmadığını kontrol eder.
    # FastAPI uygulamasını uvicorn ile başlat
    # Debugger bu satırdan sonra sunucuyu çalıştırır.
    uvicorn.run(
        "main:app",    # uygulama yolu, FastAPI uygulamasının nerde olduğunu söyler
        host="0.0.0.0", #Sunucunun hangi IP’den dinleme yapacağını belirtir. "0.0.0.0" → Tüm cihazlardan erişime izin verir.
        port=8000, #Sunucu 8000 numaralı port üzerinden çalışacaktır.
        reload=False   # Debugger kendi reload işlemini yapar
    )
