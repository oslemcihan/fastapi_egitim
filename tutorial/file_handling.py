#FASTAPI – Request Files
#
# Bu dosya FastAPI ile dosya yüklemenin nasıl yapılacağını
# ve UploadFile kullanımının avantajlarını açıklar.
#
# Dosya yüklemek için gerekli paket:
#     pip install python-multipart

from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1) DOSYAYI BYTES OLARAK ALMA
# Bu yöntem dosyayı RAM'e tamamen yükler.
# Küçük dosyalar için uygundur, büyük dosyalar için tehlikelidir.

@app.post("/upload-bytes/")
async def upload_bytes(file: Annotated[bytes, File()]):
    """
    Dosyayı bytes olarak alır. Tüm dosya RAM'e yüklenir.
    """
    return {"file_size": len(file)}


# 2) DOSYAYI UploadFile OLARAK ALMA (Tavsiye edilir)
# UploadFile RAM yerine disk kullanabilir.
# Daha büyük dosyalar için çok daha verimlidir.
# Meta bilgilerine erişebilirsin

@app.post("/upload-file/")
async def upload_file(file: UploadFile):
    """
    UploadFile dosyayı geçici bir dosya olarak depolar.
    Meta bilgiler:
      file.filename
      file.content_type
    """
    contents = await file.read()     # Dosya içeriğini oku
    size = len(contents)

    # Dosyayı tekrar okumak için başa sar:
    await file.seek(0) #eğerki tekrar bu dosyayı okursam diye başa getiriyorum konumu

    return {
        "filename": file.filename,
        "size": size,
        "content_type": file.content_type
    }


# 3) OPSİYONEL DOSYA

@app.post("/optional-file/")
async def optional_file(file: UploadFile | None = None):
    """
    Dosya gönderilmezse None döner.
    """
    if not file:
        return {"message": "Dosya gönderilmedi"}
    return {"filename": file.filename}


# 4) BİRDEN FAZLA DOSYA YÜKLEME

@app.post("/upload-multiple/")
async def upload_multiple(files: list[UploadFile]):
    """
    Aynı form alanı üzerinden çoklu dosya yüklenebilir.
    """
    return {"filenames": [file.filename for file in files]}


# 5) DOSYA YÜKLEME FORMU (Test etmek için HTML)

@app.get("/")
async def main():
    """
    Basit bir tarayıcı formu döndürür.
    Birden fazla dosya yükleme test edilebilir.
    """
    content = """
    <body>
    <h3>Bytes ile dosya yükleme</h3>
    <form action="/upload-bytes/" method="post" enctype="multipart/form-data">
        <input name="file" type="file">
        <input type="submit">
    </form>

    <h3>UploadFile ile dosya yükleme</h3>
    <form action="/upload-file/" method="post" enctype="multipart/form-data">
        <input name="file" type="file">
        <input type="submit">
    </form>

    <h3>Çoklu dosya yükleme</h3>
    <form action="/upload-multiple/" method="post" enctype="multipart/form-data">
        <input name="files" type="file" multiple>
        <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

# ÖZET:
# - Küçük dosyalar → bytes
# - Büyük dosyalar → UploadFile
# - Çoklu dosyalar → list[UploadFile]
# - Form veri tipi → multipart/form-data
