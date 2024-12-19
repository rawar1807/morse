from pydub import AudioSegment
from pydub.playback import play
from time import sleep
import PySimpleGUI as sg
import os
import sys

def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
dot_file = resource_path('dot.wav')

# Check if the file exists
if os.path.exists(dot_file):
    print(f"File found: {dot_file}")
else:
    print(f"File not found at: {dot_file}")


encode_table = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    " ": "SPACE",
}
decode_table = {v: k for k, v in encode_table.items()}
def encode(s):
    s=s.upper()
    enc = " ".join(encode_table[x] for x in s)
    return enc.replace(" SPACE ", "   ")
def decode(encoded):
    symbols = encoded.replace("   ", " SPACE ").split(" ")
    return "".join(decode_table[x] for x in symbols)
def play_morse_code(morse_code):
    dot_sound = AudioSegment.from_file("dot.wav")
    dash_sound = AudioSegment.from_file("dash.wav")
    for symbol in morse_code:
        if symbol == ".":
            play(dot_sound)
        elif symbol == "-":
            play(dash_sound)
        elif symbol == " ":
            sleep(0.2)
        elif symbol == "   ":
            sleep(0.6)
layout = [
    [sg.Text("Scrie textul sau codul Morse:")],
    [sg.InputText(key="-INPUT-", size=(50, 1))],
    [sg.Button("Codifica"), sg.Button("Decodifica"), sg.Button("Play"), sg.Button("Exit")],
    [sg.Text("Output:"), sg.Text("", size=(50, 1), key="-OUTPUT-")]
]
window = sg.Window("Codificator/Decodificator Morse", layout)
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    user_input = values["-INPUT-"]
    if event == "Codifica":
        output = encode(user_input)
        window["-OUTPUT-"].update(output)
    elif event == "Decodifica":
        output = decode(user_input)
        window["-OUTPUT-"].update(output)
    elif event == "Play":
        encoded = encode(user_input)
        if encoded:
            sg.popup("Playing Morse Code: " + encoded)
            play_morse_code(encoded)
window.close()
while True:
    print("\nCodificator/Decodificator Morse")
    print("1. Codifica textul in codul Morse")
    print("2. Decodifica codul Morse in text")
    print("3. Codifica textul in cod morse si da-i play")
    print("4. Exit")
    choice = input("Alege (1/2/3/4): ")
    if choice == "1":
        text = input("Scrie textul de codificat: ").upper()
        print("Cod Morse:", encode(text))
    elif choice == "3":
        text = input("Scrie textul si asculta codul: ").upper()
        encoded = encode(text)
        print("Playing Morse Code:", encoded)
        play_morse_code(encoded)
    elif choice == "2":
        morse_code = input("Scrie codul Morse de decodificat. ")
        try:
            print("Text decodificat", decode(morse_code))
        except KeyError:
            print("Eroare:Text invalid")
    elif choice == "4":
        break
    else:
        print("Alegere invalida. Alege 1,2,3,4")
