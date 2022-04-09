import PySimpleGUI as sg


layout = [
            [sg.Image('casual_winter.png')],
         ]

window = sg.Window('Style Me', layout)
event, values = window.read()
window.close ()
