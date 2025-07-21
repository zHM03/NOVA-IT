from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime

from commands.clock import saat
from commands.calculator import hesap_makinesi_popup_ac
from commands.reminder import hatirlatici_popup_ac
from commands.weather import weather
from commands.breath import breath
from commands.cleaner import clean
from commands.shutdown import kapatma_popup_ac

class AsistanEkrani(BoxLayout):
    kullanici_metni = StringProperty("")
    cevap = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kullanici_metni = self.saat_bazli_selamlama()
        
    def hatirlatici_popup_ac(self):
        print("Hatırlatıcı popup açıldı")
        hatirlatici_popup_ac(self)

    def hesap_makinesi_popup_ac(self):
        print("Hesap makinesi popup açıldı")
        hesap_makinesi_popup_ac(self)

    def kapatma_popup_ac(self):
        print("Shutdown popup açıldı")
        kapatma_popup_ac(self)

    def saat_bazli_selamlama(self):
        saat_ = datetime.now().hour
        if saat_ < 6:
            return "İyi geceler!"
        elif saat_ < 12:
            return "Günaydın!"
        elif saat_ < 18:
            return "İyi günler!"
        else:
            return "İyi akşamlar!"

    def yazili_girdi_isle(self, metin):
        metin = metin.strip()
        self.kullanici_metni = metin
        self.cevap = ""

        cevap = self.komut_calistir(metin, callback=self.guncelle_cevap)

        if not cevap:
            self.cevap = "Anlamadım"
        elif cevap != "Nefes egzersizi başladı...":
            self.cevap = cevap

    def guncelle_cevap(self, mesaj):
        Clock.schedule_once(lambda dt: setattr(self, 'cevap', mesaj))

    def komut_calistir(self, metin, callback=None):
        def hesap_makinesi_komut(metin):
            if "hesap makinesi" in metin.lower():
                hesap_makinesi_popup_ac(self)
                return "Hesap makinesi açıldı"
            return None

        komutlar = [
            lambda m: breath(m, callback=callback) if callback else None,
            saat,
            hesap_makinesi_komut,
            weather,
            clean,
            hatirlatici_popup_ac,
            kapatma_popup_ac,
        ]

        for komut in komutlar:
            try:
                sonuc = komut(metin)
                if sonuc:
                    return sonuc
            except Exception as e:
                print(f"[HATA] Komut çalıştırılırken hata oluştu: {e}")
                continue

        return None
