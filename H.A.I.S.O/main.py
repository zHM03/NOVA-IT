import os
import sys
from kivy.config import Config
from kivy.lang import Builder
from kivy.app import App

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

kv_path = os.path.join(base_path, "ui.kv")
Builder.load_file(kv_path)

from ui import AsistanEkrani

class AsistanApp(App):
    def build(self):
        return AsistanEkrani()

if __name__ == "__main__":
    try:
        AsistanApp().run()
    except Exception as e:
        print("Hata oluştu:", e)
        import traceback
        traceback.print_exc()
