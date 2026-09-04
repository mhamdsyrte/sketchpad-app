"""
دفتر رسم بسيط - Kivy version (قابل للتحويل لـ APK)
"""

import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Line, Rectangle
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

COLORS = {
    "أسود": (0, 0, 0, 1),
    "أحمر": (1, 0, 0, 1),
    "أزرق": (0, 0, 1, 1),
    "أخضر": (0, 0.6, 0, 1),
    "أصفر": (1, 0.85, 0, 1),
}


class DrawingArea(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_width = 3
        self.current_color = (0, 0, 0, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.current_color)
                touch.ud["line"] = Line(points=(touch.x, touch.y), width=self.line_width)

    def on_touch_move(self, touch):
        if "line" in touch.ud:
            touch.ud["line"].points += [touch.x, touch.y]

    def clear_canvas(self):
        self.canvas.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

    def export_image(self, filename="drawing.png"):
        # يحفظ في مجلد التنزيلات على أندرويد إذا كانت الصلاحية موجودة
        try:
            from android.storage import primary_external_storage_path  # type: ignore
            downloads = os.path.join(primary_external_storage_path(), "Download")
        except Exception:
            downloads = os.path.expanduser("~")
        os.makedirs(downloads, exist_ok=True)
        path = os.path.join(downloads, filename)
        self.export_to_png(path)
        return path


class SketchApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical")

        self.drawing_area = DrawingArea()

        toolbar = BoxLayout(size_hint_y=0.12, spacing=5, padding=5)

        for name, rgba in COLORS.items():
            btn = Button(text=name, background_color=rgba)
            btn.bind(on_press=lambda inst, c=rgba: self.set_color(c))
            toolbar.add_widget(btn)

        clear_btn = Button(text="مسح")
        clear_btn.bind(on_press=lambda inst: self.drawing_area.clear_canvas())
        toolbar.add_widget(clear_btn)

        save_btn = Button(text="حفظ كصورة")
        save_btn.bind(on_press=self.save_image)
        toolbar.add_widget(save_btn)

        size_box = BoxLayout(size_hint_y=0.08, padding=5)
        size_box.add_widget(Label(text="حجم الفرشاة", size_hint_x=0.3))
        slider = Slider(min=1, max=20, value=3)
        slider.bind(value=self.set_line_width)
        size_box.add_widget(slider)

        root.add_widget(toolbar)
        root.add_widget(size_box)
        root.add_widget(self.drawing_area)
        return root

    def set_color(self, rgba):
        self.drawing_area.current_color = rgba

    def set_line_width(self, instance, value):
        self.drawing_area.line_width = value

    def save_image(self, instance):
        path = self.drawing_area.export_image()
        popup = Popup(title="تم الحفظ", content=Label(text=f"الصورة انحفظت في:\n{path}"),
                       size_hint=(0.8, 0.3))
        popup.open()


if __name__ == "__main__":
    SketchApp().run()
