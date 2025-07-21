from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

def hesap_makinesi_popup_ac(root_widget):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=15)
    
    girdi = TextInput(font_size=20, size_hint_y=None, height=40, multiline=False)
    layout.add_widget(girdi)
    
    tuslar = [
        '7', '8', '9', '+',
        '4', '5', '6', '-',
        '1', '2', '3', '*',
        'C', '0', '=', '/'
    ]
    
    grid = GridLayout(cols=4, spacing=6, size_hint_y=None)
    grid.height = 200
    
    def tus_basildi(instance):
        if instance.text == 'C':
            girdi.text = ''
        elif instance.text == '=':
            try:
                sonuc = eval(girdi.text, {"__builtins__": None}, {})
                girdi.text = str(sonuc)
            except:
                girdi.text = 'Hata!'
                root_widget.cevap = "Geçersiz matematiksel ifade"
        else:
            girdi.text += instance.text
    
    for tus in tuslar:
        btn = Button(
            text=tus,
            font_size=20,
            size_hint_y=None,
            height=40,
            background_color=(0.3, 0.5, 0.7, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        btn.bind(on_release=tus_basildi)
        grid.add_widget(btn)
    
    layout.add_widget(grid)
    
    btn_kapat = Button(
        text="Kapat",
        size_hint_y=None,
        height=40,
        background_color=(0.8, 0.2, 0.2, 1),
        background_normal='',
        color=(1, 1, 1, 1)
    )
    btn_kapat.bind(on_release=lambda _: popup.dismiss())
    layout.add_widget(btn_kapat)
    
    popup = Popup(
        title="",
        content=layout,
        size_hint=(0.7, 0.6),
        auto_dismiss=False,
        background=''
    )
    popup.background_color = (0, 0, 0.3, 1)
    popup.open()
