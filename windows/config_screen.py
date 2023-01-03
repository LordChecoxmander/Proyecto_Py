import PySimpleGUI as sg
import os
import json


def crear_arch_config():
    """Crea el json de configuración con una configuración estándar inicial"""

    config = {'Tiempo': 60, 'Rondas': 5, 'Puntaje_sumar': 10, 'Puntaje_restar': 5,
              'Cant_pistas': {'Facil': 5, 'Normal': 3, 'Dificil': 2},
              'Datasets': {'Volcanes': True, 'Spotify': True, 'FIFA': True}
              }
    with open(os.path.join(os.path.dirname(__file__), '..', 'users', 'config.json'), 'w') as arch:
        json.dump(config, arch, indent=4)


def actualizar_config(values):
    """Actualiza la configuración en el json"""

    with open(os.path.join(os.path.dirname(__file__), '..', 'users', 'config.json'), 'r') as arch:
        config = json.load(arch)

    if values['-TIME-']:
        config['Tiempo'] = int(values['-TIME-'])
    if values['-ROUNDS-']:
        config['Rondas'] = int(values['-ROUNDS-'])
    if values['-WINSCORE-']:
        config['Puntaje_sumar'] = int(values['-WINSCORE-'])
    if values['-LOSESCORE-']:
        config['Puntaje_restar'] = int(values['-LOSESCORE-'])
    if values['-EASYCAR-']:
        config['Cant_pistas']['Facil'] = int(values['-EASYCAR-'])
    if values['-NORMALCAR-']:
        config['Cant_pistas']['Normal'] = int(values['-NORMALCAR-'])
    if values['-HARDCAR-']:
        config['Cant_pistas']['Dificil'] = int(values['-HARDCAR-'])
    if values['-VOLCANES-'] != config['Datasets']['Volcanes']:
        config['Datasets']['Volcanes'] = values['-VOLCANES-']
    if values['-SPOTIFY-'] != config['Datasets']['Spotify']:
        config['Datasets']['Spotify'] = values['-SPOTIFY-']
    if values['-FIFA-'] != config['Datasets']['FIFA']:
        config['Datasets']['FIFA'] = values['-FIFA-']

    with open(os.path.join(os.path.dirname(__file__), '..', 'users', 'config.json'), 'w') as arch:
        json.dump(config, arch, indent=4)


def verificar_config():
    """Verifica que la configuracion ingresada por el usuario no sea ilógica para el juego"""

    with open(os.path.join(os.path.dirname(__file__), '..', 'users', 'config.json'), 'r') as arch:
        config = json.load(arch)
        if config['Tiempo'] == 0 or True not in (list(config['Datasets'].values())):
            return False
    return True


