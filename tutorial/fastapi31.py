#app/main.py -> Ana uygulama dosyası
from fastapi import FastAPI, Depends

# Diğer modülleri içeri aktarıyoruz
from .routers import users, items
from .internal import admin
from .dependencies import get_query_token, get_token_header

# Global dependency: tüm endpoint'lerde çalışır
app = FastAPI(dependencies=[Depends(get_query_token)])

# users router'ını ekle
app.include_router(users.router)

# items router'ını ekle
app.include_router(items.router)

# admin router'ını özel prefix ve güvenlikle ekle
app.include_router(
    admin.router,
    prefix="/admin",                # tüm path'ler /admin/... olacak
    tags=["admin"],                 # docs'ta "admin" başlığı altında görünür
    dependencies=[Depends(get_token_header)],  # güvenlik
    responses={418: {"description": "I'm a teapot"}}  # örnek özel hata
)

# Ana endpoint
@app.get("/")
def root():
    return {"message": "Hello Bigger Applications!"}


####################################################################################################################
#app/dependencies.py

from fastapi import Header, HTTPException
from typing import Annotated

# Tüm items endpoint'leri bu header'ı ister
async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(400, "X-Token header invalid")

# Tüm uygulama get_query_token bağımlılığını global olarak kullanır
async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(400, "Invalid token")
    

####################################################################################################################
#app/routers/users.py
from fastapi import APIRouter

router = APIRouter()  # Mini-FastAPI router

@router.get("/users/", tags=["users"])
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
def read_user_me():
    return {"username": "current user"}

@router.get("/users/{username}", tags=["users"])
def read_user(username: str):
    return {"username": username}


####################################################################################################################
#app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",                     # tüm path'ler buna eklenir
    tags=["items"],                      # docs için kategori
    dependencies=[Depends(get_token_header)],  # toplu güvenlik
    responses={404: {"description": "Not found"}}
)

fake_items_db = {
    "plumbus": {"name": "Plumbus"},
    "gun": {"name": "Portal Gun"}
}

@router.get("/")
def read_items():
    return fake_items_db

@router.get("/{item_id}")
def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(404, "Item not found")
    return {"item_id": item_id, "name": fake_items_db[item_id]["name"]}


####################################################################################################################
#app/internal/admin.py
from fastapi import APIRouter

# Bu dosyayı değiştirmiyoruz (kurumsal ortak dosya gibi)
router = APIRouter()

@router.post("/")
def update_admin():
    return {"message": "Admin updated"}
