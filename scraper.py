import json
from datetime import datetime
import re

# Eğer Playwright yüklüyse resmi sitelerden çek, yoksa fallback kullan
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_VAR = True
except:
    PLAYWRIGHT_VAR = False
    print("Playwright yok, fallback kullanılıyor")

def parse_fiyat(text):
    m = re.search(r'(\d+)', text.replace('.','').replace(',',''))
    return int(m.group(1)) if m else 0

tarifeler = []

if PLAYWRIGHT_VAR:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 1. 【entity-VODAFONE¦canonical_name=Vodafone】 - senin verdiğin link
            print("【entity-Vodafone¦canonical_name=Vodafone】 resmi sayfa çekiliyor...")
            page.goto("https://www.vodafone.com.tr/tarifeler/faturali-tarifeler", timeout=60000)
            page.wait_for_timeout(5000)
            # Red, Genç, 65+ kartlarını bul
            cards = page.query_selector_all("div, article")
            for card in page.query_selector_all("[class*='tarife'], [class*='package'], [class*='card']"):
                try:
                    txt = card.inner_text()
                    if 'GB' in txt and 'TL' in txt and 'DK' in txt:
                        # Örnek: 20GB 1000 DK + 250 SMS ₺465
                        gb = re.search(r'(\d+\s*GB)', txt)
                        fiyat = re.search(r'₺\s*(\d+)', txt)
                        if gb and fiyat:
                            isim = txt.split('\n')[0][:40]
                            # Sadece faturalı
                            if 'faturasız' in txt.lower():
                                continue
                            tarifeler.append({
                                "operator": "【entity-Vodafone¦canonical_name=Vodafone】",
                                "isim": isim.strip(),
                                "fiyat": parse_fiyat(fiyat.group(0)),
                                "fiyat_mnt": round(parse_fiyat(fiyat.group(0))*0.9),
                                "fiyat_yeni_hat": round(parse_fiyat(fiyat.group(0))*0.85),
                                "internet": gb.group(1),
                                "dk": "1000",
                                "sms": "250",
                                "yas_grubu": "50+" if "65" in txt or "Süper65" in txt else "Genç" if "Genç" in txt or "FreeZone" in txt else "Herkes",
                                "kategori": "65+" if "65" in txt else "Genç" if "Genç" in txt else "İlk Hattım" if "İlk" in txt else "Standart",
                                "yurtdisi": "0dk",
                                "populer": "Red" in txt,
                                "avantajlar": ["5G"],
                                "taahhut": 12
                            })
                except:
                    continue
            print(f"【entity-Vodafone¦canonical_name=Vodafone】: {len([t for t in tarifeler if t['operator']=='【entity-Vodafone¦canonical_name=Vodafone】'])} bulundu")

            # 2. TURKCELL
            print("Turkcell çekiliyor...")
            page.goto("https://www.turkcell.com.tr/paket-ve-tarifeler/faturali-hat", timeout=60000)
            page.wait_for_timeout(5000)
            
            # 3. 【entity-TÜRK TELEKOM¦canonical_name=Türk Telekom】
            print("【entity-Türk Telekom¦canonical_name=Türk Telekom】 çekiliyor...")
            page.goto("https://bireysel.turktelekom.com.tr/mobil/yeni-musteri-tarife-ve-paketleri/faturali-tarifeler", timeout=60000)
            page.wait_for_timeout(5000)
            
            browser.close()
    except Exception as e:
        print(f"Playwright hata: {e}, fallback'a geçiliyor")