def build():
    """Crea la ventana de configuración del juego"""

    sg.theme('LightBlue')
    fuente = 'Verdana', 11
    pad_st = 10, 8

    with open(os.path.join(os.path.dirname(__file__), '..', 'users', 'config.json'), 'r') as arch:
        config = json.load(arch)

    # construcción del área de configuraciones generales
    gen_txt = [
        [sg.Text('Tiempo límite por ronda (en segundos)',
                 font=fuente, pad=pad_st)],
        [sg.Text('Cantidad de rondas por juego', font=fuente, pad=pad_st)],
        [sg.Text('Puntaje sumado por cada respuesta correcta',
                 font=fuente, pad=pad_st)],
        [sg.Text('Puntaje restado por cada respuesta incorrecta',
                 font=fuente, pad=pad_st)],
    ]

    gen_opt = [
        [sg.InputCombo((30, 60, 90), default_value=config['Tiempo'],
                       size=(10, 1), pad=pad_st, key='-TIME-')],
        [sg.OptionMenu((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), default_value=config['Rondas'], size=(7, 1), pad=pad_st,
                       key='-ROUNDS-')],
        [sg.InputCombo([5, 10, 15], default_value=config['Puntaje_sumar'], size=(10, 1), pad=pad_st,
                       key='-WINSCORE-')],
        [sg.InputCombo([0, 5, 10], size=(10, 1), default_value=config['Puntaje_restar'], pad=pad_st,
                       key='-LOSESCORE-')]
    ]

    general = [
        [sg.Frame('Configuración general', [[
            sg.VPush(),
            sg.Column(layout=gen_txt, element_justification='l'),
            sg.Push(),
            sg.Column(layout=gen_opt, element_justification='r'),
            sg.VPush()
        ]], font=('Verdana', 13), size=(550, 180))]
    ]

    # construcción del área de selección de datasets
    datasets_opt = [
        [sg.Text('Elige al menos una', font=('Verdana', 10))],
        [sg.Checkbox('Erupciones volcanicas', default=config['Datasets']['Volcanes'],
                     enable_events=True, font=fuente, pad=pad_st, key='-VOLCANES-')],
        [sg.Checkbox('Spotify Top 100 2010-2019', default=config['Datasets']['Spotify'],
                     enable_events=True, font=fuente, pad=pad_st, key='-SPOTIFY-')],
        [sg.Checkbox('Jugadores FIFA 2021', default=config['Datasets']['FIFA'],
                     enable_events=True, font=fuente, pad=pad_st, key='-FIFA-')]
    ]

    datasets = [
        [sg.Frame('Categorías para jugar', layout=datasets_opt, font=('Verdana', 13),
                  pad=pad_st, size=(550, 180))]
    ]

    # construcción del área de configuraciones por nivel
    level_txt = [
        [sg.Text('Fácil', font=fuente, pad=pad_st)],
        [sg.Text('Normal', font=fuente, pad=pad_st)],
        [sg.Text('Difícil', font=fuente, pad=pad_st)]
    ]

    level_opt = [
        [sg.OptionMenu((1, 2, 3, 4, 5), default_value=config['Cant_pistas']['Facil'], size=(10, 1), pad=pad_st,
                       key='-EASYCAR-')],
        [sg.OptionMenu((1, 2, 3, 4), default_value=config['Cant_pistas']['Normal'], size=(10, 1), pad=pad_st,
                       key='-NORMALCAR-')],
        [sg.OptionMenu((1, 2, 3), default_value=config['Cant_pistas']['Dificil'], size=(10, 1), pad=pad_st,
                       key='-HARDCAR-')]
    ]

    level = [
        [sg.Frame('Cantidad de características a mostrar según el nivel', [[
            sg.Column(layout=level_txt, element_justification='l'),
            sg.Push(),
            sg.Column(layout=level_opt, element_justification='r')
        ]], font=('Verdana', 13), size=(550, 150))]
    ]

    # construcción del layout
    layout = [
        [sg.VPush()],
        [sg.Column(general, element_justification='c')],
        [sg.Column(level, element_justification='c')],
        [sg.Column(datasets, element_justification='c')],
        [sg.VPush()],
        [sg.Button('Volver', font=fuente, border_width=2, size=(10, 1), button_color=('black', 'white'),
                   key='-VOLVER-'),
         sg.Button('Aceptar', font=fuente, border_width=2, size=(10, 1), key='-OK-')]
    ]

    window = sg.Window('FiguRace *-* Configuración', layout, resizable=True, size=(600, 640), auto_size_buttons=True,
                       element_justification='c')

    while True:
        event, values = window.read()
        match event:

            case sg.WIN_CLOSED:
                window.close()
                break

            case '-OK-':
                try:
                    actualizar_config(values)
                    if verificar_config():
                        sg.popup('Configuración guardada con éxito', title='¡Hecho!', keep_on_top=True,
                                 font=fuente)
                        window.close()
                        break
                    else:
                        sg.popup('Por favor verifica tus opciones', title='¡Cuidado!', keep_on_top=True,
                                 font=fuente)
                except ValueError:
                    sg.popup('Por favor ingresa solo números en los campos solicitados.', title='¡Cuidado!',
                             keep_on_top=True, font=fuente)

            case '-VOLVER-':
                window.close()
                break
