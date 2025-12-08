#FASTAPI EXTRA DATA TYPES ÖRNEKLERİ

from fastapi import FastAPI, Body
from datetime import datetime, timedelta, time
from uuid import UUID
from typing import Annotated

"""
Bu dosya FastAPI'nin desteklediği gelişmiş veri tiplerini göstermektedir.

FastAPI + Pydantic sayesinde:
- UUID
- datetime
- date
- time
- timedelta
- bytes
- Decimal
gibi veri tiplerini otomatik doğrular, dönüştürür ve dökümante eder.
"""

app = FastAPI()

#GELİŞMİŞ VERİ TİPLERİ KULLANAN ENDPOINT

@app.put("/items/{item_id}")
async def read_items(
    # UUID türünde path parametresi
    item_id: UUID,

    # datetime → ISO formatlı string olarak gelir, datetime objesine çevrilir
    start_datetime: Annotated[datetime, Body()],

    # başka bir datetime
    end_datetime: Annotated[datetime, Body()],

    # timedelta → float saniye olarak gönderilir, timedelta nesnesine dönüşür
    process_after: Annotated[timedelta, Body()],

    # time → sadece saat/dakika/saniye bilgisini alır
    repeat_at: Annotated[time | None, Body()] = None,
):
    """
    ÖRNEK JSON:
    {
        "start_datetime": "2024-01-12T15:30:00",
        "end_datetime": "2024-01-12T18:00:00",
        "process_after": 3600,  # 1 saat = 3600 saniye
        "repeat_at": "14:00:00"
    }
    """

    # Normal Python işlemleri yapılabilir:
    start_process = start_datetime + process_after   # datetime + timedelta
    duration = end_datetime - start_process          # iki datetime arası fark

    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }

