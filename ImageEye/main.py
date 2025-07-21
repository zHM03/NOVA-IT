import cv2
from ultralytics import YOLO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.animation import Animation
import threading
import sys
import os

Window.size = (900, 600)
Window.clearcolor = get_color_from_hex('#121212')

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_path, 'yolov8l.pt')

model = None

class BgImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class LoadingBar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bar_width = 0
        with self.canvas:
            Color(0.2, 0.7, 0.9, 1)
            self.rect = Rectangle(pos=self.pos, size=(self.bar_width, self.height))
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.bar_width, self.height)
    def start(self, duration=2, on_complete=None):
        self.bar_width = 0
        anim = Animation(bar_width=self.width, duration=duration)
        anim.bind(on_progress=lambda *x: self.update_rect())
        if on_complete:
            anim.bind(on_complete=lambda *x: on_complete())
        anim.start(self)

class ImageEyeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        self.title_label = Label(
            text="[b][size=32]ImageEye[/size][/b]",
            markup=True,
            color=get_color_from_hex('#e0e0e0'),
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.title_label)

        self.subtitle_label = Label(
            text="Model hazırlanıyor...",
            color=get_color_from_hex('#f0f0f0'),
            size_hint=(1, 0.05)
        )
        self.layout.add_widget(self.subtitle_label)

        self.middle_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint=(1, 0.7))

        self.img_widget = BgImage(size_hint=(0.7, 1), allow_stretch=True, keep_ratio=True)
        self.middle_layout.add_widget(self.img_widget)

        self.scrollview = ScrollView(size_hint=(0.3, 1))
        self.obj_list = GridLayout(cols=1, size_hint_y=None, spacing=8, padding=8)
        self.obj_list.bind(minimum_height=self.obj_list.setter('height'))
        self.scrollview.add_widget(self.obj_list)
        self.middle_layout.add_widget(self.scrollview)

        self.layout.add_widget(self.middle_layout)

        self.btn_select = Button(
            text="Resim Seç",
            size_hint=(1, 0.1),
            font_size=20,
            background_normal='',
            background_color=get_color_from_hex('#080054'),
            color=get_color_from_hex('#f0f0f0'),
            bold=True
        )
        self.btn_select.bind(on_release=self.show_file_chooser)
        self.layout.add_widget(self.btn_select)
        self.btn_select.disabled = True

        self.loading_bar = LoadingBar(size_hint=(1, 0.02))
        self.layout.add_widget(self.loading_bar)
        self.loading_bar.opacity = 0

        self.status_label = Label(
            text="Model yükleniyor...",
            size_hint=(1, 0.05),
            color=get_color_from_hex('#f0f0f0')
        )
        self.layout.add_widget(self.status_label)

        Window.bind(on_dropfile=self.on_file_drop)

        threading.Thread(target=self.load_model_thread, daemon=True).start()

        return self.layout

    def on_file_drop(self, window, file_path):
        path = file_path.decode('utf-8')
        self.start_processing(path)

    def load_model_thread(self):
        global model
        try:
            model = YOLO(model_path)
        except Exception as e:
            print("Model indiriliyor...", e)
            model = YOLO("yolov8l.pt")

        Clock.schedule_once(lambda dt: self.on_model_loaded())

    def on_model_loaded(self):
        self.status_label.text = "Model yüklendi. Lütfen bir resim seçin."
        self.subtitle_label.text = "YOLOv8l Modeli ile Gelişmiş Nesne Tespiti"
        self.btn_select.disabled = False

    def show_file_chooser(self, instance):
        content = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        popup = Popup(title="Resim Dosyası Seç", content=content, size_hint=(0.9, 0.9))

        def file_chosen(instance, selection, touch):
            if selection:
                popup.dismiss()
                self.start_processing(selection[0])

        content.bind(on_submit=file_chosen)
        popup.open()

    def start_processing(self, image_path):
        self.status_label.text = "Resim seçildi, görüntüleniyor..."
        self.loading_bar.opacity = 1
        self.display_image(image_path)

        threading.Thread(target=self.run_model_thread, args=(image_path,), daemon=True).start()
        self.loading_bar.start(duration=2, on_complete=self.loading_bar_done)

    def display_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            self.status_label.text = "Resim açılamadı!"
            self.loading_bar.opacity = 0
            return
        (h, w) = image.shape[:2]
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        buf = image_rgb.tobytes()

        texture = Texture.create(size=(w, h))
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.img_widget.texture = texture
        self.original_image = image

    def run_model_thread(self, image_path):
        results = model(self.original_image)
        Clock.schedule_once(lambda dt: self.show_results(results))

    def loading_bar_done(self, *args):
        pass

    def show_results(self, results):
        self.obj_list.clear_widgets()
        total_boxes = sum(len(r.boxes) for r in results)

        if total_boxes == 0:
            label = Label(
                text="Tespit edilemedi!",
                size_hint_y=None,
                height=40,
                font_size=20,
                color=get_color_from_hex('#ff5252'),
                bold=True
            )
            self.obj_list.add_widget(label)
        else:
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls)
                    conf = box.conf.item()
                    cls_name = model.names[cls_id]
                    label = Label(
                        text=f"{cls_name}: {conf:.2f}",
                        size_hint_y=None,
                        height=40,
                        font_size=20,
                        color=get_color_from_hex('#f0f0f0'),
                        bold=True
                    )
                    self.obj_list.add_widget(label)

        annotated_frame = results[0].plot()
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        buf = annotated_frame.tobytes()
        (h, w) = annotated_frame.shape[:2]
        texture = Texture.create(size=(w, h))
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.img_widget.texture = texture

        self.status_label.text = "Tespit tamamlandı!"
        self.loading_bar.opacity = 0


if __name__ == "__main__":
    ImageEyeApp().run()
