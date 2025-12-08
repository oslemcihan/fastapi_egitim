#SQLModel + FastAPI CRUD Uygulaması (Detaylı Açıklamalı)


from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select



# 1) SQL MODELLERİ

# Tüm modellerin ortak alanlarını koyduğumuz base model
# (Miras almak için kullanılır)
class HeroBase(SQLModel):
    name: str = Field(index=True)       # İsim alanı → index=True hızlı arama yapmayı sağlar
    age: int | None = Field(default=None, index=True)  # Yaş opsiyoneldir


# Veritabanında bir tablo oluşturulacak model
# table=True YAZILMAZSA SQL tablosu oluşmaz!
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  # Birincil anahtar
    secret_name: str  # Bu alan sadece DB’de tutulur, API'ye döndürmeyiz


# API’den dönen güvenli model
# secret_name yoktur → gizlilik için
class HeroPublic(HeroBase):
    id: int  # API’ye dönecek id (zorunlu)


# Kullanıcı yeni kayıt yaparken göndereceği model
class HeroCreate(HeroBase):
    secret_name: str  # Yeni kayıt için gizli isim gerekir


# PATCH güncellemelerinde kullanılan model
# Her alan opsiyoneldir → hangisi verilmişse sadece o güncellenir
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None



# 2) VERİTABANI BAĞLANTISI

# SQLite dosya yolu
sqlite_url = "sqlite:///database.db"

# Engine → veritabanı motoru
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


# Uygulama başlarken tabloları oluştur
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



# 3) SESSION DEPENDENCY

def get_session():
    """
    Her istek geldiğinde çalışır.
    with Session(...) → otomatik aç/kapa işlemi sağlar.
    yield session → endpoint'e session gönderilir.
    """
    with Session(engine) as session:
        yield session  # Bu session endpoint’te kullanılacak


# Annotated ile daha sade kullanım
SessionDep = Annotated[Session, Depends(get_session)]



# 4) FASTAPI UYGULAMASI

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()  # Uygulama açılırken tabloları oluştur


# 5) CRUD ENDPOINTLERİ

# -----------------------
# CREATE
# -----------------------
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    """
    Kullanıcı HeroCreate modeline uygun JSON gönderir.
    Bu model Hero (veritabanı modeli) formatına dönüştürülür.
    """
    db_hero = Hero.model_validate(hero)  # HeroCreate → Hero dönüşümü
    session.add(db_hero)                 # Veritabanına ekle
    session.commit()                     # Kayıt işlemini tamamla
    session.refresh(db_hero)             # Eklenen kaydı yeniden yükle (ID elde etmek için)

    return db_hero  # API HeroPublic modeli döner (secret_name gizlenir)


# -----------------------
# READ ALL
# -----------------------
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,  # Atlanacak kayıt sayısı
    limit: Annotated[int, Query(le=100)] = 100  # En fazla 100 kayıt getir
):
    heroes = session.exec(
        select(Hero).offset(offset).limit(limit)
    ).all()

    return heroes


# -----------------------
# READ ONE
# -----------------------
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:  # Eğer ID bulunamazsa
        raise HTTPException(status_code=404, detail="Hero not found")

    return hero


# -----------------------
# UPDATE (PATCH)
# -----------------------
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, update: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)

    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")

    # Kullanıcının gönderdiği alanları al (None olmayanlar)
    update_data = update.model_dump(exclude_unset=True)

    # SQLModel’ın özel update fonksiyonu
    hero_db.sqlmodel_update(update_data)

    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)

    return hero_db


# -----------------------
# DELETE
# -----------------------
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()

    return {"ok": True}
