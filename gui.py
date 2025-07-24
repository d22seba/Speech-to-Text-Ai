import PySimpleGUI as sg

layout = [
    [sg.Text("Gib etwas ein:")],
    [sg.Input(key='-EINGABE-')],
    [sg.Button("Absenden")],
    [sg.Text("", key='-AUSGABE-', size=(40,1))]
]

fenster = sg.Window("Einfache PySimpleGUI GUI", layout)

while True:
    event, values = fenster.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Absenden":
        text = values['-EINGABE-']
        fenster['-AUSGABE-'].update(f"Du hast eingegeben: {text}")

fenster.close()
