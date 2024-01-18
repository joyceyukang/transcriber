from flask import Flask, render_template
from deepgram import Deepgram
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

dg_client = Deepgram(os.getenv('DEEPGRAM_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')








# import PySimpleGUI as sg
# import speech_recognition as sr

# sg.theme("DarkBlue14")
# sg.set_options(font=("Helvetica", 14))

# # create layout of GUI
# layout = [[sg.Text("speeach to Text")], [sg.Multiline(size=(70, 20), key="-OUTPUT-")], [sg.Button("Record", button_color=('white', 'gray'), border_width=10), sg.Button("Exit", button_color=("white", "red"), border_width=10)]]

# window = sg.Window("Speech to Text", layout)

# # Loop for events
# while True:
#     event, values = window.read()
#     if event == "Exit" or event == sg.WIN_CLOSED:
#         break
#     elif event == "Record":
#         # Initialize recognizer
#         r = sr.Recognizer()

#         # Record Audio
#         with sr.Microphone() as source:
#             audio = r.listen(source)
        
#         # Recognize speech using Google Search recognition
#         try:
#             text = r.recognize.google(audio)
#             window["-OUTPUT-"].update(text)
#         except sr.UnknownValueError:
#             window["-OUTPUT-"].update("Could not understand audio")
#         except sr.RequestError as e:
#             window["-OUTPUT-"].update("Error: {e}")

# window.close()
            