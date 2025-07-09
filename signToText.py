import cv2
import time
import difflib
import requests
import pyttsx3
import pygame

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.button import Button
from ultralytics import YOLO
from kivy.core.text import LabelBase

LabelBase.register(name='Aldrich', fn_regular=r'sign_language_1\Aldrich\Aldrich-Regular.ttf')

# --- Initialize TTS and Sound ---
engine = pyttsx3.init()
pygame.mixer.init()
beep_sound = pygame.mixer.Sound(r"sign_language_1\beep-329314.mp3")  # Provide a small "beep.wav" sound file in your project folder

# --- KV Layout (Modern, Clean, Consistent Theme) ---
# --- KV Layout (with Aldrich font applied) ---
Builder.load_string("""
<SignTranslatorKivy>:
    orientation: 'vertical'
    spacing: dp(16)
    padding: dp(20)

    canvas.before:
        Color:
            rgba: 0.07, 0.07, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Title Section
    BoxLayout:
        size_hint_y: None
        height: dp(60)
        Label:
            text: 'Sign Language Translator'
            font_size: '28sp'
            font_name: 'Aldrich'
            bold: True
            color: 0.4, 0.8, 1, 1
            halign: 'center'
            valign: 'middle'
            text_size: self.size

    # Camera Feed
    Image:
        id: camera_feed
        size_hint_y: 0.65
        allow_stretch: True
        keep_ratio: True
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.14, 1
            Rectangle:
                pos: self.pos
                size: self.size

    # Button Controls
    BoxLayout:
        size_hint_y: None
        height: dp(55)
        spacing: dp(10)

        Button:
            text: 'Clear'
            id: clear_btn
            font_name: 'Aldrich'
            background_normal: ''
            background_color: 0.2, 0.6, 0.86, 1
            color: 1, 1, 1, 1
            font_size: '16sp'
            bold: True
            on_release: root.clear_text()

        Button:
            text: 'Pause'
            id: pause_btn
            font_name: 'Aldrich'
            background_normal: ''
            background_color: 0.18, 0.55, 0.78, 1
            color: 1, 1, 1, 1
            font_size: '16sp'
            bold: True
            on_release: root.toggle_pause()

        Button:
            text: 'Autocorrect'
            id: autocorrect_btn
            font_name: 'Aldrich'
            background_normal: ''
            background_color: 0.16, 0.5, 0.75, 1
            color: 1, 1, 1, 1
            font_size: '16sp'
            bold: True
            on_release: root.autocorrect_text()

        Button:
            text: 'Speak'
            id: tts_btn
            font_name: 'Aldrich'
            background_normal: ''
            background_color: 0.14, 0.45, 0.7, 1
            color: 1, 1, 1, 1
            font_size: '16sp'
            bold: True
            on_release: root.speak_text()

    # Text Output
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.25
        padding: dp(10)
        spacing: dp(10)

        Label:
            id: result_text
            text: ''
            font_size: '22sp'
            font_name: 'Aldrich'
            halign: 'center'
            valign: 'middle'
            text_size: self.width - dp(20), None
            color: 0, 1, 1, 1
            bold: True
            size_hint_y: None
            height: self.texture_size[1]

        Label:
            id: corrected_text
            text: ''
            font_size: '20sp'
            font_name: 'Aldrich'
            halign: 'center'
            valign: 'middle'
            text_size: self.width - dp(20), None
            color: 1, 0.8, 0.4, 1
            bold: True
            size_hint_y: None
            height: self.texture_size[1]
""")




# --- Helper Functions ---
VALID_WORDS = ['hello', 'help', 'home', 'good', 'yes', 'no', 'thanks', 'please', 'sorry', 'how', 'are', 'you', 'sir', 'akshat', 'kabir']

def autocorrect(text):
    text = text.replace(' ', '')
    matches = difflib.get_close_matches(text, VALID_WORDS, n=1, cutoff=0.1)
    if matches:
        return matches[0]
    else:
        return text

def autocomplete(text):
    text = text.replace(' ', '')
    matches = [word for word in VALID_WORDS if word.startswith(text.lower())]
    if matches:
        return matches[0]
    else:
        return text

