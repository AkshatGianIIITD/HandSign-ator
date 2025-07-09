
# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.widget import Widget
# from kivy.uix.image import Image
# from kivy.uix.anchorlayout import AnchorLayout
# from kivy.core.window import Window

# # Set the background color (Soft White)
# Window.clearcolor = (249/255, 250/255, 251/255, 1)  # RGB normalized to 0-1

# # Import the widgets (layouts) from your two apps
# from signToText import SignTranslatorKivy
# from Text_To_Sign import InputSection

# # If Aldrich.ttf is not in default fonts, you must put it inside your project folder
# ALDRICH_FONT = r'sign_language_1\Aldrich\Aldrich-Regular.ttf'  # path to your font

# class HomeScreen(Screen):
#     def __init__(self, **kwargs):
#         super(HomeScreen, self).__init__(**kwargs)

#         main_layout = BoxLayout(orientation='vertical', spacing=30, padding=[50, 100, 50, 100])

#         # Optional: Add a logo or title at the top
#         title = Label(
#             text=" Sign Language Translator",
#             font_size=32,
#             bold=True,
#             color=(0.2, 0.2, 0.2, 1),
#             font_name=ALDRICH_FONT
#         )
#         main_layout.add_widget(title)

#         # Spacer
#         main_layout.add_widget(Widget(size_hint_y=None, height=20))

#         # Buttons area
#         btn_layout = BoxLayout(orientation='vertical', spacing=20)

#         btn1 = Button(
#             text="Sign to Text",
#             font_size=24,
#             font_name=ALDRICH_FONT,
#             size_hint=(1, None),
#             height=70,
#             background_normal='',
#             background_color=(74/255, 144/255, 226/255, 1),  # Soft Blue
#             color=(1, 1, 1, 1),
#             border=(20, 20, 20, 20)
#         )
#         btn1.bind(on_press=self.goto_sign_to_text)

#         btn2 = Button(
#             text="Text to Sign",
#             font_size=24,
#             font_name=ALDRICH_FONT,
#             size_hint=(1, None),
#             height=70,
#             background_normal='',
#             background_color=(80/255, 227/255, 194/255, 1),  # Light Teal
#             color=(1, 1, 1, 1),
#             border=(20, 20, 20, 20)
#         )
#         btn2.bind(on_press=self.goto_text_to_sign)

#         btn_layout.add_widget(btn1)
#         btn_layout.add_widget(btn2)

#         main_layout.add_widget(btn_layout)

#         # Spacer at bottom
#         main_layout.add_widget(Widget())

#         # Center everything
#         anchor = AnchorLayout(anchor_x='center', anchor_y='center')
#         anchor.add_widget(main_layout)

#         self.add_widget(anchor)

#     def goto_sign_to_text(self, instance):
#         self.manager.current = 'sign_to_text'

#     def goto_text_to_sign(self, instance):
#         self.manager.current = 'text_to_sign'

# class SignToTextScreen(Screen):
#     def __init__(self, **kwargs):
#         super(SignToTextScreen, self).__init__(**kwargs)
#         self.layout = BoxLayout(orientation='vertical')

#         # Add a back button at the top
#         self.back_btn = Button(
#             text="Back to Home",
#             size_hint=(1, 0.1),
#             font_name=ALDRICH_FONT
#         )
#         self.back_btn.bind(on_press=self.back_to_home)
#         self.layout.add_widget(self.back_btn)

#         self.sign_to_text_widget = None  # Widget not created yet
#         self.add_widget(self.layout)

#     def on_enter(self):
#         # Create fresh widget every time we enter
#         self.sign_to_text_widget = SignTranslatorKivy(model_path=r"sign_language_1\best.pt")
#         self.layout.add_widget(self.sign_to_text_widget)

#     def on_leave(self):
#         # When leaving, release camera and delete widget
#         if self.sign_to_text_widget:
#             self.sign_to_text_widget.on_stop()  # release VideoCapture
#             self.layout.remove_widget(self.sign_to_text_widget)
#             self.sign_to_text_widget = None

#     def back_to_home(self, instance):
#         self.manager.current = 'home'

# class TextToSignScreen(Screen):
#     def __init__(self, **kwargs):
#         super(TextToSignScreen, self).__init__(**kwargs)
#         layout = BoxLayout(orientation='vertical')

#         # Add a back button on top
#         back_btn = Button(
#             text="Back to Home",
#             size_hint=(1, 0.1),
#             font_name=ALDRICH_FONT
#         )
#         back_btn.bind(on_press=self.back_to_home)
#         layout.add_widget(back_btn)

#         # Add your original widget
#         layout.add_widget(InputSection())

#         self.add_widget(layout)

#     def back_to_home(self, instance):
#         self.manager.current = 'home'

# class MainApp(App):
#     def build(self):
#         sm = ScreenManager()

