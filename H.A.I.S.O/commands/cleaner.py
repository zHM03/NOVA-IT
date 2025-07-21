import os
import shutil
import tempfile

def clean(metin):
    komutlar = ["temizle", "temizlik zamanı", "geçici dosyaları sil"]

    if not any(k in metin.lower() for k in komutlar):
        return None

    try:
        temp_path = tempfile.gettempdir()
        for root, dirs, files in os.walk(temp_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception:
                    pass
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                except Exception:
                    pass

        prefetch_path = r"C:\Windows\Prefetch"
        for root, dirs, files in os.walk(prefetch_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception:
                    pass
                
        alt_temp = r"C:\Windows\Temp"
        if os.path.exists(alt_temp):
            for root, dirs, files in os.walk(alt_temp, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception:
                        pass
                for name in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                    except Exception:
                        pass

    except Exception:
        pass

    return "Geçici dosyalar başarıyla silindi."