def send_to_gemini(text):
    GEMINI_API_KEY = "<REPLACE-WITH-YOUR-API-KEY>"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""You are given a list of valid words: {VALID_WORDS}.
                                    Given an input {text}, autocorrect it by matching and separating words strictly from the list.

                                    If the input is a single word, correct it to the closest matching word.

                                    If the input is a sequence, split and correct it into valid words.

                                    Keep the total number of characters (excluding spaces) approximately the same as the input.
                                    Return only the corrected and separated sentence, without any explanations."""
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "Error parsing Gemini response."
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Main App ---
class SignTranslatorKivy(BoxLayout):
    def __init__(self, model_path, **kwargs):
        super().__init__(**kwargs)
        self.model = YOLO(model_path)
        self.capture = cv2.VideoCapture(1)
        self.translation_buffer = []
        self.last_detection_time = time.time()
        self.last_capture_time = time.time()
        self.capture_interval = 2
        self.paused = False
        Clock.schedule_interval(self.update, 1/30)

    def update(self, dt):
        if self.paused:
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        frame_height, frame_width = frame.shape[:2]
        center_x, center_y = frame_width // 2, frame_height // 2
        region_w, region_h = frame_width * 0.7, frame_height * 0.7
        region_x1, region_y1 = center_x - region_w / 2, center_y - region_h / 2
        region_x2, region_y2 = center_x + region_w / 2, center_y + region_h / 2

        if time.time() - self.last_capture_time >= self.capture_interval:
            results = self.model(frame)
            annotated = results[0].plot()

            if results[0].boxes.cls is not None and len(results[0].boxes.cls) > 0:
                for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
                    x1, y1, x2, y2 = box.cpu().numpy()
                    label = self.model.names[int(cls.cpu().numpy())]

                    # if label in ['Q', 'R', 'K']:
                    #     continue
                    if label in ['Q']:
                          continue

                    box_center_x = (x1 + x2) / 2
                    box_center_y = (y1 + y2) / 2

                    if region_x1 <= box_center_x <= region_x2 and region_y1 <= box_center_y <= region_y2:
                        self.translation_buffer.append(label)
                        beep_sound.play()  # Play sound on new letter detection

                        raw_text = ''.join(self.translation_buffer).rstrip()
                        words = raw_text.split(' ')
                        if words:
                            last_word = words[-1]
                            predicted = autocomplete(last_word)
                            if predicted.startswith(last_word) and predicted != last_word:
                                suggestion = predicted[len(last_word):]
                                for ch in suggestion:
                                    self.translation_buffer.append(ch)

                        self.last_detection_time = time.time()
                        break

            self.last_capture_time = time.time()
        else:
            annotated = frame.copy()

        if time.time() - self.last_detection_time > 6:
            if not self.translation_buffer or self.translation_buffer[-1] != ' ':
                raw_text = ''.join(self.translation_buffer).rstrip()
                words = raw_text.split(' ')
                if words:
                    last_word = words[-1]
                    corrected = autocorrect(last_word)
                    if corrected != last_word:
                        for _ in range(len(last_word)):
                            if self.translation_buffer:
                                self.translation_buffer.pop()
                        for ch in corrected:
                            self.translation_buffer.append(ch)
                self.last_detection_time = time.time()

        annotated = cv2.rectangle(annotated,
                                  (int(region_x1), int(region_y1)),
                                  (int(region_x2), int(region_y2)),
                                  (0, 255, 0), 2)

        buf = cv2.flip(annotated, 0).tobytes()
        tex = Texture.create(size=(annotated.shape[1], annotated.shape[0]), colorfmt='bgr')
        tex.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.camera_feed.texture = tex

        self.ids.result_text.text = ''.join(self.translation_buffer)

    def clear_text(self):
        self.translation_buffer.clear()
        self.ids.result_text.text = ''
        self.ids.corrected_text.text = ''

    def toggle_pause(self):
        self.paused = not self.paused
        btn = self.ids.pause_btn
        btn.text = 'Resume' if self.paused else 'Pause'

    def autocorrect_text(self):
        current_text = ''.join(self.translation_buffer)
        corrected_sentence = send_to_gemini(current_text)
        self.ids.corrected_text.text = corrected_sentence

    def speak_text(self):
        text = self.ids.corrected_text.text
        if text:
            engine.say(text)
            engine.runAndWait()

    def on_stop(self):
        self.capture.release()

class SignLanguageApp(App):
    def build(self):
        return SignTranslatorKivy(model_path=r"sign_language_1\best.pt")

    def on_stop(self):
        self.root.on_stop()

if __name__ == '__main__':
    SignLanguageApp().run()
