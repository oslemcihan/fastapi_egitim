#FASTAPI – FORMS + FILES
# Bu dosya aynı anda hem FORM alanlarının (text verileri)
# hem de FILE alanlarının (dosya yükleme) nasıl alınacağını
# örneklerle açıklar.
#
# Dosya/form yükleme için gerekli paket:
#     pip install python-multipart

from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


# 1) FORM + FILE aynı request içinde alma

@app.post("/upload/")
async def upload(
    # Dosyayı RAM'e tamamen yükle (küçük dosyalar için)
    file: Annotated[bytes, File()],
    
    # Dosyayı UploadFile olarak al (büyük dosyalar için ideal)
    fileb: Annotated[UploadFile, File()],
    
    # Formdan gelen text alanı
    token: Annotated[str, Form()],
):
    """
    Bu endpoint hem dosya hem form alanı alır.
    - file  → bytes (dosya içeriği RAM'e yüklenir)
    - fileb → UploadFile (büyük dosyalar için uygun)
    - token → form alanı (örneğin kullanıcı token)
    """

    # fileb içeriğini okumak istersek:
    fileb_content = await fileb.read()

    return {
        "file_size": len(file),
        "fileb_size": len(fileb_content),
        "fileb_type": fileb.content_type, #UploadFile, tarayıcıdan gelen Content-Type header’ını tutar. Böylece dosyanın türünü alırız:
        "token": token,
    }


# 2) HTML FORM 

@app.get("/")
async def form_page():
    """
    Tarayıcı üzerinden test etmek için HTML formu döndürür.
    """
    html = """
    <body>
        <h2>Form + Dosya Yükleme</h2>
        <form action="/upload/" enctype="multipart/form-data" method="post">
            <p>File (bytes): <input type="file" name="file"></p>
            <p>Fileb (UploadFile): <input type="file" name="fileb"></p>
            <p>Token (Form alanı): <input type="text" name="token"></p>
            <input type="submit">
        </form>
    </body>
    """
    return HTMLResponse(html)

# ÖZET
#
# File()  → dosya alanı
# Form()  → metin alanı
# UploadFile → büyük dosyalar için en ideal yöntem
#
#  Form + File + Body(JSON) aynı anda kullanılamaz
#    (HTTP multipart/form-data kısıtı)
