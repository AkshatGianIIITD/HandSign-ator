# **HANDSIGN \- Sign Language Translator**

## **Overview**

HANDSIGN is an innovative Sign Language Translator application developed by Group 1 for FVE 2025\. This project aims to bridge communication gaps by providing a versatile platform for translating sign language to text/speech and vice-versa.

For a visual demonstration and more information, please check out our design presentation on [Canva](https://www.canva.com/design/DAGlpdPJcUo/ex1hLADz94YlG9FArJYQ1Q/edit?utm_content=DAGlpdPJcUo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton&authuser=0).

## **Features**

The application offers a range of functionalities to facilitate seamless communication:

* **Sign Language Translator:**  
  * **Input:** Camera (for sign language detection)  
  * **Output:** Text  
  * **Functions:**  
    * **Clear:** Clears the current text output.  
    * **Pause:** Pauses the video feed.  
    * **Auto Correct:** AI-powered correction for misspelled words in the output.  
    * **Speak:** Text output can be read aloud.  
* **Speech to Sign:**  
  * **Input:** Speech  
  * **Output:** Sign Language (visual representation)  
  * **Function:** Show Sign / Translate  
* **Text to Sign:**  
  * **Input:** Text  
  * **Output:** Sign Language (visual representation)  
  * **Function:** Show Sign / Translate

## **Project Map**

The core functionalities are interconnected as follows:

* **Landing Page:** Serves as the entry point to the application.  
* **Sign Language Translator:** Directly accessible from the Landing Page.  
* **Speech to Sign:** Directly accessible from the Landing Page.  
* **Text to Sign:** Directly accessible from the Landing Page.

## **Use Cases**

HANDSIGN addresses various communication scenarios:

<img width="1234" height="695" alt="image" src="https://github.com/user-attachments/assets/c1b512c2-14e8-46c7-9662-a907a2017e38" />


## **Installation**

To get started with the HANDSIGN application, please follow these installation steps:

### **Prerequisites**

* Python

### **Python Package Installation**

To use the application's UI, hand detection, YOLOv11 model, and speech recognition features, install the following Python packages:

* **For UI (Kivy):**  
  pip install kivy

* **For Hand Detection (OpenCV):**  
  pip install opencv-python

* **For Detection Model (YOLOv11 with Ultralytics):**  
  pip install ultralytics

* **For Speech Recognition (SpeechRecognition and PyAudio):**  
  pip install SpeechRecognition  
  pip install pipwin  
  pipwin install pyaudio

  **Note:** The pip install \<package\> command is specific to Windows. For Linux and macOS, please use the equivalent commands or methods to install PyAudio.

## **Usage**

Follow these steps to clone the project and run the HANDSIGN application:

### **Getting Started**

1. **Clone the Repository:**  
   git clone \<your-repository-url\>  
   cd handsign-project

   *(Replace \<your-repository-url\> with the actual URL of your GitHub repository.)*  
2. **Complete Installations:** Ensure all the packages listed in the [Installation](https://www.google.com/search?q=%23installation) section are successfully installed.  
3. Run the Application:  
   Open your terminal or command prompt in the project's root directory and execute:  
   python app.py

### **Application Features Guide**

Upon launching the application, you will be presented with a homepage offering two main options: **Sign to Text** and **Text to Sign**.

#### **Sign to Text Feature**

Click the **Sign to Text** button to open the dedicated window. This feature is part of the **HandVoice** application and is designed to empower individuals with speech impairments to communicate effectively using sign language.

* **Sign Language Input:** Users provide sign language input through their camera. The application detects these signs and converts them into text.  
* **Text-to-Speech:** The generated text can be read aloud using the built-in text-to-speech feature, enabling clearer verbal communication. For example, signing letters like G, O, and D will display the word “good,” which can then be spoken aloud by the app.  
* **Auto-Correction:** The page supports auto-correction. If the input is slightly off (e.g., detecting 'H' and 'L' instead of "hello"), the app can auto-correct it to the intended word, improving accuracy.  
* **Sentence Formation:** Users can type or form full sentences using sign input.  
* **"Speak" Button:** Use the **Speak** button to have the generated text read aloud.  
* **"Clear" Button:** The **Clear** button resets the text area, allowing for fresh input.

[Watch the demo](https://drive.google.com/file/d/1jytnRHUC5LRaVTzNOSF7JQqRGuavR0mA/view?usp=sharing)

#### **Text to Sign Feature**

From the Homepage, click the **Text to Sign** button to open its respective window. This feature allows users to convert both typed text and spoken words into sign language.

* **Text Input:** Type a message (e.g., "Hello, I am Akshat") into the designated area.  
* **Speech Input:** Alternatively, you can record your voice by speaking naturally (e.g., "Hello, how are you doing?") into the microphone. The app will transcribe your speech into text.  
* **"Show Sign Language" Button:** After entering text or speaking, click the **Show Sign Language** button. The app will then display the corresponding sign language for your input.  
* **Multimodal Communication:** This feature enables efficient communication through sign language using both written and spoken input. (For a demonstration, please refer to demo\_3 if available.)

[Watch the demo](https://drive.google.com/file/d/1zZ_879s1-jEwlWzWnwgpfLHuZgPgwlKd/view?usp=sharing)

## **Technologies Used**

* Python  
* Kivy  
* OpenCV  
* Ultralytics (for YOLOv11)  
* YOLO (You Only Look Once)  
* SpeechRecognition  
* PyAudio  
* Pipwin
