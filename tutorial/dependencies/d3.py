# SUB-DEPENDENCIES (ALT BAĞIMLILIKLAR)
# Bu örnek, bir dependency'nin başka bir dependency'e bağlı
# olmasını gösterir.

from typing import Annotated
from fastapi import FastAPI, Depends, Cookie

app = FastAPI()

# 1. BAĞIMLILIK — query_extractor
# Görev:
#   - URL'de ?q=... şeklinde gönderilen query parametresini alır

def query_extractor(q: str | None = None):
    return q


# 2. ALT BAĞIMLILIK — query_or_cookie_extractor
# Bu fonksiyon hem bir "dependable" hem bir "dependant"tır.
# Yani hem bağımlılıktır hem de başka bağımlılıklara ihtiyaç duyar.
# Parametreler:
#   - q → query_extractor dependency'sinden gelir
#   - last_query → Cookie'den okunur
# Eğer URL'de q yoksa, cookie içindeki son sorguyu döndürür.

def query_or_cookie_extractor(
    q: Annotated[str | None, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    # q parametresi yoksa cookie'yi döndür
    if not q:
        return last_query
    return q


# 3. ENDPOINT — read_query
# Bu endpoint sadece *tek* dependency belirtir:
#   query_or_cookie_extractor
# Ama FastAPI otomatik olarak şunu yapar:
#   - önce query_extractor çalışır
#   - sonra query_or_cookie_extractor çalışır
#   - sonuç fonksiyona aktarılır

@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str | None, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}


# NOT:
# Eğer bir dependency birden fazla defa kullanılsaydı,
# FastAPI onu sadece 1 kez çalıştırır (cache).
# Eğer zorla her seferinde çalışmasını istersen:
# Depends(query_extractor, use_cache=False)