#         # First screen added will be the default (home screen)
#         sm.add_widget(HomeScreen(name='home'))
#         sm.add_widget(SignToTextScreen(name='sign_to_text'))
#         sm.add_widget(TextToSignScreen(name='text_to_sign'))

#         sm.current = 'home'  # <-- Explicitly set home as the first screen

#         return sm

# if __name__ == '__main__':
#     MainApp().run()


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout  # <-- Import FloatLayout
from kivy.core.window import Window

# Set the background color (Soft White) -- Still there if image doesn't load
Window.clearcolor = (249/255, 250/255, 251/255, 1)

from signToText import SignTranslatorKivy
from Text_To_Sign import InputSection

ALDRICH_FONT = r'sign_language_1\Aldrich\Aldrich-Regular.ttf'

# Set your background image path
BACKGROUND_IMAGE = r"sign_language_1\bg.jpg"  # <-- Put your image in this location

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        # Background image
        bg_image = Image(
            source=BACKGROUND_IMAGE,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 0.2)  # <-- 20% opacity (RGBA)
        )
        layout.add_widget(bg_image)

        # Main content
        main_layout = BoxLayout(orientation='vertical', spacing=30, padding=[50, 100, 50, 100])

        title = Label(
            text="HandVoice",
            font_size=54,
            bold=True,
            color=(0.2, 0.2, 0.2, 1),
            font_name=ALDRICH_FONT
        )
        main_layout.add_widget(title)

        main_layout.add_widget(Widget(size_hint_y=None, height=20))

        btn_layout = BoxLayout(orientation='vertical', spacing=20)

        btn1 = Button(
            text="Sign to Text",
            font_size=24,
            font_name=ALDRICH_FONT,
            size_hint=(1, None),
            height=70,
            background_normal='',
            background_color=(74/255, 144/255, 226/255, 1),  # <-- full opaque
            color=(1, 1, 1, 1),
            border=(20, 20, 20, 20)
        )
        btn1.bind(on_press=self.goto_sign_to_text)

        btn2 = Button(
            text="Text to Sign",
            font_size=24,
            font_name=ALDRICH_FONT,
            size_hint=(1, None),
            height=70,
            background_normal='',
            background_color=(80/255, 227/255, 194/255, 1),
            color=(1, 1, 1, 1),
            border=(20, 20, 20, 20)
        )
        btn2.bind(on_press=self.goto_text_to_sign)

        btn_layout.add_widget(btn1)
        btn_layout.add_widget(btn2)

        main_layout.add_widget(btn_layout)
        main_layout.add_widget(Widget())

        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        anchor.add_widget(main_layout)

        layout.add_widget(anchor)

        self.add_widget(layout)

    def goto_sign_to_text(self, instance):
        self.manager.current = 'sign_to_text'

    def goto_text_to_sign(self, instance):
        self.manager.current = 'text_to_sign'

class SignToTextScreen(Screen):
    def __init__(self, **kwargs):
        super(SignToTextScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        bg_image = Image(
            source=BACKGROUND_IMAGE,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 0.2)  # <-- Add this line for 20% opacity
        )
        layout.add_widget(bg_image)

        self.layout = BoxLayout(orientation='vertical')

        self.back_btn = Button(
            text="Back to Home",
            size_hint=(1, 0.1),
            font_name=ALDRICH_FONT
        )
        self.back_btn.bind(on_press=self.back_to_home)
        self.layout.add_widget(self.back_btn)

        self.sign_to_text_widget = None
        layout.add_widget(self.layout)

        self.add_widget(layout)

    def on_enter(self):
        self.sign_to_text_widget = SignTranslatorKivy(model_path=r"sign_language_1\best.pt")
        self.layout.add_widget(self.sign_to_text_widget)

    def on_leave(self):
        if self.sign_to_text_widget:
            self.sign_to_text_widget.on_stop()
            self.layout.remove_widget(self.sign_to_text_widget)
            self.sign_to_text_widget = None

    def back_to_home(self, instance):
        self.manager.current = 'home'

class TextToSignScreen(Screen):
    def __init__(self, **kwargs):
        super(TextToSignScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        bg_image = Image(
            source=BACKGROUND_IMAGE,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            color=(1, 1, 1, 0.05)  # <-- Add this line for 20% opacity
        )
        layout.add_widget(bg_image)

        content_layout = BoxLayout(orientation='vertical')

        back_btn = Button(
            text="Back to Home",
            size_hint=(1, 0.1),
            font_name=ALDRICH_FONT
        )
        back_btn.bind(on_press=self.back_to_home)
        content_layout.add_widget(back_btn)

        content_layout.add_widget(InputSection())

        layout.add_widget(content_layout)

        self.add_widget(layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SignToTextScreen(name='sign_to_text'))
        sm.add_widget(TextToSignScreen(name='text_to_sign'))
        sm.current = 'home'
        return sm

if __name__ == '__main__':
    MainApp().run()
