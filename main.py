from flask import Flask, render_template
from deepgram import Deepgram
from dotenv import load_dotenv
import os
import asyncio
from aiohttp import web
from aiohttp_wsgi import WSGIHandler

from typing import Dict, Callable


load_dotenv()

app = Flask('aioflask')

dg_client = Deepgram(os.getenv('DEEPGRAM_API_KEY'))

async def process_audio(fast_socket: web.WebSocketResponse):
    async def get_transcript(data: Dict) -> None:
        if 'channel' in data:
            transcript = data['channel']['alternatives'][0]['transcript']
        
            if transcript:
                await fast_socket.send_str(transcript)

    deepgram_socket = await connect_to_deepgram(get_transcript)

    return deepgram_socket

async def connect_to_deepgram(transcript_received_handler: Callable[[Dict], None]) -> str:
    try:
        socket = await dg_client.transcription.live({'punctuate': True, 'interim_results': False})
        socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, transcript_received_handler)

        return socket
    except Exception as e:
        raise Exception(f'Could not open socket: {e}')

@app.route('/')
def index():
    return render_template('index.html')

async def socket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request) 

    deepgram_socket = await process_audio(ws)

    while True:
        data = await ws.receive_bytes()
        deepgram_socket.send(data)

  

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    aio_app = web.Application()
    wsgi = WSGIHandler(app)
    aio_app.router.add_route('*', '/{path_info: *}', wsgi.handle_request)
    aio_app.router.add_route('GET', '/listen', socket)
    web.run_app(aio_app, port=5555)

"""process_audio takes fast_socket as an argument, which will keep the connection open between the client and the Flask server. We also connect to Deepgram and pass in the get_transcript function. This function gets the transcript and sends it back to the client."""

"""connect_to_deepgram function creates a socket connection to deepgram, listens for the connection to close, and gets incoming transcript objects.
"""

""" # accepts a websocket connection between the server and the client 
# as long as the connection stays open, we will receive bytes and wait until we get a message from the client. """

""" # adds to endpoint listen to the socket function
# the equivalent of this is app.route in Flask """

    # calls a function process_audio and opens the conenction to Deepgram

    # while the server and browser connection stays open, we'll wait for messages and send data

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
            