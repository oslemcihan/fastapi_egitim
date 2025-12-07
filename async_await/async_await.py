import asyncio
import time

# 1) SENKRON (def) ÖRNEĞİ — Her iş sırayla yapılır.

def slow_sync_task(task_name: str):
    """
    Bu fonksiyon beklerken CPU boş durur. (senkron)
    """
    print(f"{task_name} başladı...")
    time.sleep(2)  # 2 saniye BEKLE → bu sırada hiçbir şey yapamazsın
    print(f"{task_name} bitti!")
    return f"{task_name} sonucu"



# 2) ASENKRON (async) ÖRNEĞİ — Beklerken başka işler yapılır.

async def slow_async_task(task_name: str):
    """
    Bu fonksiyon await ile beklerken, CPU boş durmaz,
    başka async görevleri çalıştırır → concurrency olur.
    """
    print(f"{task_name} başladı...")
    await asyncio.sleep(2)  # 2 saniye bekliyor ama diğer işler devam edebilir
    print(f"{task_name} bitti!")
    return f"{task_name} sonucu"


# 3) SENKRON ÇALIŞMA ÖRNEĞİ
# Her iş teker teker yapılır → toplam 4 saniye sürer

def run_sync_example():
    print("\n--- SENKRON ÇALIŞMA ÖRNEĞİ ---")
    start = time.time()

    slow_sync_task("Görev 1")
    slow_sync_task("Görev 2")

    end = time.time()
    print(f"Senkron toplam süre: {end - start:.2f} saniye\n")


# 4) ASENKRON ÇALIŞMA ÖRNEĞİ
# Görevler aynı anda başlar → 2 saniyede biter.


async def run_async_example():
    print("\n--- ASENKRON ÇALIŞMA ÖRNEĞİ ---")
    start = time.time()

    # iki görevi aynı anda başlatıyoruz
    task1 = asyncio.create_task(slow_async_task("Görev 1"))
    task2 = asyncio.create_task(slow_async_task("Görev 2"))

    # her ikisini de bekle
    await task1
    await task2

    end = time.time()
    print(f"Asenkron toplam süre: {end - start:.2f} saniye\n")


# 5) await kullanımı — NEDEN async def gerekli?


async def why_await_example():
    """
    await sadece async fonksiyon içinde çalışır.
    Aşağıdaki örnek bunu gösterir.
    """
    print("await sadece async fonksiyonlarda kullanılır.")

