#BODY – MULTIPLE PARAMETERS 

from fastapi import FastAPI, Path, Body
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

# 1) MODELLER

class Item(BaseModel):
    """
    İtem modelimiz:
    - name → zorunlu
    - description → opsiyonel
    - price → zorunlu
    - tax → opsiyonel
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    """
    Kullanıcı modeli:
    - username → zorunlu
    - full_name → opsiyonel
    """
    username: str
    full_name: str | None = None


# 2) PATH + QUERY + BODY PARAMETRESİ BİRLİKTE KULLANMA

@app.put("/items/{item_id}")
async def update_item_basic(
    item_id: Annotated[int, Path(title="Ürün ID", ge=0, le=1000)],
    q: str | None = None,      # QUERY parametresi
    item: Item | None = None   # BODY parametresi (opsiyonel)
):
    """
    Bu örnek:
    - Path, Query ve Body aynı anda nasıl alınır?
    - item body'den gelmezse None olabilir.
    """
    results = {"item_id": item_id}

    if q:
        results["q"] = q
    if item:
        results["item"] = item

    return results


# 3) BİRDEN FAZLA BODY PARAMETRESİ

@app.put("/items/{item_id}/full")
async def update_item_full(item_id: int, item: Item, user: User):
    """
    Burada hem 'item' hem 'user' gövdeden gelecektir.

    FastAPI JSON'ı şöyle bekler:

    {
        "item": {...},
        "user": {...}
    }
    """
    return {"item_id": item_id, "item": item, "user": user}


# 4) BODY İÇİNDE TEKİL DEĞER ALMA

@app.put("/items/{item_id}/importance")
async def update_item_importance(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)]
):
    """
    importance → normalde query sanılırdı.
    Body() ile body içinden alındığını belirtmiş oluyoruz.

    Beklenen JSON:

    {
        "item": {...},
        "user": {...},
        "importance": 5
    }
    """
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }


# 5) TEK BODY PARAMETRESİNİ EMBED ETME (embed=True)

@app.put("/items/{item_id}/embedded")
async def update_item_embedded(
    item_id: int,
    item: Annotated[Item, Body(embed=True)]
):
    """
    Body’deki veriyi bir anahtar içine sararak daha düzenli ve yapılandırılmış JSON formatı oluşturmanı sağlar.

    Normalde body şöyle olurdu:

    {
        "name": "...",
        "price": 10
    }

    embed=True ile şöyle beklenir:

    {
        "item": {
            "name": "...",
            "price": 10
        }
    }
    """
    return {"item_id": item_id, "item": item}

