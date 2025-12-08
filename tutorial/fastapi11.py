#FASTAPI - REQUEST BODY EXAMPLE VERİ TANIMLAMA

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

# 1) MODEL SEVİYESİNDE ÖRNEK TANIMI (json_schema_extra)

class Item(BaseModel):
    """
    Bu model için bir örnek veri modeli seviyesinde ekleniyor.
    Swagger UI bu örneği otomatik gösterecektir.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # JSON Schema içine örnek eklenir
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Laptop",
                    "description": "Yüksek performanslı laptop",
                    "price": 12500.5,
                    "tax": 750
                }
            ]
        }
    }


# 2) FIELD(examples) KULLANIMI

class ItemWithFieldExamples(BaseModel):
    """
    Her bir alan için ayrı örnekler tanımlanabilir.
    """
    name: str = Field(examples=["Telefon"])
    description: str | None = Field(default=None, examples=["Akıllı telefon"])
    price: float = Field(examples=[8999.99])
    tax: float | None = Field(default=None, examples=[500.0])


# 3) BODY(examples) — TEK ÖRNEK KULLANMA

@app.put("/items/example-body/{item_id}")
async def update_item_example_body(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Masa",
                    "description": "Ahşap çalışma masası",
                    "price": 750.0,
                    "tax": 50.0
                }
            ]
        )
    ]
):
    return {"item_id": item_id, "item": item}


# 4) OPENAPI_EXAMPLES — ÇOKLU ÖRNEKLER

@app.put("/items/multiple-examples/{item_id}")
async def update_item_multiple_examples(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "Normal veri örneği",
                    "description": "Geçerli bir ürün örneği",
                    "value": {
                        "name": "Kalem",
                        "description": "Mavi tükenmez kalem",
                        "price": 12.5,
                        "tax": 1.2
                    }
                },
                "converted": {
                    "summary": "Dönüştürülebilen veri",
                    "description": "FastAPI string '35.4'u float'a dönüştürür",
                    "value": {
                        "name": "Defter",
                        "price": "35.4"
                    }
                },
                "invalid": {
                    "summary": "Geçersiz veri",
                    "description": "FastAPI bunu dönüştüremez, hata verir",
                    "value": {
                        "name": "Silgi",
                        "price": "otuz beş"
                    }
                }
            }
        )
    ]
):
    return {"item_id": item_id, "item": item}
