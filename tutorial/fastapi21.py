#FASTAPI – FORM MODELLERİ (Form Models)
# Bu dosya, form verilerini Pydantic modelleri ile nasıl
# kullanabileceğimizi adım adım açıklar.
#
# Normalde Form alanlarını tek tek yazardık:
#   username: Annotated[str, Form()]
#   password: Annotated[str, Form()]
#
# Ancak bu yöntem büyüyen sistemlerde karışır.
# Bu yüzden form alanlarını bir Pydantic modeline toplarız.
#
# NOT:
# Form verisi kullanmak için gerekli paket:
#     pip install python-multipart

from typing import Annotated
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

# 1) FORM ALANLARI İÇİN Pydantic MODEL KULLANIMI

class LoginForm(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[LoginForm, Form()]):
    """
    Bu endpoint form verisini bir Pydantic modele aktarır.
    Artık username ve password ayrı ayrı alınmaz.
    Form() → gelen verinin form-data olduğunu belirtir.
    """
    return data

# 2) EKSTRA FORM ALANLARINI YASAKLAMAK (Güvenlik)

class StrictLoginForm(BaseModel):
    username: str
    password: str

    # Modelde olmayan alanları kabul etme!
    model_config = {"extra": "forbid"}


@app.post("/secure-login/")
async def secure_login(data: Annotated[StrictLoginForm, Form()]):
    """
    Extra form alanları gönderilirse API hata döner.
    Bu yöntem güvenlik için önemlidir.
    """
    return data


# 3) GÖNDERİLEBİLECEK FORM ÖRNEĞİ:
#
# username=Rick
# password=PortalGun
#
# Ama aşağıdaki gibi bir veri gönderilirse:
#
# username=Rick
# password=PortalGun
# extra=Hello
#
# API şu hatayı döner:
#
#   "Extra inputs are not permitted"


