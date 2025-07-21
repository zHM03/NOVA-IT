import os
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def hatirlatici_popup_ac(root_widget):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    layout.add_widget(Label(text="Hatırlatıcı Kur", font_size=20, size_hint_y=None, height=30))
    layout.add_widget(Label(size_hint_y=None, height=10))
    input_kutu = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)

    sure_input = TextInput(
        hint_text="Süre (dk)", 
        multiline=False, 
        input_filter='int',
        size_hint=(0.3, 1)
    )
    mesaj_input = TextInput(
        hint_text="Mesaj", 
        multiline=False,
        size_hint=(0.7, 1)
    )

    input_kutu.add_widget(sure_input)
    input_kutu.add_widget(mesaj_input)
    layout.add_widget(input_kutu)

    buton_kutu = BoxLayout(size_hint_y=None, height=40, spacing=10)
    btn_baslat = Button(text="Başlat", background_color=(0, 1, 0, 1))
    btn_iptal = Button(text="İptal", background_color=(1, 0, 0, 1))
    buton_kutu.add_widget(btn_baslat)
    buton_kutu.add_widget(btn_iptal)
    layout.add_widget(buton_kutu)

    popup = Popup(title="Hatırlatıcı", content=layout, size_hint=(0.6, 0.4), auto_dismiss=False)
    popup.open()


    def hatirlatici_calis(dt):
        def play_sound(dt):
            sound = SoundLoader.load(ses_dosyasi)
            if sound:
                sound.play()
        Clock.schedule_once(play_sound)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ses_dosyasi = os.path.join(base_dir, "assets", "ding.mp3")
        sound = SoundLoader.load(ses_dosyasi)
        if sound:
            sound.play()

        def popup_goster(dt):
            popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            popup_layout.add_widget(Label(text=f"Hatırlatma:\n{mesaj_input.text}", font_size=18))

            btn_tamam = Button(text="Tamam", size_hint_y=None, height=40)
            popup_layout.add_widget(btn_tamam)

            hatirlatma_popup = Popup(title="Hatırlatıcı", content=popup_layout,
                                     size_hint=(0.6, 0.4), auto_dismiss=False)

            btn_tamam.bind(on_release=hatirlatma_popup.dismiss)
            hatirlatma_popup.open()

        Clock.schedule_once(popup_goster)

    def baslat(_):
        dakika_str = sure_input.text.strip()
        mesaj = mesaj_input.text.strip()

        try:
            dakika = int(dakika_str)
            if dakika <= 0 or not mesaj:
                root_widget.cevap = "Lütfen geçerli süre ve mesaj girin."
                return
        except ValueError:
            root_widget.cevap = "Süre sayı olmalı."
            return

        sure_saniye = dakika *60
        popup.dismiss()
        root_widget.cevap = f"{dakika} dakika sonra hatırlatma yapılacak."
        root_widget.hatirlatici_event = Clock.schedule_once(hatirlatici_calis, sure_saniye)

    def iptal(_):
        popup.dismiss()

    btn_baslat.bind(on_release=baslat)
    btn_iptal.bind(on_release=iptal)

    popup.open()
