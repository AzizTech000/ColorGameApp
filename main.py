import os
os.environ['KIVY_NO_CONSOLELOG'] = '0' # Logs dikhane ke liye
os.environ['KIVY_GL_BACKEND'] = 'angle' # Windows compatibility ke liye

from kivy.config import Config
Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', '1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import threading

# Aapki purani files yahan connect ho rahi hain
from scanner import ScreenScanner
from analyzer import ImageAnalyzer
from alert import AlertSystem
from logic import StrategyManager

class ColorGameAndroid(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.strategy = StrategyManager()
        self.scanner = ScreenScanner(self)
        self.is_locked = False
        self.seconds_left = 30
        self.timer_event = None
        
        # --- UI Design ---
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.8) # Dark background
            self.rect = Rectangle(size=(800, 500), pos=(50, 200))

        # Prediction Label (Upar wala text)
        self.pred_label = Label(
            text="PREDICTION: WAITING...",
            font_size='22sp',
            bold=True,
            color=(1, 1, 0, 1), # Yellow
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.add_widget(self.pred_label)

        # Timer Label (Bich wala countdown)
        self.timer_label = Label(
            text="30",
            font_size='40sp',
            bold=True,
            color=(0, 1, 0, 1), # Green
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.timer_label)

        # Lock Button
        self.lock_btn = Button(
            text="🔓 UNLOCK",
            size_hint=(0.25, 0.1),
            pos_hint={'x': 0.05, 'y': 0.85},
            background_color=(0.9, 0.5, 0.1, 1)
        )
        self.lock_btn.bind(on_press=self.toggle_lock)
        self.add_widget(self.lock_btn)

        # Start Button
        self.start_btn = Button(
            text="START SYSTEM",
            size_hint=(0.6, 0.15),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            background_color=(0, 0.5, 0.5, 1)
        )
        self.start_btn.bind(on_press=self.start_timer)
        self.add_widget(self.start_btn)

    def toggle_lock(self, instance):
        self.is_locked = not self.is_locked
        self.lock_btn.text = "🔒 LOCKED" if self.is_locked else "🔓 UNLOCK"
        self.lock_btn.background_color = (0.7, 0.2, 0.1, 1) if self.is_locked else (0.9, 0.5, 0.1, 1)

    def start_timer(self, instance):
        if not self.timer_event:
            self.timer_event = Clock.schedule_interval(self.update_clock, 1)
            self.start_btn.text = "SYSTEM ACTIVE"
            self.start_btn.background_color = (0.1, 0.7, 0.3, 1)

    def update_clock(self, dt):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            self.timer_label.text = f"{self.seconds_left:02d}"
            self.timer_label.color = (1, 0, 0, 1) if self.seconds_left <= 5 else (0, 1, 0, 1)
        else:
            self.seconds_left = 30
            # Jab 0 ho jaye to Scan shuru karo
            threading.Thread(target=self.do_scan, daemon=True).start()

    def do_scan(self):
        # 1. Screenshot lo (Scanner.py use karke)
        ss = self.scanner.capture_red_box()
        
        # 2. Number aur Size pehchano (Analyzer.py)
        num, sz = ImageAnalyzer.get_number_and_size(ss)
        
        if sz != "N/A":
            # 3. Next prediction calculate karo (Logic.py)
            next_pred, stage = self.strategy.calculate_next(sz)
            
            # 4. UI Update (Kivy ke liye schedule karna padta hai)
            Clock.schedule_once(lambda dt: self.update_prediction_display(next_pred, stage), 0)

    def update_prediction_display(self, pred, stage):
        self.pred_label.text = f"STAGE {stage}: {pred}"
        # Agar stage 6 ho to Alert (Alert.py)
        if stage >= 6:
            AlertSystem.trigger_danger_alert(self)

class MainApp(App):
    def build(self):
        return ColorGameAndroid()

if __name__ == '__main__':
    MainApp().run()