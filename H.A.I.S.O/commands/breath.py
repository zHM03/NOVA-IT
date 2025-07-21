from kivy.clock import Clock
import threading
import time

def _geri_sayim(mesaj, sure, callback):
    for i in range(sure, -1, -1):
        if callback:
            Clock.schedule_once(lambda dt, m=mesaj, s=i: callback(f"{m} {s}"))
        time.sleep(1)

def _nefes_egzersizi_thread(callback):
    adimlar = [
        ("Derin nefes alın", 4),
        ("Nefesinizi tutun", 7),
        ("Yavaşça nefes verin", 8),
        ("Tekrar derin nefes alın", 4)
    ]

    time.sleep(2) 

    for mesaj, sure in adimlar:
        _geri_sayim(mesaj, sure, callback)

    if callback:
        Clock.schedule_once(lambda dt: callback("Kendinizi daha iyi hissediyor musnuz?"))

def breath(metin: str, callback=None) -> str:
    if "nefes" in metin.lower():
        threading.Thread(target=_nefes_egzersizi_thread, args=(callback,), daemon=True).start()
        return "Duruşunuzu Düzeltin..."
    return None
