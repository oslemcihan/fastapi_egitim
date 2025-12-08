#BODY - FIELDS 

from fastapi import FastAPI, Body
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

# 1) FIELD KULLANILAN Pydantic MODELİ => Pydantic modeline Field() ekleyerek, body içindeki 
# alanlara detaylı doğrulama ve açıklama ekleyebilirsin.

class Item(BaseModel):
    """
    Bu model içindeki alanlara Field() ile ek doğrulama yapıyoruz.
    Field, Query/Path/Body ile aynı doğrulama parametrelerini kullanır.
    """

    # Normal zorunlu bir alan
    name: str

    # Opsiyonel alan, fakat Field ile:
    # - başlık (title)
    # - max_length doğrulaması ekledik.
    description: str | None = Field(
        default=None,
        title="Ürünün açıklaması",
        max_length=300
    )

    # Field ile price > 0 zorunluluğu ekledik
    price: float = Field(
        gt=0,
        description="Fiyat sıfırdan büyük olmalıdır"
    )

    # Normal opsiyonel alan
    tax: float | None = None


# 2) BODY PARAMETRESİ ALAN ENDPOINT

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[Item, Body(embed=True)]  # Model embed edilerek alınıyor
):
    """
    embed=True:
    Gövdenin şu şekilde olmasını sağlar:

    {
        "item": {
            "name": "...",
            "description": "...",
            "price": 10
        }
    }

    Field() ile tanımladığımız tüm doğrulamalar body içi veri kontrolünde uygulanır.
    """
    return {"item_id": item_id, "item": item}

