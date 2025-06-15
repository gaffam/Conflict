import feedparser
import json
from time import sleep
from datetime import datetime, timedelta

# --- AYARLAR BOLUMU ---
RSS_DOSYASI = 'rss_kaynaklari.txt'
# GeoJSON formatinda [Boylam, Enlem]
LOKASYONLAR = {
    "Jerusalem": {"coords": [35.2137, 31.7683], "country": "Israel"},
    "Tel Aviv": {"coords": [34.7818, 32.0853], "country": "Israel"},
    "Gaza": {"coords": [34.4667, 31.5], "country": "Palestine"},
    "Ashkelon": {"coords": [34.5714, 31.6693], "country": "Israel"},
    "Sderot": {"coords": [34.5944, 31.525], "country": "Israel"},
    "Haifa": {"coords": [34.9896, 32.794], "country": "Israel"},
    "West Bank": {"coords": [35.26, 31.95], "country": "Palestine"},
    "Iran": {"coords": [53.6880, 32.4279], "country": "Iran"},
    "Syria": {"coords": [38.9968, 34.8021], "country": "Syria"},
    "Lebanon": {"coords": [35.8623, 33.8547], "country": "Lebanon"},
}

# Son 24 saatteki haberleri dikkate almak icin zaman penceresi
ZAMAN_PENCERESI = timedelta(hours=24)

# Onemli anahtar kelimeler ve agirlik seviyesi
ANAHTAR_KELIMELER = {
    "missile": "high",
    "rocket": "high",
    "attack": "high",
    "drone": "medium",
}
DEFAULT_SEVERITY = "info"



def rss_kaynaklarini_oku():
    """rss_kaynaklari.txt dosyasindan URL'leri okur ve bir liste olarak dondurur."""
    try:
        with open(RSS_DOSYASI, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"{len(urls)} adet RSS kaynagi dosyadan okundu.")
        return urls
    except FileNotFoundError:
        print(f"HATA: '{RSS_DOSYASI}' adinda bir dosya bulunamadi. Lutfen olusturun.")
        return []

def verileri_cek_ve_isle():
    RSS_URLS = rss_kaynaklarini_oku()
    if not RSS_URLS:
        print("Islenecek RSS kaynagi yok. Script duraklatiliyor.")
        return

    print(f"[{datetime.now()}] RSS kaynaklari taraniyor...")
    bulunan_haberler = []
    gorulen_linkler = set()

    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                try:
                    title = getattr(entry, 'title', '')
                    summary = getattr(entry, 'summary', '')
                    haber_metni = (title + " " + summary).lower()
                    haber_linki = getattr(entry, 'link', '')
                    if not haber_linki:
                        continue

                    yayim_zamani = getattr(entry, 'published_parsed', None)
                    if yayim_zamani:
                        entry_dt = datetime(*yayim_zamani[:6])
                    else:
                        entry_dt = datetime.utcnow()
                    if datetime.utcnow() - entry_dt > ZAMAN_PENCERESI:
                        continue

                    if haber_linki in gorulen_linkler:
                        continue

                    for lokasyon, bil in LOKASYONLAR.items():
                        if lokasyon.lower() in haber_metni:
                            seviye = DEFAULT_SEVERITY
                            for kelime, sv in ANAHTAR_KELIMELER.items():
                                if kelime in haber_metni:
                                    seviye = sv
                                    break
                            haber_objesi = {
                                "baslik": title,
                                "link": haber_linki,
                                "tarih": entry.get("published", "Tarih bulunamadi"),
                                "kaynak": getattr(feed.feed, 'title', url),
                                "lokasyon_adi": lokasyon,
                                "koordinatlar": bil["coords"],
                                "country": bil["country"],
                                "severity": seviye,
                            }
                            bulunan_haberler.append(haber_objesi)
                            gorulen_linkler.add(haber_linki)
                            break
                except Exception as e:
                    print(f"Hata: entry islenemedi - {e}")
        except Exception as e:
            print(f"Hata: {url} okunurken sorun olustu - {e}")

    geojson_olustur(bulunan_haberler)


def geojson_olustur(haber_listesi):
    print(f"{len(haber_listesi)} adet konumla iliskili haber bulundu.")
    features = []
    for haber in haber_listesi:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": haber["koordinatlar"],
            },
            "properties": {
                "baslik": haber["baslik"],
                "link": haber["link"],
                "tarih": haber["tarih"],
                "kaynak": haber["kaynak"],
                "lokasyon": haber["lokasyon_adi"],
                "country": haber["country"],
                "severity": haber["severity"],
            },
        }
        features.append(feature)

    geojson_yapisi = {"type": "FeatureCollection", "features": features}

    with open("data.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson_yapisi, f, ensure_ascii=False, indent=4)
    print("data.geojson dosyasi basariyla guncellendi.")


if __name__ == "__main__":
    while True:
        verileri_cek_ve_isle()
        sleep(900)