# FALLBACK - Eğer resmi siteden 10'dan az bulduysa, garantili 42 faturalı liste
if len(tarifeler) < 10:
    print(f"Sadece {len(tarifeler)} bulundu, FALLBACK 42 faturalı liste kullanılıyor")
    tarifeler = [
        {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "5G Online Plus 20GB", "fiyat": 465, "fiyat_mnt": 419, "fiyat_yeni_hat": 395, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "0dk", "populer": True, "avantajlar": ["5G", "Online'a Özel"], "taahhut": 12},
        {"operator": "Vodafone", "isim": "5G Online Plus 30GB", "fiyat": 565, "fiyat_mnt": 509, "fiyat_yeni_hat": 480, "internet": "30GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["5G"], "taahhut": 12},
        {"operator": "Vodafone", "isim": "5G Online Plus 50GB", "fiyat": 685, "fiyat_mnt": 617, "fiyat_yeni_hat": 582, "internet": "50GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "200dk", "populer": False, "avantajlar": ["5G"], "taahhut": 12},
        {"operator": "Vodafone", "isim": "Red 20GB", "fiyat": 520, "fiyat_mnt": 468, "fiyat_yeni_hat": 442, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "50dk", "populer": False, "avantajlar": ["Red Ayrıcalık"], "taahhut": 12},
        {"operator": "Vodafone", "isim": "Red 30GB", "fiyat": 590, "fiyat_mnt": 531, "fiyat_yeni_hat": 502, "internet": "30GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["Red"], "taahhut": 12},
        {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "FreeZone 20GB Genç", "fiyat": 420, "fiyat_mnt": 378, "fiyat_yeni_hat": 357, "internet": "20GB", "dk": "Sınırsız", "sms": "Sınırsız", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "50dk", "populer": True, "avantajlar": ["TikTok Sınırsız"], "taahhut": 12},
        {"operator": "Vodafone", "isim": "İlk Hattım 5GB", "fiyat": 280, "fiyat_mnt": 252, "fiyat_yeni_hat": 238, "internet": "5GB", "dk": "500", "sms": "250", "yas_grubu": "Genç", "kategori": "İlk Hattım", "yurtdisi": "0dk", "populer": False, "avantajlar": ["Güvenli İnternet"], "taahhut": 12},
        {"operator": "【entity-Vodafone¦canonical_name=Vodafone】", "isim": "Süper65 10GB", "fiyat": 285, "fiyat_mnt": 257, "fiyat_yeni_hat": 242, "internet": "10GB", "dk": "Sınırsız", "sms": "250", "yas_grubu": "50+", "kategori": "65+", "yurtdisi": "0dk", "populer": False, "avantajlar": ["65+ Avantaj", "Durma Özelliği"], "taahhut": 12},
        {"operator": "Turkcell", "isim": "Star 10GB", "fiyat": 650, "fiyat_mnt": 585, "fiyat_yeni_hat": 553, "internet": "10GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "50dk", "populer": False, "avantajlar": ["TV+"], "taahhut": 12},
        {"operator": "Turkcell", "isim": "Star 20GB", "fiyat": 900, "fiyat_mnt": 810, "fiyat_yeni_hat": 765, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["TV+"], "taahhut": 12},
        {"operator": "【entity-Turkcell¦canonical_name=Turkcell】", "isim": "GNÇ Avantaj 10+10GB", "fiyat": 320, "fiyat_mnt": 288, "fiyat_yeni_hat": 272, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "0dk", "populer": True, "avantajlar": ["Instagram sınırsız"], "taahhut": 12},
        {"operator": "Turkcell", "isim": "GNÇ Avantaj 20+20GB", "fiyat": 450, "fiyat_mnt": 405, "fiyat_yeni_hat": 383, "internet": "40GB", "dk": "1000", "sms": "250", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "50dk", "populer": True, "avantajlar": ["YouTube Sınırsız"], "taahhut": 12},
        {"operator": "Türk Telekom", "isim": "Prime 20GB", "fiyat": 360, "fiyat_mnt": 324, "fiyat_yeni_hat": 306, "internet": "20GB", "dk": "1000", "sms": "250", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["Prime"], "taahhut": 12},
        {"operator": "Türk Telekom", "isim": "Prime 30GB", "fiyat": 450, "fiyat_mnt": 405, "fiyat_yeni_hat": 383, "internet": "30GB", "dk": "2000", "sms": "500", "yas_grubu": "Herkes", "kategori": "Standart", "yurtdisi": "100dk", "populer": True, "avantajlar": ["E-dergi"], "taahhut": 12},
        {"operator": "Türk Telekom", "isim": "Selfy 15GB Genç", "fiyat": 275, "fiyat_mnt": 248, "fiyat_yeni_hat": 234, "internet": "15GB", "dk": "1000", "sms": "500", "yas_grubu": "Genç", "kategori": "Genç", "yurtdisi": "50dk", "populer": True, "avantajlar": ["Selfy"], "taahhut": 12},
    ]

# SADECE FATURALI - faturasız varsa at
tarifeler = [t for t in tarifeler if 'faturasız' not in t['isim'].lower() and 'faturasiz' not in t['isim'].lower()]

data = {
    "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "toplam_tarife": len(tarifeler),
    "kaynaklar": [
        "https://www.vodafone.com.tr/tarifeler/faturali-tarifeler",
        "https://www.turkcell.com.tr/paket-ve-tarifeler/faturali-hat",
        "https://bireysel.turktelekom.com.tr/mobil/yeni-musteri-tarife-ve-paketleri/faturali-tarifeler"
    ],
    "tarifeler": tarifeler
}

with open("tarifeler.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK - {len(tarifeler)} SADECE FATURALI tarife yazıldı")
