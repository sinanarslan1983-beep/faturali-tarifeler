import json
from datetime import datetime

# GARANTİ FATURALI LİSTE - 42 ADET - SADECE FATURALI, FATURASIZ YOK
tarifeler = [
  {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "Red 10GB", "fiyat": 440, "fiyat_mnt": 396, "fiyat_yeni_hat": 374, "internet": "10GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "0dk", "populer": True, "avantajlar": ["5G Uyumlu", "【entity-Vodafone¦canonical_name=Vodafone】 TV"], "taahhut": 12},
  {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "Red 15GB", "fiyat": 465, "fiyat_mnt": 419, "fiyat_yeni_hat": 395, "internet": "15GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "0dk", "populer": False, "avantajlar": ["5G"], "taahhut": 12},
  {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "Red 20GB", "fiyat": 520, "fiyat_mnt": 468, "fiyat_yeni_hat": 442, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "50dk", "populer": False, "avantajlar": ["Yurtdışı 50dk"], "taahhut": 12},
  {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "Red 25GB", "fiyat": 545, "fiyat_mnt": 491, "fiyat_yeni_hat": 463, "internet": "25GB", "dk": "1000", "sms": "500", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["Yurtdışı 100dk"], "taahhut": 12},
  {"operator": "Vodafone", "isim": "Red 30GB 5G", "fiyat": 590, "fiyat_mnt": 531, "fiyat_yeni_hat": 502, "internet": "30GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["5G Ultra", "TV 3 ay"], "taahhut": 12},
  {"operator": "Vodafone", "isim": "Red 60GB 5G", "fiyat": 745, "fiyat_mnt": 671, "fiyat_yeni_hat": 633, "internet": "60GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "Sınırsız", "populer": True, "avantajlar": ["Yurtdışı Sınırsız"], "taahhut": 12},
  {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "FreeZone 15GB Genç", "fiyat": 380, "fiyat_mnt": 342, "fiyat_yeni_hat": 323, "internet": "15GB", "dk": "1000", "sms": "1000", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "0dk", "populer": True, "avantajlar": ["TikTok Sınırsız"], "taahhut": 12},
  {"operator": "Vodafone", "isim": "FreeZone 20GB Genç", "fiyat": 420, "fiyat_mnt": 378, "fiyat_yeni_hat": 357, "internet": "20GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "50dk", "populer": True, "avantajlar": ["TikTok", "YouTube Sınırsız"], "taahhut": 12},
  {"operator": "Vodafone", "isim": "Red 30GB Yurtdışı 300dk", "fiyat": 720, "fiyat_mnt": 648, "fiyat_yeni_hat": 612, "internet": "30GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Herkes", "kategori": "Yurtdışı", "yurtdisi": "300dk", "populer": True, "avantajlar": ["Yurtdışı 300dk"], "taahhut": 12},
  {"operator": "Vodafone", "isim": "Kolay 8GB 50+", "fiyat": 320, "fiyat_mnt": 288, "fiyat_yeni_hat": 272, "internet": "8GB", "dk": "500", "sms": "250", "yas_grubu": "50+", "kategori": "65+", "yurtdisi": "0dk", "populer": False, "avantajlar": ["50+ avantaj"], "taahhut": 12},
  {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "Star+ 5GB", "fiyat": 550, "fiyat_mnt": 495, "fiyat_yeni_hat": 468, "internet": "5GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "0dk", "populer": False, "avantajlar": ["TV+"], "taahhut": 12},
  {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "Star+ 10GB", "fiyat": 650, "fiyat_mnt": 585, "fiyat_yeni_hat": 553, "internet": "10GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "50dk", "populer": False, "avantajlar": ["TV+", "Fizy"], "taahhut": 12},
  {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "Star+ 20GB", "fiyat": 900, "fiyat_mnt": 810, "fiyat_yeni_hat": 765, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["TV+", "Fizy"], "taahhut": 12},
  {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "Star+ 30GB", "fiyat": 1100, "fiyat_mnt": 990, "fiyat_yeni_hat": 935, "internet": "30GB", "dk": "2000", "sms": "500", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "200dk", "populer": False, "avantajlar": ["TV+"], "taahhut": 12},
  {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "GNÇ Avantaj 5+5GB", "fiyat": 280, "fiyat_mnt": 252, "fiyat_yeni_hat": 238, "internet": "10GB", "dk": "1000", "sms": "250", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "0dk", "populer": True, "avantajlar": ["GNÇ"], "taahhut": 12},
  {"operator": "Turkcell", "isim": "GNÇ Avantaj 10+10GB", "fiyat": 320, "fiyat_mnt": 288, "fiyat_yeni_hat": 272, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "0dk", "populer": True, "avantajlar": ["Instagram sınırsız"], "taahhut": 12},
  {"operator": "Turkcell", "isim": "GNÇ Avantaj 20+20GB", "fiyat": 450, "fiyat_mnt": 405, "fiyat_yeni_hat": 383, "internet": "40GB", "dk": "1000", "sms": "250", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "50dk", "populer": True, "avantajlar": ["YouTube Sınırsız"], "taahhut": 12},
  {"operator": "Turkcell", "isim": "Avantaj+ 20GB 3000DK", "fiyat": 400, "fiyat_mnt": 360, "fiyat_yeni_hat": 340, "internet": "20GB", "dk": "3000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["Bol dakika"], "taahhut": 12},
  {"operator": "Turkcell", "isim": "Dev Star 120GB Yıllık", "fiyat": 520, "fiyat_mnt": 468, "fiyat_yeni_hat": 442, "internet": "120GB", "dk": "12000", "sms": "6000", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "500dk", "populer": True, "avantajlar": ["Yıllık avantaj"], "taahhut": 24},
  {"operator": "【entity-Türk Telekom¦canonical_name=Turkcell】", "isim": "Prime 10GB", "fiyat": 265, "fiyat_mnt": 239, "fiyat_yeni_hat": 225, "internet": "10GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "0dk", "populer": True, "avantajlar": ["Prime"], "taahhut": 12},
  {"operator": "【entity-Türk Telekom¦canonical_name=Turkcell】", "isim": "Prime 20GB", "fiyat": 360, "fiyat_mnt": 324, "fiyat_yeni_hat": 306, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["Prime"], "taahhut": 12},
  {"operator": "Türk Telekom", "isim": "Prime 30GB", "fiyat": 450, "fiyat_mnt": 405, "fiyat_yeni_hat": 383, "internet": "30GB", "dk": "2000", "sms": "500", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["E-dergi"], "taahhut": 12},
  {"operator": "Türk Telekom", "isim": "Emekli 10GB", "fiyat": 195, "fiyat_mnt": 176, "fiyat_yeni_hat": 166, "internet": "10GB", "dk": "1000", "sms": "250", "yas_grubu": "50+", "kategori": "65+", "yurtdisi": "0dk", "populer": True, "avantajlar": ["Emekli"], "taahhut": 12},
  {"operator": "Türk Telekom", "isim": "Selfy 15GB Genç", "fiyat": 275, "fiyat_mnt": 248, "fiyat_yeni_hat": 234, "internet": "15GB", "dk": "1000", "sms": "500", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "50dk", "populer": True, "avantajlar": ["Selfy"], "taahhut": 12},
  {"operator": "Türk Telekom", "isim": "Selfy 25GB TikTok", "fiyat": 365, "fiyat_mnt": 329, "fiyat_yeni_hat": 310, "internet": "25GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "100dk", "populer": False, "avantajlar": ["TikTok sınırsız"], "taahhut": 12},
  {"operator": "Türk Telekom", "isim": "Prime Yurtdışı 30GB 400dk", "fiyat": 650, "fiyat_mnt": 585, "fiyat_yeni_hat": 553, "internet": "30GB", "dk": "2000", "sms": "500", "yas_grubu": "Herkes", "kategori": "Yurtdışı", "yurtdisi": "400dk", "populer": True, "avantajlar": ["Yurtdışı 400dk"], "taahhut": 12},
]

data = {
    "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "toplam_tarife": len(tarifeler),
    "tarifeler": tarifeler
}

with open("tarifeler.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK - {len(tarifeler)} faturalı tarife yazıldı - SADECE FATURALI")
