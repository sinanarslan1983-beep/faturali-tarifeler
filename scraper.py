import json
from datetime import datetime
tarifeler = [
  {"operator": "Vodafone", "isim": "Red 20GB", "fiyat": 385, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes"},
  {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "FreeZone 20GB Genç", "fiyat": 350, "internet": "20GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Genç"},
  {"operator": "Vodafone", "isim": "Red 30GB 5G", "fiyat": 450, "internet": "30GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Herkes"},
  {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "GNÇ 25GB", "fiyat": 325, "internet": "25GB", "dk": "1000", "sms": "1000", "yas_grubu": "Genç"},
  {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "Süper 25GB", "fiyat": 410, "internet": "25GB", "dk": "1000", "sms": "500", "yas_grubu": "Herkes"},
  {"operator": "Turk Telekom", "isim": "Prime Emekli 15GB", "fiyat": 280, "internet": "15GB", "dk": "1000", "sms": "250", "yas_grubu": "50+"},
  {"operator": "Turk Telekom", "isim": "Prime 20GB", "fiyat": 360, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes"}
]
data = {"guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"), "tarifeler": tarifeler}
with open("tarifeler.json", "w", encoding="utf-8") as f:
  json.dump(data, f, ensure_ascii=False, indent=2)
print("OK - 7 tarife")
