# FastAPI'de CORS kullanımını gösteren tam açıklamalı örnek

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1) Frontend hangi adreslerde çalışıyorsa burada belirtmeliyiz.
# ÖRN:
# React: http://localhost:3000
# Vue:   http://localhost:5173
# Angular: http://localhost:4200


allowed_origins = [ #“Origin” şu demektir: PROTOKOL + DOMAİN + PORT
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:4200",
]

# 2) CORS middleware ekliyoruz
# Açıklamalar:
# - allow_origins: Hangi origin’lerin backend’e erişebileceği
# - allow_credentials: Cookie/Auth header gönderimine izin verir
# - allow_methods: Hangi HTTP metodlarına izin verilecek
# - allow_headers: Hangi HEADER’lara izin verilecek

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True, #true ise wildcard * kullanılamaz
    allow_methods=["*"],       # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],       # Tüm header’lara izin ver
)

# 3) Basit bir endpoint
# Frontend bu endpoint’e fetch isteği gönderebilir

@app.get("/hello")
async def hello():
    return {"message": "CORS ayarların doğruysa frontend ulaşabilir!"}

"""
Wildcard (“ * ”) Kullanımı;
"*" kullanarak tüm origin’lere izin verebilirsiniz.
Ama büyük bir sınırlama vardır:
allow_credentials=True ise wildcard kullanılamaz.
Çünkü credentials içeren isteklerde * kullanmak tarayıcı tarafından engellenir.
Credentials kapsamına girenler:
Cookies
Authorization header
Bearer token
Basic auth
Bu nedenle güvenli kullanım:
Eğer cookie/token kullanılıyorsa → kesinlikle tek tek origin belirtmelisin.
"""