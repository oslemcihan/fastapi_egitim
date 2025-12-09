#FASTAPI – RESPONSE MODELLERİ

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Any

app = FastAPI()

#GİRİŞ ve ÇIKIŞ MODELLERİNİ AYIRMA (GÜVENLİK)

class UserIn(BaseModel):
    """
    Kullanıcıdan alınan model.
    Tehlikeli alanlar içerir (ör. password).
    """
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    """
    API’nin kullanıcıya göndermesi gereken model.
    Şifre içermez.
    """
    username: str
    email: EmailStr


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    """
    Dikkat:
    - Fonksiyon UserIn modelini döndürüyor.
    - Ancak response_model=UserOut olduğu için FastAPI
      password alanını otomatik siler.
    """
    return user  # İçinde password var ama kullanıcıya gönderilmez.


#İDE ve MYPY UYUMLU – KALITIM YÖNTEMİ

class BaseUser(BaseModel):
    username: str
    email: EmailStr


class UserIn2(BaseUser):
    """
    Bu model BaseUser'dan kalıtım alıyor ve ek alan ekliyor.
    """
    password: str


@app.post("/user2/")
async def create_user2(user: UserIn2) -> BaseUser:
    """
    - IDE der ki: BaseUser dönebilirsin çünkü UserIn2, BaseUser'ın alt sınıfıdır.
    - FastAPI ise dönen veriyi BaseUser alanlarına göre filtreler.
    """
    return user  # password alanı otomatik çıkarılır.


#MODELDE VARSAYILAN DEĞERLERİ YOK SAYMA

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 20},
    "bar": {"name": "Bar", "price": 50, "tax": 20.2},
}


@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True #Default değerleri eklemez, sadece gerçek veriyi döndürür
)
async def read_item(item_id: str):
    """
    - Varsayılan değerleri döndürmez (exclude_unset=True)
    - Sadece gerçekte mevcut olan alanlar döner
    """
    return items[item_id]


#BELİRLİ ALANLARI SEÇME / ÇIKARMA

@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    response_model_exclude={"tax"}
)
async def read_public_item(item_id: str):
    """
    Bu endpoint sadece 'tax' alanını kaldırır.
    """
    return items[item_id]



#ÖZET
"""
✔ response_model → Çıkışın doğrulanması + filtrelenmesi + dokümantasyon
✔ return type → IDE ve mypy için ipucu (FastAPI bundan bağımsız olabilir)
✔ response_model_exclude_unset → Varsayılan değerleri çıkarır
✔ response_model_exclude / include → Belirli alanları filtreler
✔ Inheritance yöntemi → Hem güvenlik hem IDE uyumluluğu için en iyi yöntem
"""

