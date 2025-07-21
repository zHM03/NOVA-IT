from datetime import datetime

def saat(metin: str) -> str:
    metin = metin.lower()

    if "saat" in metin:
        simdi = datetime.now()
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        tarih_str = f"{simdi.day} {aylar[simdi.month - 1]} {simdi.year}, {gunler[simdi.weekday()]}"
        return f"               Saat {simdi.hour}:{simdi.minute:02d}\n{tarih_str}"
    
    elif "tarih" in metin or "hangi gündeyiz" in metin or "kaçıncı gün" in metin or "ayın kaçı" in metin:
        simdi = datetime.now()
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        tarih_str = f"{simdi.day} {aylar[simdi.month - 1]} {simdi.year}, {gunler[simdi.weekday()]}"
        return f"Bugün:\n{tarih_str}"
    
    return None
