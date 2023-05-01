import PySimpleGUI as sg
import pyttsx4

engine = pyttsx4.init()

bw: dict = {'size': (7, 2), 'font': ('Franklin Gothic Book', 24), 'button_color': ("darkblue", "white")}
bt: dict = {'size': (7, 2), 'font': ('Franklin Gothic Book', 24), 'button_color': ("darkblue", "lightblue")}
bo: dict = {'size': (15, 2), 'font': ('Franklin Gothic Book', 24), 'button_color': ("darkblue", "lightblue"), 'focus': True}

pronunciations = {
    '*': 'times',
    '/': 'divided by',
    '-': 'minus',
    '+': 'plus',
    '.': 'point',
    '%': 'modulo'
}

operation = ""


def gui():
    sg.theme('DarkBlue1')

    layout = [
        [
            sg.Text(size=(16, 1), key='_OUT_', justification="right", background_color="black", text_color="white", font=("DIGITAL-7", 48),
                    relief="sunken"),
            sg.Button('PLAY', **bt)
        ],
        [
            sg.Button('C', key='_CLEAR_', **bt), sg.Button('CE', key='_CE_', **bt), sg.Button('%', **bt), sg.Button('/', **bt)
        ],
        [
            sg.Button('7', **bw), sg.Button('8', **bw), sg.Button('9', **bw), sg.Button('*', **bt)
        ],
        [
            sg.Button('4', **bw), sg.Button('5', **bw), sg.Button('6', **bw), sg.Button('-', **bt)
        ],
        [
            sg.Button('1', **bw), sg.Button('2', **bw), sg.Button('3', **bw), sg.Button('+', **bt)
        ],
        [
            sg.Button('0', **bw), sg.Button('.', **bw), sg.Button('=', key='_DISPLAY_', **bo)
        ]
    ]

    window = sg.Window('Calculator', layout)

    def replace():
        global operation
        for key, value in pronunciations.items():
            operation = operation.replace(key, value)

    def calculate():
        global operation
        number = str(eval(operation))
        number = number[:16]
        number = number.rstrip('0').rstrip('.')

        return number

    def reset():
        global operation
        if number != 0:
            operation = str(number)
        else:
            operation = ""

    def play():
        global operation
        replace()
        engine.say(operation)
        engine.say("Equals")
        engine.say(str(number))
        engine.runAndWait()

    # Event loop
    while True:

        global operation

        event, values = window.read()
        print(event, values)

        if event in (None, 'Exit'):
            break

        elif event == '_DISPLAY_':
            try:
                number = calculate()

                reset()
                window['_OUT_'].update(number)
            except:
                operation = ""
                window['_OUT_'].update("Syntax error")

        elif event == '_CLEAR_':
            operation = ""
            window['_OUT_'].update(0)

        elif event == '_CE_':
            operation = operation[:-1]
            window['_OUT_'].update(operation)

        elif event == 'PLAY':
            try:
                number = calculate()

                if operation != number:
                    play()

                elif operation == number:
                    engine.say(operation)
                    engine.runAndWait()

                reset()
                window['_OUT_'].update(number)
            except:
                engine.say("Alert! There is a syntax error")
                engine.runAndWait()

                operation = ""
                window['_OUT_'].update("Syntax error")

        else:
            if len(operation) < 16:
                operation += event
                window['_OUT_'].update(operation)

    window.close()


if __name__ == '__main__':
    gui()
