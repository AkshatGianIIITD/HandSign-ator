

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
import os
import threading
import speech_recognition as sr
from kivy.uix.relativelayout import RelativeLayout


# Define the font globally
ALDRICH_FONT =  r'sign_language_1\Aldrich\Aldrich-Regular.ttf'  # Ensure Aldrich.ttf is available in your project folder

class InputSection(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [30, 50, 30, 50]
        self.spacing = 20

        # Title label
        self.title_label = Label(
            text=" HandVoice",
            font_size=32,
            bold=True,
            font_name=ALDRICH_FONT,
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=60
        )

        # Input field and label
        self.label = Label(
            text="Enter a sentence:",
            font_size=20,
            font_name=ALDRICH_FONT,
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height=30
        )

        self.text_input = TextInput(
            hint_text="Type here...",
            multiline=False,
            size_hint_y=None,
            height=50,
            background_normal='',
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0.2, 0.2, 0.8, 1),
            font_size=18,
            font_name=ALDRICH_FONT
        )

        # Speech-to-text button
        self.speech_button = Button(
            text=" Record Speech",
            size_hint_y=None,
            height=55,
            background_normal='',
            background_color=(80/255, 227/255, 194/255, 1),  # Light Teal
            color=(0, 0, 0, 1),
            font_size=20,
            font_name=ALDRICH_FONT
        )
        self.speech_button.bind(on_press=self.record_speech)

        # Submit button
        self.submit_button = Button(
            text=" Show Sign Language",
            size_hint_y=None,
            height=55,
            background_normal='',
            background_color=(74/255, 144/255, 226/255, 1),  # Soft Blue
            color=(1, 1, 1, 1),
            font_size=20,
            font_name=ALDRICH_FONT
        )
        self.submit_button.bind(on_press=self.on_submit)

        # Scrollable layout for images
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.image_layout = GridLayout(cols=20, spacing=5, size_hint_y=None)
        self.image_layout.bind(minimum_height=self.image_layout.setter('height'))
        self.scroll_view.add_widget(self.image_layout)

        # Adding widgets
        self.add_widget(self.title_label)
        self.add_widget(self.label)
        self.add_widget(self.text_input)
        self.add_widget(self.speech_button)
        self.add_widget(self.submit_button)
        self.add_widget(self.scroll_view)

    def on_submit(self, instance):
        sentence = self.text_input.text.upper()
        self.image_layout.clear_widgets()

        for char in sentence:
            if char == ' ':
                spacer = Widget(size_hint_x=None, width=40)
                self.image_layout.add_widget(spacer)
            elif char.isalpha():
                image_path = f"sign_language_1/data_alphabets/{char}.png"
                if os.path.exists(image_path):
                    img = Image(
                        source=image_path,
                        size_hint=(None, None),
                        size=(80, 80),
                        allow_stretch=True,
                        keep_ratio=True
                    )
                    self.image_layout.add_widget(img)

    def record_speech(self, instance):
        threading.Thread(target=self._record_speech_thread).start()

    def _record_speech_thread(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            self.update_button_color((1, 0, 0, 1))  # Red while listening
            print("Listening for speech...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            self.update_text_input(text)
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
        finally:
            self.update_button_color((80/255, 227/255, 194/255, 1))  # Light teal again

    def update_text_input(self, text):
        Clock.schedule_once(lambda dt: setattr(self.text_input, 'text', text))

    def update_button_color(self, color):
        Clock.schedule_once(lambda dt: setattr(self.speech_button, 'background_color', color))
