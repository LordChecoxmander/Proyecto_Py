import PySimpleGUI as sg
import json
import os


def getting_path():
    return os.path.join(os.getcwd(), 'users', 'users.json')


def modify_users_data(values):
    with open(getting_path(), 'r') as file:
        users = json.load(file)
    users[values['-NICK-']] = {'Edad': values['-EDAD-'],
                               'Genero': values['-GENERO-']}
    with open(getting_path(), 'w') as file:
        # Actualizo el contenido del json con el diccionario modificado
        json.dump(users, file, indent=4)


def build():
    """Construye la ventana de las perfiles"""
    # Variables utilizadas para tamaños
    generos = ['Masculino', 'Femenino', 'Otro']
    size_button = (8, 1)
    size_input = (30, 2)
    spc_btw_button = (40, 2)
    padding_text = (10, 8)
    sg.theme("LightBlue")
    fuente = 'Verdana', 11

    # Creacion de LayOut
    profile_txt = [
        [sg.Text("Nickname", pad=padding_text, font=fuente)],
        [sg.Text("Género", pad=padding_text, font=fuente)],
        [sg.Text("Edad", pad=padding_text, font=fuente)]
    ]

    profile_inputs = [
        [sg.Input(key='-NICK-', size=size_input, pad=padding_text)],
        [sg.OptionMenu(generos, pad=padding_text,
                       size=(10, 1), key='-GENERO-')],
        [sg.Spin([i for i in range(1, 110)], initial_value=0,
                 size=(5, 1), pad=padding_text, key='-EDAD-')]
    ]

    profile_ly = [
        [sg.Frame('Creacion/Edicion de perfil', [[
            sg.Column(layout=profile_txt, element_justification='l'),
            sg.Push(),
            sg.Column(layout=profile_inputs, element_justification='l')
        ]], font=('Verdana', 14), size=(550, 160))]
    ]

    layout = [
        [sg.VPush()],
        [sg.Column(profile_ly, element_justification='c')],
        [sg.VPush()],
        [sg.Button('Volver', font=fuente, border_width=2, size=size_button, button_color=('black', 'white'),
                   pad=spc_btw_button, key='-VOLVER-'),
         sg.Button('Borrar', font=fuente, border_width=2, size=size_button, button_color=('black', 'white'),
                   pad=spc_btw_button, key='-BORRAR-'),
         sg.Button('Aceptar', font=fuente, border_width=2, size=size_button, pad=spc_btw_button, key='-ACEPTAR-')]
    ]

    window = sg.Window("FiguRace *-* Perfiles", layout, resizable=False, size=(600, 300),
                       auto_size_buttons=True, element_justification='c')

    while True:
        # Inicio la ventana
        event, values = window.read()
        match event:
            case '-ACEPTAR-':
                # Verifico que los campos no esten vacios.
                try:
                    if values['-NICK-'] == '' or int(values['-EDAD-']) == 0 or values['-GENERO-'] == '':
                        sg.popup('Por favor complete todos los campos',
                                 title='Error')
                    else:
                        # Verifico que el que el nick sea valido
                        if values['-NICK-'] == 'Usuarios':
                            sg.popup('Nickname invalido', title='Error')
                            window['-NICK-'].update('')
                        else:
                            modify_users_data(values)
                            sg.popup('Perfil creado/modificado con exito')
                            window.close()

                except ValueError:
                    sg.popup('Por favor ingresa un número para la edad',
                             title='Error')

            case '-BORRAR-':
                # Actualizo el contenido de todos los espsacios para que no contengan nada.
                window['-NICK-'].update('')
                window['-EDAD-'].update(0)
                window['-GENERO-'].update('')

            case '-VOLVER-':
                window.close()
                break

            case sg.WIN_CLOSED:
                window.close()
                break
