import sys
import os

# 1) HANGİ PYTHON KULLANILIYOR?
# Sanal ortam aktifse Python yolu .venv içinden gelir.
# Aktif değilse global Python kullanılır.

def show_python_path():
    """
    sys.executable → şu anda kullanılan python.exe veya python binary'sinin tam yolu.
    Sanal ortam aktifse: project/.venv/bin/python
    Global ortamda ise: /usr/bin/python veya C:\\Python311\\python.exe
    """
    print("Şu anda kullanılan Python yolu:")
    print(sys.executable)
    print()


# 2) PAKET VERSİYONU NEDEN ÖNEMLİ?
# Farklı projelerde aynı paketin farklı sürümlerine ihtiyaç olabilir.

def simulate_project_dependencies():
    """
    Bu fonksiyon, farklı projelerin aynı pakete farklı sürümler ihtiyaç duymasını simüle eder.
    Gerçekte paket import edilemiyor olabilir ama mantığı görmek yeterli.
    """

    project1_requires = "harry v1"
    project2_requires = "harry v3"

    print("Proje 1 (philosophers-stone) paket gereksinimi:", project1_requires)
    print("Proje 2 (prisoner-of-azkaban) paket gereksinimi:", project2_requires)

    print("""
  Eğer global ortama kurarsan:
- harry==1 kurarsın → Proje 1 çalışır
- Sonra harry==3 kurarsın → Proje 2 çalışır ama Proje 1 bozulur

  Her paket değişiminde eski projeler bozulabilir.
    """)

    print("Sanal ortam kullanırsan:")
    print("""
  philosophers-stone/.venv → harry v1 içerir
  prisoner-of-azkaban/.venv → harry v3 içerir

 Projeler birbirini BOZMAZ.
 Her proje kendi ortamında kendi paket versiyonlarını kullanır.
    """)

    print()


# 3) SANAL ORTAM AKTİF Mİ?
# Basit bir kontrol: VIRTUAL_ENV environment variable'ı sanal ortam aktifken oluşur.


def check_virtual_env():
    venv_path = os.getenv("VIRTUAL_ENV")

    if venv_path:
        print("Sanal ortam AKTİF!")
        print("Sanal ortam dizini:", venv_path)
    else:
        print("Sanal ortam aktif değil (GLOBAL Python kullanılıyor).")

    print()


# 4) GERÇEK SENARYO – SANAL ORTAM YOKSA PROJE KARIŞIKLIĞI

def scenario_without_venv():
    print("Sanal ortam YOKKEN gerçek hayat senaryosu:")
    print("""
- Bir projede FastAPI 0.95 gerekir.
- Başka projede FastAPI 0.110 gerekir.
- Global ortama hangisini yüklersen o proje çalışır, diğeri bozulur.
- Aynı PC'de 10 proje varsa hepsi birbirinin paket versiyonunu bozar.

Bu yüzden GLOBAL kurulum çok risklidir.
""")
    print()


# 5) GERÇEK SENARYO – SANAL ORTAM İLE TEMİZ ÇALIŞMA

def scenario_with_venv():
    print("Sanal ortam ile temiz çalışma örneği:")
    print("""
- Her projede yalnızca ihtiyaç duyulan paketler kurulur.
- Paket versiyonları karışmaz.
- Editor (VS Code / PyCharm) doğru ortamı görünce autocomplete mükemmel çalışır.
- Deploy ederken aynı ortamı sunucuya aktarabilirsin.
""")
    print()
