from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
import os
import speech_recognition as sr

class InputSection(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Background Image - Lo-Fi Style
        with self.canvas.before:
            self.bg_image = Image(source='bg2.jpg', allow_stretch=True, keep_ratio=False)
            self.bg_image.size = self.size  # Adjust image size to fit the window

        # Title label
        self.title_label = Label(
            text="Sign Language App",
            font_size=30,
            bold=True,
            color=(0, 0.5, 1, 1),
            size_hint_y=None,
            height=50,
            halign='center'
        )

        # Input field and label
        self.label = Label(text="Enter a sentence:")
        self.text_input = TextInput(hint_text="Type here", multiline=False, size_hint_y=None, height=40)
        self.text_input.background_normal = ''
        self.text_input.background_color = (0.9, 0.9, 0.9, 1)

        # Speech-to-text button with dynamic color change
        self.speech_button = Button(
            text="Record Speech",
            size_hint_y=None,
            height=50,
            background_color=(0, 1, 0, 1),  # Green color when idle
            bold=True,
            color=(0, 0, 0, 1)
        )
        self.speech_button.bind(on_press=self.record_speech)

        # Submit button for showing sign language images
        self.submit_button = Button(
            text="Show Sign Language",
            size_hint_y=None,
            height=50,
            background_color=(0, 0.5, 1, 1),
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.submit_button.bind(on_press=self.on_submit)

        # Scrollable layout for images
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.image_layout = GridLayout(cols=20, spacing=5, size_hint_y=None)
        self.image_layout.bind(minimum_height=self.image_layout.setter('height'))
        self.scroll_view.add_widget(self.image_layout)

        # Adding widgets to the layout
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
                # Add a spacer widget
                spacer = Widget(size_hint_x=None, width=40)
                self.image_layout.add_widget(spacer)
            elif char.isalpha():
                image_path = f"data_alphabets/{char}.png"
                if os.path.exists(image_path):
                    img = Image(
                        source=image_path,
                        size_hint=(None, None),  # Fixed size for each image
                        size=(80, 80),           # Consistent size for every image
                        allow_stretch=True,      # Stretch to fit box
                        keep_ratio=True          # Keep the correct aspect ratio
                    )
                    self.image_layout.add_widget(img)

    def record_speech(self, instance):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            # Change button color to red when listening
            self.speech_button.background_color = (1, 0, 0, 1)  # Red color
            print("Listening for speech...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        try:
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            self.text_input.text = text  # Display the recognized text in the TextInput
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
        finally:
            # Change button color back to green after listening
            self.speech_button.background_color = (0, 1, 0, 1)  # Green color when idle

    def on_size(self, *args):
        # This method ensures that the background image is resized when the window is resized
        self.bg_image.size = self.size


class MyApp(App):
    def build(self):
        return InputSection()

MyApp().run()
