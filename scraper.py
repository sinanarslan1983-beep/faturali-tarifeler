import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def temizle(text):
    return re.sub(r'\s+', ' ', text).strip()

def fiyati_al(text):
    m = re.search(r'(\d+)', text.replace('.', ''))
    return int(m.group(1)) if m else 0

def kategori_bul(isim):
    isim_low = isim.lower()
    if '65' in isim_low or 'emekli' in isim_low or '50+' in isim_low:
        return '65+'
    if 'ilk' in isim_low:
        return 'İlk Hattım'
    if 'esnaf' in isim_low:
        return 'Esnaf'
    if 'gnç' in isim_low or 'freezone' in isim_low or 'selfy' in isim_low or 'genç' in isim_low:
        return 'Genç'
    if 'yurtdışı' in isim_low or 'yurtdisi' in isim_low:
        return 'Yurtdışı'
    return 'Standart'

def yas_grubu_bul(isim, kategori):
    if kategori == '65+':
        return '50+'
    if kategori == 'Genç' or kategori == 'İlk Hattım':
        return 'Genç'
    return 'Herkes'

OPERATOR_URLS = {
    "【entity-Vodafone¦canonical_name=Vodafone】": "https://www.ceptetarife.com/tarifeler/vodafone",
    "【entity-Turkcell¦canonical_name=Turkcell】": "https://www.ceptetarife.com/tarifeler/turkcell",
    "【entity-Türk Telekom¦canonical_name=Türk Telekom】": "https://www.ceptetarife.com/tarifeler/turk-telekom"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

tum_tarifeler = []

for operator, url in OPERATOR_URLS.items():
    try:
        print(f"{operator} çekiliyor: {url}")
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'lxml')
        rows = soup.select('table tr')
        count = 0
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue
            isim = temizle(cols[0].get_text())
            internet = temizle(cols[1].get_text())
            dk = temizle(cols[2].get_text())
            sms = temizle(cols[3].get_text())
            fiyat_text = temizle(cols[4].get_text())
            fiyat = fiyati_al(fiyat_text)
            if fiyat < 50 or 'faturasız' in isim.lower():
                continue
            if 'faturalı' not in isim.lower() and 'faturalı' not in fiyat_text.lower():
                # faturalı olmayanları atlama, ama faturasız yazanı atla
                if 'faturasız' in isim.lower():
                    continue
            
            kategori = kategori_bul(isim)
            yas = yas_grubu_bul(isim, kategori)
            yurtdisi = "0dk"
            if 'yurtdışı' in isim.lower() or 'yurtdisi' in isim.lower():
                m = re.search(r'(\d+)\s*dk', isim.lower())
                yurtdisi = f"{m.group(1)}dk" if m else "100dk"
            
            populer = False
            if fiyat < 350 or 'avantaj' in isim.lower() or '20' in internet:
                populer = True
            
            tarife = {
                "operator": operator,
                "isim": isim.replace(' Faturalı','').replace('  ',' ').strip()[:40],
                "fiyat": fiyat,
                "fiyat_mnt": round(fiyat*0.9),
                "fiyat_yeni_hat": round(fiyat*0.85),
                "internet": internet,
                "dk": dk,
                "sms": sms,
                "yas_grubu": yas,
                "kategori": kategori,
                "yurtdisi": yurtdisi,
                "populer": populer,
                "avantajlar": ["5G Uyumlu"] if '5G' in isim else ["TV+" if operator=="Turkcell" else "Vodafone TV" if operator=="Vodafone" else "Prime"],
                "taahhut": 12
            }
            tum_tarifeler.append(tarife)
            count += 1
        print(f"{operator}: {count} tarife bulundu")
    except Exception as e:
        print(f"{operator} hata: {e}")

# Eğer 10'dan az bulduysa ESKİ dosyayı koru, üstüne yazma
if len(tum_tarifeler) < 10:
    print(f"SADECE {len(tum_tarifeler)} tarife bulundu, ESKİ dosya korunuyor!")
    try:
        with open("tarifeler.json", "r", encoding="utf-8") as f:
            old = json.load(f)
            if len(old.get('tarifeler', [])) > 10:
                print("Eski dosya korunuyor, çıkılıyor")
                exit(0)
    except:
        pass
    # Fallback 62 tarifelik liste
    print("Fallback liste kullanılıyor")

# Fallback'i buraya ekle (senin 62'lik listen) eğer scraping az bulduysa
if len(tum_tarifeler) < 20:
    # senin hazırladığın 62'lik tam listeyi buraya gömüyoruz (kısa tutuldu, gerçekte 62 olacak)
    fallback = [
        {"operator": "Vodafone", "isim": "Red 20GB", "fiyat": 520, "fiyat_mnt": 468, "fiyat_yeni_hat": 442, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "50dk", "populer": True, "avantajlar": ["5G"], "taahhut": 12},
        {"operator": "Turkcell", "isim": "GNÇ Avantaj 10+10GB", "fiyat": 320, "fiyat_mnt": 288, "fiyat_yeni_hat": 272, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "0dk", "populer": True, "avantajlar": ["【entity-Instagram¦canonical_name=Instagram】 sınırsız"], "taahhut": 12},
        {"operator": "【entity-Türk Telekom¦canonical_name=Türk Telekom】", "isim": "Prime 20GB", "fiyat": 360, "fiyat_mnt": 324, "fiyat_yeni_hat": 306, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["Prime"], "taahhut": 12},
    ]
    # Gerçekte buraya 62 tarifeyi koy, şimdilik 3 örnek
    if len(tum_tarifeler) == 0:
        tum_tarifeler = fallback

data = {
    "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "toplam_tarife": len(tum_tarifeler),
    "tarifeler": tum_tarifeler
}

with open("tarifeler.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK - {len(tum_tarifeler)} tarife yazıldı")
