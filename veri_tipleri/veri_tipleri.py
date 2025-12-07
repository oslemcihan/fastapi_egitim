# Python Tip Belirteçleri Örnek Dosyası


from typing import List, Tuple, Set, Dict, Optional, Union
from datetime import datetime
from pydantic import BaseModel

# 1) Basit Tipler

def get_full_name(first_name: str, last_name: str) -> str:
    """
    str -> metin tipidir.
    Fonksiyon: İki string alır, baş harflerini büyütür, birleştirip döner.
    """
    return first_name.title() + " " + last_name.title()

# 2) Tip Belirteçleri ile Hata Kontrolü


def get_name_with_age(name: str, age: int) -> str:
    """
    int -> tam sayı tipidir.
    Burada age int olduğu için doğrudan string ile toplanamaz.
    """
    return name + " is this old: " + str(age)


# 3) Generic Tipler: List

def process_items_list(items: List[str]):
    """
    List[str] -> Her elemanı str olan bir liste.
    List = birden fazla veri tutan yapı.
    """
    for item in items:
        print(item.upper())


# 4) Tuple ve Set

def process_tuple_set(
    items_t: Tuple[int, int, str], 
    items_s: Set[bytes]
):
    """
    Tuple -> sabit uzunluklu liste gibidir, elemanların tipleri sıralı verilir ve de değiştirilemeler. ekleme silme vb. yapılamaz.
    Set -> sırasız ve tekrarsız eleman kümesidir.
    """
    print("Tuple:", items_t)
    print("Set:", items_s)


# 5) Dict (Sözlük)


def process_dict(prices: Dict[str, float]):
    """
    Dict[key_type, value_type]
    Dict -> anahtar:değer yapısıdır.
    Örn: {"elma": 3.5}
    """
    for name, price in prices.items():
        print(f"{name} -> {price} TL")
"""
f-string -> string içine değişken gömebilme yöntemi.
süslü parantez içindeki değişken doğrudan yazıya eklenir.
"""


# 6) Optional

def say_hi(name: Optional[str] = None):
    """
    Optional[str] -> str olabilir veya None olabilir.
    """
    if name:
        print(f"Hello {name}")
    else:
        print("Hello World")


# 7) Sınıflar için Tip Belirteci

class Person:
    """
    Sınıfın tip belirteci ile kullanımı.
    """
    def __init__(self, name: str):
        self.name = name
"""
__init__ -> Bu nesneyi BAŞLATMA metodu.
"""

def get_person_name(person: Person) -> str:
    """
    Parametre olarak Person sınıfı bekler.
    """
    return person.name


# 8) Pydantic Model Örneği -> Veri Doğrulama yapar

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: Union[datetime, None] = None  # datetime veya None olabilir
    friends: List[int] = []  # listede sadece int bulunur


# Pydantic doğrulama örneği
external_data = {
    "id": "123",                # string gelir ama Pydantic int'e çevirir
    "signup_ts": "2020-01-01 10:00",
    "friends": [1, "2", b"3"],  # Pydantic hepsini int yapar
}

user = User(**external_data)
"""
**external_data:
Sözlüğü açar
Anahtarlarını fonksiyon parametresi yapar
"""

print("\n--- Pydantic Kullanımı ---")
print(user)
print("User ID:", user.id)