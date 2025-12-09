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
class HeroUpdate(SQLModel): #HeroUpdate in miras aldığı sınafa ve diğerlerine bak bu farklı çünkü her alan opsiyonel olsun diye
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None



# 2) VERİTABANI BAĞLANTISI

# SQLite dosya yolu
sqlite_url = "sqlite:///database.db" # -> Bulunduğun klasörde database.db adında bir SQLite veritabanı dosyası oluştur ve ona bağlan.

# Engine → veritabanı motoru
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
# engine = Veritabanı ile FastAPI/SQLModel arasındaki köprü.
# connect_args={"check_same_thread": False} -> Merak etme, aynı veritabanı bağlantısını birden fazla thread kullanabilir. ama açık kalırsa hata verir. Bu ayar o hatayı engeller.

# Uygulama başlarken tabloları oluştur
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    #Amaç: SQLModel ile tanımladığın tüm table=True modellerini bulup, veritabanında 
    #karşılık gelen tabloları oluşturmak.
    #metadata: üm modellerin (tabloya dönüşecek olanların) bilgisini tutan bir yapı.
    #create_all() fonksiyonu: metadata içindeki tüm tablo modellerini alır,  
    #engine üzerinden veritabanına bağlanır, Eksik olan tabloları oluşturur
    #Engin ile  kullanılmasının sebebi, hangi veritabanına bağlanacağını bilmesi için.



# 3) SESSION DEPENDENCY
#Session, veritabanı ile işlem yaptığın bağlantıdır.
def get_session():
    """
    Her istek geldiğinde çalışır.
    with Session(...) → otomatik aç/kapa işlemi sağlar.
    yield session → endpoint'e session gönderilir.
    """
    with Session(engine) as session: #Bu, otomatik session açıp kapatma prensibidir.
        yield session  # Bu session endpoint’te kullanılacak


# Annotated ile daha sade kullanım
SessionDep = Annotated[Session, Depends(get_session)]



# 4) FASTAPI UYGULAMASI

app = FastAPI() #Yeni bir FastAPI uygulaması oluşturur. Bu satır olmadan api çalışmaz.


@app.on_event("startup") # Uygulama açılırken çalışacak fonksiyon. Aslında fastai bazı olaylar için özwl fonk. tanımına izin verir onşardan biridir.
def on_startup():
    create_db_and_tables()  # Uygulama açılırken tabloları oluştur


# 5) CRUD ENDPOINTLERİ

# -----------------------
# CREATE
# -----------------------
@app.post("/heroes/", response_model=HeroPublic) #response_model=HeroPublic → Response olarak HeroPublic dönecek
def create_hero(hero: HeroCreate, session: SessionDep):
    """
    Kullanıcı HeroCreate modeline uygun JSON gönderir.
    Bu model Hero (veritabanı modeli) formatına dönüştürülür.
    """
    db_hero = Hero.model_validate(hero)  # HeroCreate → Hero dönüşümü
    session.add(db_hero)                 # Bu, Hero objesini veritabanı işlem kuyruğuna ekler.
    session.commit()                     # Bekleyen tüm işlemler veritabanına uygulanır
    session.refresh(db_hero)             # Eklenen kaydı yeniden yükle (ID elde etmek için)

    return db_hero  # API HeroPublic modeli döner (secret_name gizlenir)


# -----------------------
# READ ALL
# -----------------------
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep, #SessionDep bu bir kısalmadır aslında Session = Depends(get_session)
    offset: int = 0,  # Atlanacak kayıt sayısı
    limit: Annotated[int, Query(le=100)] = 100  # En fazla 100 kayıt getir
):
    heroes = session.exec( # -> session.exec(...): Bu SQL sorgusunu veritabanında çalıştırır.
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
    #Veritabanından gelen hero_db objesinin üzerinde, sadece gönderilen alanları güncelle.
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
