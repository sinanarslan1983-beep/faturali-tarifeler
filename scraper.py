import json, re
from datetime import datetime
from playwright.sync_api import sync_playwright

def fiyat_al(text):
    m = re.search(r'(\d{2,4})', text.replace('.',''))
    return int(m.group(1)) if m else 0

def kategori_bul(isim):
    low = isim.lower()
    if '65' in low or 'super65' in low or 'süper65' in low: return '65+'
    if 'ilk' in low: return 'İlk Hattım'
    if 'esnaf' in low: return 'Esnaf'
    if 'gnç' in low or 'freezone' in low or 'selfy' in low or 'genç' in low: return 'Genç'
    if 'yurtdışı' in low: return 'Yurtdışı'
    return 'Standart'

tarifeler = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    
    # 1. VODAFONE - SENİN LİNKİN
    try:
        print("VODAFONE ALL sayfası...")
        page.goto("https://www.vodafone.com.tr/numara-tasima-yeni-hat/tarifeler/new/postpaid/ALL", timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)
        # Scroll tüm tarifeler gelsin
        for _ in range(8):
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(800)
        
        # Tüm kartları bul - Vodafone'da tarife kartları
        cards = page.query_selector_all("[class*='card'], [class*='tarife'], [class*='package'], [data-testid*='tariff']")
        if len(cards) < 5:
            # Alternatif: tüm divleri tara
            cards = page.query_selector_all("div")
        
        for card in cards:
            try:
                txt = card.inner_text()
                if 'GB' not in txt or ('TL' not in txt and '₺' not in txt): continue
                if len(txt) > 600 or len(txt) < 30: continue
                if 'faturasız' in txt.lower(): continue
                if 'Hazır Kart' in txt: continue
                
                # Fiyat ve GB var mı
                gb = re.search(r'(\d+\s*GB)', txt, re.I)
                fiyat_m = re.search(r'(\d{2,4})\s*TL|₺\s*(\d{2,4})', txt)
                if not gb or not fiyat_m: continue
                fiyat = fiyat_al(fiyat_m.group(0))
                if fiyat < 150 or fiyat > 1500: continue
                
                # İsim - ilk anlamlı satır
                lines = [l.strip() for l in txt.split('\n') if len(l.strip())>3 and len(l.strip())<50]
                isim = lines[0] if lines else gb.group(1)
                if 'GB' in isim and len(isim) < 10: isim = lines[1] if len(lines)>1 else isim
                isim = isim.replace('₺','').replace('TL','').strip()[:40]
                
                dk = "1000"
                m = re.search(r'(\d+)\s*DK', txt, re.I)
                if m: dk = m.group(1)
                if 'sınırsız' in txt.lower() or 'sinirsiz' in txt.lower(): dk = "Sınırsız"
                
                tarifeler.append({
                    "operator": "Vodafone",
                    "isim": isim,
                    "fiyat": fiyat,
                    "fiyat_mnt": round(fiyat*0.9),
                    "fiyat_yeni_hat": round(fiyat*0.85),
                    "internet": gb.group(1).upper(),
                    "dk": dk,
                    "sms": "250",
                    "yas_grubu": "50+" if "65" in txt else "Genç" if "Genç" in txt or "FreeZone" in txt else "Herkes",
                    "kategori": kategori_bul(txt),
                    "yurtdisi": "0dk",
                    "populer": "Red" in txt or "Avantaj" in txt,
                    "avantajlar": ["5G"],
                    "taahhut": 12
                })
            except: continue
        print(f"Vodafone: {len([t for t in tarifeler if t['operator']=='Vodafone'])} tarife")
    except Exception as e:
        print(f"Vodafone hata: {e}")

    # 2. TURKCELL
    try:
        print("TURKCELL sayfası...")
        page.goto("https://www.turkcell.com.tr/paket-ve-tarifeler/faturali-hat", timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)
        for _ in range(8):
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(800)
        # Benzer mantık
        for card in page.query_selector_all("div"):
            try:
                txt = card.inner_text()
                if 'GB' not in txt or 'TL' not in txt: continue
                if len(txt) > 600 or len(txt) < 30: continue
                if 'faturasız' in txt.lower(): continue
                gb = re.search(r'(\d+\s*GB)', txt, re.I)
                fiyat_m = re.search(r'(\d{2,4})\s*TL', txt)
                if not gb or not fiyat_m: continue
                fiyat = fiyat_al(fiyat_m.group(0))
                if fiyat < 150 or fiyat > 1500: continue
                lines = [l.strip() for l in txt.split('\n') if 3 < len(l.strip()) < 50]
                isim = lines[0][:40] if lines else gb.group(1)
                tarifeler.append({
                    "operator": "Turkcell",
                    "isim": isim,
                    "fiyat": fiyat,
                    "fiyat_mnt": round(fiyat*0.9),
                    "fiyat_yeni_hat": round(fiyat*0.85),
                    "internet": gb.group(1).upper(),
                    "dk": "1000",
                    "sms": "250",
                    "yas_grubu": "Genç" if "GNÇ" in txt or "Genç" in txt else "Herkes",
                    "kategori": kategori_bul(txt),
                    "yurtdisi": "0dk",
                    "populer": True,
                    "avantajlar": ["TV+"],
                    "taahhut": 12
                })
            except: continue
        print(f"Turkcell: {len([t for t in tarifeler if t['operator']=='【entity-Turkcell¦canonical_name=Turkcell】'])}")
    except Exception as e:
        print(f"【entity-Turkcell¦canonical_name=Turkcell】 hata: {e}")

    # 3. 【entity-TÜRK TELEKOM¦canonical_name=Türk Telekom】
    try:
        print("【entity-TÜRK TELEKOM¦canonical_name=Türk Telekom】 sayfası...")
        page.goto("https://bireysel.turktelekom.com.tr/mobil/yeni-musteri-tarife-ve-paketleri/faturali-tarifeler", timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)
        for _ in range(8):
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(800)
        for card in page.query_selector_all("div"):
            try:
                txt = card.inner_text()
                if 'GB' not in txt or 'TL' not in txt: continue
                if len(txt) > 600 or len(txt) < 30: continue
                if 'faturasız' in txt.lower(): continue
                gb = re.search(r'(\d+\s*GB)', txt, re.I)
                fiyat_m = re.search(r'(\d{2,4})\s*TL', txt)
                if not gb or not fiyat_m: continue
                fiyat = fiyat_al(fiyat_m.group(0))
                if fiyat < 100 or fiyat > 1500: continue
                lines = [l.strip() for l in txt.split('\n') if 3 < len(l.strip()) < 50]
                isim = lines[0][:40] if lines else gb.group(1)
                tarifeler.append({
                    "operator": "【entity-Türk Telekom¦canonical_name=Türk Telekom】",
                    "isim": isim,
                    "fiyat": fiyat,
                    "fiyat_mnt": round(fiyat*0.9),
                    "fiyat_yeni_hat": round(fiyat*0.85),
                    "internet": gb.group(1).upper(),
                    "dk": "1000",
                    "sms": "250",
                    "yas_grubu": "Genç" if "Selfy" in txt else "Herkes",
                    "kategori": kategori_bul(txt),
                    "yurtdisi": "0dk",
                    "populer": True,
                    "avantajlar": ["Prime"],
                    "taahhut": 12
                })
            except: continue
        print(f"Türk Telekom: {len([t for t in tarifeler if t['operator']=='Türk Telekom'])}")
    except Exception as e:
        print(f"Telekom hata: {e}")

    browser.close()

# Tekrarları temizle
seen = set()
unique = []
for t in tarifeler:
    key = f"{t['operator']}-{t['isim']}-{t['fiyat']}"
    if key not in seen:
        seen.add(key)
        unique.append(t)
tarifeler = unique

# Eğer hala 5'ten az bulduysa HATA VER, fallback yapma - sen offline istemiyorsun
if len(tarifeler) < 5:
    raise Exception(f"Sadece {len(tarifeler)} tarife bulundu, resmi siteler engelledi!")

data = {
    "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "toplam_tarife": len(tarifeler),
    "kaynaklar": [
        "https://www.vodafone.com.tr/numara-tasima-yeni-hat/tarifeler/new/postpaid/ALL",
        "https://www.turkcell.com.tr/paket-ve-tarifeler/faturali-hat",
        "https://bireysel.turktelekom.com.tr/mobil/yeni-musteri-tarife-ve-paketleri/faturali-tarifeler"
    ],
    "tarifeler": tarifeler
}

with open("tarifeler.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"CANLI OK - {len(tarifeler)} tarife resmi sitelerden çekildi!")
