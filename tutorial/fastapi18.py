#FASTAPI – EXTRA MODELLER
#Kullanıcı modelleri, kalıtım, dict unpacking,
#response modelleri, Union modeller

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

#TEMEL MODEL (BASE)

class UserBase(BaseModel):
    """
    User modellerinin ortak alanları burada.
    - Kullanıcı adı
    - Email
    - İsteğe bağlı isim
    """
    username: str
    email: EmailStr
    full_name: str | None = None


#API'YE GİRİŞ YAPAN MODEL (password içerir)

class UserIn(UserBase):
    """
    API'ye kullanıcı oluştururken gönderilecek model.
    Bu model DÜZ PAROLA içerir. (Saklanmaz!)
    """
    password: str


#API'DEN DÖNDÜRÜLEN MODEL (password içermez)

class UserOut(UserBase):
    """
    Kullanıcıya döndürülen model.
    ŞİFRE YOK!
    """
    pass


#VERİTABANINA KAYDEDİLEN MODEL (password hash)

class UserInDB(UserBase):
    """
    Veritabanında saklanan model.
    Düz parola yerine sadece hashed_password saklanır.
    """
    hashed_password: str


#SAHTE PAROLA HASH FONKSİYONU

def fake_password_hasher(raw_password: str):
    """
    Gerçek hayatta BCRYPT, ARGON2 gibi algoritmalar kullanılır.
    Bu sadece örnek amaçlıdır.
    """
    return "supersecret" + raw_password


#USER KAYIT FONKSİYONU (sözde veritabanı)

def fake_save_user(user_in: UserIn):
    """
    - Parola hash'lenir
    - UserInDB modeline çevrilir
    - Veritabanına kaydedilmiş gibi yapılır
    """
    hashed_password = fake_password_hasher(user_in.password)

    # dict() → Pydantic modelini Python dict’e çevirir
    # **dict → "unpacking" ile anahtar-değer olarak aktarılır
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)

    #user_in.dict() → UserIn modelini Python dict'e çevirir
    #** → bu dict’i UserInDB modeline parametre olarak geçer
    #hashed_password=... → ekstra alan ekleriz

    print("User saved! (gerçek değil)")
    return user_in_db


#USER OLUŞTURMA ENDPOINTİ

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    """
    - Girdi modeli UserIn → password içerir
    - Veritabanı modeli UserInDB → hashed_password içerir
    - Çıkış modeli UserOut → password içermez

    FastAPI burada otomatik olarak UserOut alanlarında olmayan
    tüm verileri (ör. password veya hashed_password) filtreler.
    """
    user_saved = fake_save_user(user_in)
    return user_saved


#UNION MODELLER ÖRNEĞİ

from typing import Union

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "Low rider", "type": "car"},
    "item2": {"description": "Aeroplane", "type": "plane", "size": 5},
}

#Union -> Bu endpoint dönen veriye bakıp hangi modelin uygun olduğunu otomatik seçer.
@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    """
    Dönen model CarItem veya PlaneItem olabilir.
    FastAPI bunu otomatik olarak ayırt eder.
    """
    return items[item_id]


#LİSTE MODEL ÖRNEĞİ

class SimpleItem(BaseModel):
    name: str
    description: str

simple_items = [
    {"name": "Foo", "description": "My hero"},
    {"name": "Red", "description": "Aeroplane"},
]

@app.get("/simple-items/", response_model=list[SimpleItem])
async def read_simple_items():
    """
    Bir liste model döndürmek isteyen endpoint.
    """
    return simple_items

#KEY-VALUE RESPONSE MODEL ÖRNEĞİ

@app.get("/weights/", response_model=dict[str, float])
async def read_keyword_weights():
    """
    Anahtarları bilmediğimiz durumlarda dict[str, float] modeli kullanılır.
    """
    return {"foo": 2.3, "bar": 3.4}


#ÖZET
"""
✔ User modellerini farklı amaçlar için ayırmak gerekir.
✔ Kalıtım ile tekrar azaltılır.
✔ dict() ve ** ile model → model dönüşümü yapılır.
✔ response_model gizli veriyi filtreler.
✔ Union modeller çoklu tip döndürmeye izin verir.
✔ Liste ve dict modeller de response_model olarak kullanılabilir.
"""
