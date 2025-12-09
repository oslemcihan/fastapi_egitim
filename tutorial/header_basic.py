#FASTAPI HEADER (BAŞLIK) ÖRNEĞİ

from typing import Annotated
from fastapi import FastAPI, Header

"""
Bu dosya FastAPI'de HTTP header'larını nasıl okuyacağınızı
öğreten örnek bir projedir.

FastAPI header'ları otomatik olarak:
- okur
- doğrular
- tipine dönüştürür
- Swagger UI'da gösterir
"""

app = FastAPI()

#BASİT HEADER OKUMA (User-Agent örneği)

@app.get("/items/")
async def read_items(
    # Header() yazmazsak bu parametre Query parametresi sanılır!
    # Annotated kullanarak hem tipi hem de Header() bilgisini ekliyoruz.
    user_agent: Annotated[str | None, Header()] = None
):
    """
    Bu fonksiyon HTTP isteğindeki 'User-Agent' header'ını okur.

    ÖRNEK HTTP İSTEĞİ:
    GET /items/
    User-Agent: Mozilla/5.0

    Fonksiyon user_agent = "Mozilla/5.0" şeklinde alır.
    """
    return {"User-Agent": user_agent}


#UNDERSCORE → DASH OTOMATİK DÖNÜŞÜM KAPATMA

@app.get("/raw-header/")
async def read_raw_header(
    # Bu durumda FastAPI header isminde underscore aramaz.
    # Yani header tam olarak "strange_header" olarak beklenir.
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None
):
    """
    Normalde FastAPI 'strange_header' ismini 'strange-header' header'ı ile eşleştirirdi.
    Ancak convert_underscores=False dendiği için artık dönüşüm yok.
    """
    return {"strange_header": strange_header}


#BİRDEN FAZLA HEADER DEĞERİ ALMA (Duplicate Header)

@app.get("/multi-header/")
async def read_multi_header(
    # Bir header birden fazla kez gönderilecekse tipini liste yapmalıyız.
    x_token: Annotated[list[str] | None, Header()] = None
):
    """
    Eğer istek şöyle gelirse:

    X-Token: foo
    X-Token: bar

    FastAPI şunu döner:
    x_token = ["foo", "bar"]
    """
    return {"X-Token values": x_token}