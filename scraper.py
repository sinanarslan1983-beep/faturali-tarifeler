import json
from datetime import datetime
tarifeler = [
  {"operator": "Vodafone", "isim": "Red 20GB", "fiyat": 385, "internet": "20GB", "dk": "1000", "sms": "250"},
  {"operator": "Vodafone", "isim": "Red 30GB 5G", "fiyat": 450, "internet": "30GB", "dk": "Sinirsiz", "sms": "Sinirsiz"},
  {"operator": "Turkcell", "isim": "Super 25GB", "fiyat": 410, "internet": "25GB", "dk": "1000", "sms": "500"},
  {"operator": "Turk Telekom", "isim": "Prime 20GB", "fiyat": 360, "internet": "20GB", "dk": "1000", "sms": "250"}
]
data = {"guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"), "tarifeler": tarifeler}
with open("tarifeler.json", "w", encoding="utf-8") as f:
  json.dump(data, f, ensure_ascii=False, indent=2)
print("OK")
