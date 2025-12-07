# ENVIRONMENT VARIABLES – 
# Python kodunun dışında, işletim sisteminde tanımlanan bir değişkendir(terminalde).
# API şifresi saklamak, Veri tabanı bağlantı adresi saklamak, Uygulama adı, debug modu, port numarası saklamak gibi durumlarda
import os


# 1) ORTAM DEĞİŞKENİ OKUMA

# getenv("KEY", "varsayılan") → Eğer ortam değişkeni yoksa ikinci değer döner.
#getenv ile ortam değişkenlerini okuyoruz
APP_NAME = os.getenv("APP_NAME", "MyDefaultApp")  
DEBUG_MODE = os.getenv("DEBUG_MODE", "false")      
MAX_CONNECTIONS = os.getenv("MAX_CONNECTIONS", "10")


# 2) TİP DÖNÜŞTÜRME
# Ortam değişkenleri hep str olarak gelir!
# Bu yüzden ihtiyaca göre dönüştürmemiz gerekir.

# boolean dönüştürme
DEBUG_MODE_BOOL = DEBUG_MODE.lower() == "true"

# integer dönüştürme
MAX_CONNECTIONS_INT = int(MAX_CONNECTIONS)


# 3) ORTAM DEĞİŞKENİ OLMADIĞINDA YALNIZCA O PROGRAM İÇİN TANIMLAMA
# Bunu terminalde şu şekilde çalıştırabilirsiniz:
# APP_NAME="CustomName" python main.py
# Yukarıdaki komut sadece bu python çalıştırması için geçerlidir.



# 4) KODDA ORTAM DEĞİŞKENİ KULLANMA – GERÇEK HAYAT ÖRNEĞİ

def connect_to_database():
    """
    Bu fonksiyon sanki bir veri tabanına bağlanıyormuş gibi yapıyor.
    Gerçekte DB_URL dışarıdan (environment'tan) okunur.
    """

    DB_URL = os.getenv("DB_URL", "postgresql://localhost:5432/defaultdb")

    print(f"Bağlantı kuruluyor → {DB_URL}")
    return f"Database connected at {DB_URL}"


def app_config():
    """
    Uygulamanın environment üzerinden nasıl yapılandırıldığını gösteren örnek.
    """

    print("Uygulama Ayarları:")
    print(f"- App Name: {APP_NAME}")
    print(f"- Debug Mode (str): {DEBUG_MODE}")
    print(f"- Debug Mode (bool): {DEBUG_MODE_BOOL}")
    print(f"- Max Connections: {MAX_CONNECTIONS_INT}")


# 5) ENVIRONMENT DEĞİŞKENİNİN PYTHON DIŞINDA NASIL TANIMLANACAĞI

"""
Terminalde çalıştırma örnekleri:

export APP_NAME="FastAPIApp"
export DEBUG_MODE="true"
export MAX_CONNECTIONS="50"
export DB_URL="postgresql://localhost:5432/proddb"

Sonra:
python main.py
"""
