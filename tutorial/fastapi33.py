"""
Bu dosya FastAPI’de metadata, tag açıklamaları ve
docs URL özelleştirmelerinin nasıl yapıldığını gösterir.
"""

from fastapi import FastAPI

# ---------------------------------------------------------
# 1) TAG METADATA TANIMI
# ---------------------------------------------------------
# API dokümantasyonunda kategorileri açıklamak için kullanılır.
tags_metadata = [
    {
        "name": "users",  # path operation'daki tags=["users"] ile eşleşir
        "description": (
            "Kullanıcılarla ilgili işlemler. "
            "**Giriş yapma** gibi süreçler de buradadır."
        ),
    },
    {
        "name": "items",
        "description": "Eşyaları yöneten tüm işlemler. Çok _havalılar_.",
        "externalDocs": {
            "description": "Items hakkında ek doküman",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

# ---------------------------------------------------------
# 2) FASTAPI UYGULAMASI OLUŞTURMA
# ---------------------------------------------------------
app = FastAPI(
    title="MagicAPI",
    summary="Basit ama büyülü bir API",
    description=(
        "Bu API kullanıcılar ve eşyalar üzerinde işlemler yapmanızı sağlar.\n"
        "Açıklama bölümünde **Markdown** kullanabilirsiniz."
    ),
    version="1.0.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "John Developer",
        "email": "john@example.com",
    },
    license_info={
        "name": "MIT",
        "identifier": "MIT"   # url yerine identifier da kullanılabilir
    },
    openapi_tags=tags_metadata,  # tag metadataları ekledik
    openapi_url="/api/openapi.json",  # OpenAPI şemasının yeni yolu
    docs_url="/documentation",  # Swagger UI yeni URL
    redoc_url="/redocumentation",  # ReDoc yeni URL
)

# ---------------------------------------------------------
# 3) ÖRNEK ENDPOINTLER
# ---------------------------------------------------------

@app.get("/users/", tags=["users"])
async def get_users():
    """Kullanıcı listesi döner."""
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    """Eşya listesi döner."""
    return [{"name": "wand"}, {"name": "broom"}]


# ---------------------------------------------------------
# Ana endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Metadata örneği çalışıyor!"}
