#FASTAPI PATH PARAMETRELERİ EĞİTİM DOSYASI

from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# 1) BASİT YOL PARAMETRESİ

"""
Bir yol parametresi, URL içinde değişen bir değerdir.
Ör:   /items/10 → item_id = "10"
"""

@app.get("/items/{item_id}")
async def read_item_basic(item_id):
    """
    item_id burada string olarak yakalanır
    çünkü herhangi bir tip belirteci verilmedi.
    """
    return {"received_item_id": item_id}


# 2) TİP BELİRTECİ OLAN YOL PARAMETRESİ

"""
Tip belirteci kullanıldığında, FastAPI:
- Değeri otomatik olarak o tipe dönüştürür
- Yanlış tip gelirse otomatik doğrulama hatası döndürür
"""

@app.get("/items-int/{item_id}")
async def read_item_typed(item_id: int):
    """
    item_id artık int olmak zorunda.
    /items-int/3 → çalışır
    /items-int/foo → otomatik 422 doğrulama hatası
    """
    return {"item_id_is_integer": item_id}


# 3) YOL SIRALAMASININ ÖNEMİ

"""
Daha spesifik yol (sabit yol) her zaman önce gelmelidir.
Aksi halde, değişken yakalayan yol tüm istekleri yutabilir.
"""

@app.get("/users/me")
async def read_current_user():
    """
    /users/me → burası çalışmalı
    Eğer altta olsaydı, /users/{user_id} tarafından yakalanabilirdi.
    """
    return {"user": "current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    """
    /users/alex → alex döner
    Ama /users/me → üstteki endpoint sayesinde buraya düşmez.
    """
    return {"user": user_id}


# 4) AYNI YOLU İKİ KEZ TANIMLAMA HATASI

"""
Aynı path ve aynı HTTP methodu birden fazla tanımlanamaz.
İkinci tanım birincisini override ETMEZ.
FastAPI baştan hata verir.
"""

@app.get("/duplicate")
def duplicate1():
     return {"msg": "A"}

@app.get("/duplicate")
def duplicate2():
     return {"msg": "B"}

# HATA: FastAPI duplicate route error.


# 5) ENUM (ÖN TANIMLI DEĞERLER) İLE PATH PARAMETRESİ

"""
Enum sayesinde path parametresinin alabileceği değerler sınırlanabilir.
Dokümantasyonda otomatik olarak seçenekli menü çıkar.
"""

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet  = "resnet"
    lenet   = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    model_name parametresi artık sadece şu olabilir:
    - alexnet
    - resnet
    - lenet

    Yanlış bir değer → otomatik doğrulama hatası (422)
    """
    if model_name is ModelName.alexnet:
        return {"model": model_name, "info": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model": model_name, "info": "LeCNN all the images"}

    return {"model": model_name, "info": "Have some residuals"}


# 6) PATH CONVERTER (DOSYA YOLU YAKALAMA)

"""
Normal bir path parametresi "/" karakteri gördüğünde ayrılır.
Ama dosya yolu gibi bir değer istiyorsak parametreyi :path ile tanımlarız.

Ör:
    /files/home/user/data.txt
Aksi durumda {file_path} sadece 'home' kısmını yakalardı.
"""

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    file_path → tüm yolu olduğu gibi alır
    Ör: /files/home/john/data.txt
         file_path = "home/john/data.txt"
    """
    return {"full_path_received": file_path}
#ÖRNEK;
#URL:
#/files/home/user/data.txt
#Normal parametre olsaydı:
#@app.get("/files/{file_path}")
#Sonuç:
#file_path = "home"
#Yanlış — çünkü /user/data.txt kısmı kayboldu.
#PATH CONVERTER ile sonuç:
#@app.get("/files/{file_path:path}")
#Sonuç:
#file_path = "home/user/data.txt"
#Doğru — tüm yol alındı.
