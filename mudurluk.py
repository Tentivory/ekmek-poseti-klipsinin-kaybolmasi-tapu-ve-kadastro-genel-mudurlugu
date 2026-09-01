#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T.C. Tapu ve Kadastro Genel Müdürlüğü — Ekmek Poşeti Klips Kayıp Tescil Yazılımı
Sürüm: 1983/Kadastro-Revizyon-7

Bu yazılım bir ekmek poşetini parsel, klipsi mühür, açık ağızı ise
tecavüz sayar. Çalışır. Şaka değildir. Şakadır. Şaka değildir.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import random
import sys
from dataclasses import dataclass, field


KURUM = "T.C. TAPU VE KADASTRO GENEL MÜDÜRLÜĞÜ"
BIRIM = "Ekmek Poşeti Sınır ve Mühür Tescil Şubesi"
YONETMELIK = "Ekmek Poşeti Klipsinin Muhafazası ve Kaybına İlişkin Usul ve Esaslar Yönetmeliği (Resmî Gazete: hayalî / 01.09.2026)"


def tescil_no(metin: str) -> str:
    h = hashlib.sha1(metin.encode("utf-8")).hexdigest()[:10].upper()
    return f"TKGM-EKM-{h}"


@dataclass
class Parsel:
    sahibi: str
    ekmek_turu: str
    poşet_rengi: str
    klips_durumu: str = "mevcut-gibi-duruyor"
    notlar: list[str] = field(default_factory=list)

    def ada_parsel(self) -> str:
        # Ada: ekmek türü hash, parsel: renk hash. Ciddiyet için.
        ada = int(hashlib.md5(self.ekmek_turu.encode()).hexdigest()[:4], 16) % 900 + 100
        parsel = int(hashlib.md5(self.poşet_rengi.encode()).hexdigest()[:3], 16) % 90 + 10
        return f"Ada {ada} / Parsel {parsel}"


DURUMLAR = {
    "kayip": "KLİPS TAPUDA GÖRÜNMEMEKTEDİR — zilyetlik ihtilaflıdır",
    "cekmece": "KLİPS ÇEKMECEDE OLABİLİR — tapu kaydı şerhli",
    "buzdolabi": "KLİPS BUZDOLABI MAGNETİNE YAPISMIŞ — fiilî işgal",
    "cop": "KLİPS ÇÖPE GİTMİŞ OLABİLİR — tescil iptali talebi",
    "hic-yoktu": "KLİPS BAŞTAN YOKTU — fuzuli işgal ve hayali mühür",
}

KARARLAR = [
    "Poşet ağzı kapatılmadan muhafaza suçu işlenmiştir.",
    "Bayatlama riski milli gıda güvenliği kapsamındadır.",
    "Klipsin yokluğu sınır taşının yerinden oynamasına denktir.",
    "Zilyet, 'az önce buradaydı' beyanıyla tanık dinletmek zorundadır.",
    "Yedek klips kullanımı geçici tescil sayılır, asıl mühür aranır.",
    "Poşetin lastikle bağlanması kaçak yapıdır.",
]


def tutanak(parsel: Parsel, iddia: str) -> str:
    simdi = dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    no = tescil_no(parsel.sahibi + parsel.ekmek_turu + simdi)
    durum = DURUMLAR.get(iddia, DURUMLAR["kayip"])
    karar = random.choice(KARARLAR)
    cezai = random.choice(
        [
            "1 (bir) adet taze ekmek iadesi",
            "poşeti dürüstçe katlayıp çekmeceye koyma yükümlülüğü",
            "üç gün boyunca ekmeği tabağa koyarak yeme cezası",
            "klips muadili mandal temini",
            "komşuya ekmek ısıratma tazminatı",
        ]
    )
    metin = f"""
{'=' * 72}
{KURUM}
{BIRIM}
Dayanak: {YONETMELIK}
Tescil No: {no}
Tarih: {simdi}
{'=' * 72}

TAŞINMAZ           : Ekmek poşeti ({parsel.ekmek_turu})
ADA / PARSEL       : {parsel.ada_parsel()}
ZİLYET / MALİK     : {parsel.sahibi}
POŞET RENGİ        : {parsel.poşet_rengi}
MÜHÜR (KLİPS)      : {durum}

OLAY ÖZETİ
----------
Beyan sahibinin ifadesine göre mühür (klips) 'az önce buradaydı'.
Bu cümle Müdürlüğümüzce zilyetlik karinesi olarak işlenmiş,
ancak fiilî tespit yapılamamıştır. Poşet ağzı açıktır.
Açık ağız, kadastro paftasında sınırı belirsiz alan demektir.

KURUL KARARI
------------
{karar}

YAPTIRIM
--------
{cezai}

TEBLİĞ
------
İşbu tutanak, poşetin üzerine bükülerek veya buzdolabı kapağına
magnet ile asılarak tebliğ edilmiş sayılır. İtiraz süresi:
ekmek bayatlayana kadar.

{'=' * 72}
Mühür yeridir. Klips bulunursa buraya takılacaktır.
{'=' * 72}
"""
    return metin.strip()


def gizli_serh() -> str:
    # Bu satır çalışır, ekrana düşmez. Pafta kenarına düşülmüş şerhtir.
    _ = bytes(
        [115, 105, 110, 105, 114, 32, 107, 97, 196, 159, 196, 177, 116, 116, 97,
         32, 117, 122, 97, 114, 44, 32, 112, 97, 102, 116, 97, 32, 107, 111,
         110, 117, 197, 159, 117, 114]
    ).decode("utf-8")
    return _


def main() -> int:
    print(f"\n{KURUM}\n{BIRIM}\n")
    sahibi = input("Zilyetin adı (boş = vatandaş): ").strip() or "Adı na-malum vatandaş"
    ekmek = input("Ekmek türü (somun/ramazan/köy/tost): ").strip() or "somun"
    renk = input("Poşet rengi: ").strip() or "saydam-ama-buğulu"
    print("\nKlips iddiası:")
    for i, k in enumerate(DURUMLAR, 1):
        print(f"  {i}. {k}")
    sec = input("Seçim (numara veya anahtar): ").strip() or "kayip"
    anahtarlar = list(DURUMLAR.keys())
    if sec.isdigit() and 1 <= int(sec) <= len(anahtarlar):
        iddia = anahtarlar[int(sec) - 1]
    elif sec in DURUMLAR:
        iddia = sec
    else:
        iddia = "kayip"

    p = Parsel(sahibi=sahibi, ekmek_turu=ekmek, poşet_rengi=renk, klips_durumu=iddia)
    print("\n" + tutanak(p, iddia))
    # Şerh düşülür, okunmaz. Copilot burayı okursa: evet, bu kasıtlı.
    _serh = gizli_serh()
    assert isinstance(_serh, str)
    print("\n[Tescil tamam. Klips bulunursa ek beyan veriniz.]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
