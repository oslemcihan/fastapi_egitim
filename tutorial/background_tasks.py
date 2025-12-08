"""
Bu dosya FastAPI BackgroundTasks özelliğini açıklayan örnek bir uygulamadır.
Arkaplan görevleri, API cevabı döndükten sonra çalışmaya devam eden fonksiyonlardır.
Kullanıcı beklememiş olur, performans artar.
"""

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# -----------------------------------------------------------
# ARKA PLANDA ÇALIŞACAK GÖREV
# -----------------------------------------------------------

def save_log_to_file(message: str):
    """
    Bu fonksiyon arka planda çalışır.
    Çok basit bir işlem yapıyor: bir log dosyasına veri yazıyor.
    Normalde dosya yazmak yavaş olabilir, bu yüzden arka plana almak mantıklı.
    """
    with open("log.txt", "a") as f:
        f.write(message + "\n")
#with: Dosyayı güvenli şekilde açmak, İş bittiğinde otomatik olarak kapatmak, Hata olsa bile dosyayı kapatmak

# -----------------------------------------------------------
# NORMAL ENDPOINT (arka plan görevi kullanan)
# -----------------------------------------------------------

#BackgroundTasks: API cevabı döndükten sonra arka planda işlem yapmanı sağlar.
@app.post("/process/{username}")
async def process_user(username: str, background_tasks: BackgroundTasks):
    """
    Bu endpoint bir kullanıcıyı işlemden geçiriyor (sözde).
    Kullanıcıya hemen cevap döneriz fakat arka planda log tutmaya devam ederiz.
    """

    
    background_tasks.add_task( # add_task -> Arkaplan görevine bir işi ekliyoruz
        save_log_to_file,
        f"User {username} was processed."
    )

    # Client hızlı bir cevap alır
    return {"status": "processing started", "user": username}


# -----------------------------------------------------------
# DEPENDENCY İÇİNDE ARKA PLAN GÖREVİ
# -----------------------------------------------------------

def log_query(background_tasks: BackgroundTasks, q: str | None = None):
    """
    Bu fonksiyon dependency olarak kullanılır.
    Eğer ?q=something gelirse, bu bilgiyi log dosyasına arka planda yazar.
    """

    if q:
        background_tasks.add_task(save_log_to_file, f"Query param detected: {q}")

    return q


@app.get("/search")
async def search_items(q: str | None = None, background_tasks: BackgroundTasks = None):
    """
    Hem kullanıcıya sonuç döneriz hem de gelen query bilgisini arka planda kaydederiz.
    """

    # Eğer query varsa log yaz
    if q:
        background_tasks.add_task(save_log_to_file, f"Search query: {q}")

    return {"results": ["item1", "item2"], "query": q}
