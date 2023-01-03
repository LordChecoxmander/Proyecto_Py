import json
import csv
from csv import DictWriter
from random import choice, randrange
import PySimpleGUI as sg
from scripts.gamescreen.constant import *
from time import time
from windows.profile_screen import getting_path


def get_genero(usuarie):
    """Obtinene el genero de un usuario"""

    with open(getting_path(), 'r') as user:
        users = json.load(user)
    return users[usuarie]['Genero']


def get_config():
    """ Obtiene la información de configuración del usuario. """

    try:
        with open(PATH_CONFIG, 'r') as j:
            config = json.load(j)
        return config
    except FileNotFoundError:
        sg.PopupError("No se encontró el archivo de configuración.")


def select_csv():
    """ Selecciona un Data set aleatoriamente si esta en True"""

    config = get_config()
    return choice(list({key: value for key, value in config['Datasets'].items() if value}))


def get_card_data():
    """ Obtiene los headers y data del CSV seleccionado. """
    csv_selected = select_csv()
    with open(PATHS[csv_selected][0], 'r', encoding='utf-8') as reader:
        reader = csv.reader(reader, delimiter=',')
        header, data = next(reader), list(reader)

    return csv_selected, header, data


def create_col_result(clave_al, user, puntaje):
    """ Creacion de columna izquierda(categoria, resultado parcial y abandonar partida) """

    config = get_config()
    check = [[sg.Text(f'{index}- ', size=(4, 1)), sg.Image('', size=(15, 15), key=f'-IMG_{index}-')] for index in
             range(1, (config['Rondas'] + 1))]
    col_resultado_parcial = [
        [sg.Text(f"{user}")],
        [sg.Text(f'Puntos acumulados: {puntaje}', key='-PUNTAJE-')],
        [sg.Column(check)],
    ]

    col_left = [
        [sg.Text(f"-{clave_al}-", key='-TEXTO_DATA-',
                 pad=((65, 0), (0, 0)), font=GEN_FONT)],
        [sg.Image(PATHS[clave_al][1], key='-IMGDATA-')],
        [sg.Frame(f'{"Resultado Parcial"}', [[sg.Column(col_resultado_parcial)]], pad=((22, 0), (0, 0)),
                  font=GEN_FONT)],
        [sg.Button("Abandonar", font=GEN_FONT, border_width=2,
                   size=(18, 1), key="-VOLVER-")]
    ]

    return col_left


def otras_cartas(num_car, data):
    """retorna "cartas" aleatoria que no sea la que se esta jugando"""

    act_cards = [num_car]
    while len(act_cards) < 5:
        num = randrange(len(data) - 1)
        if data[num][5] not in [data[pos][5] for pos in act_cards]:
            act_cards.append(num)
    return act_cards


def select_randomly(opciones):
    """ Mezcla las cartas de forma aleatoria """

    rtas = []
    for i in range(5):
        index = choice(range(len(opciones)))
        rtas.append(opciones[index])
        del opciones[index]
    return rtas


def create_right_col(header, data, dificultad, num_carta):
    def datos_tarjeta(header, data, dificultad, num_carta):
        """ Retorna la cantidad de pistas con las que se haya configurado """

        config = get_config()
        cant = config['Cant_pistas'][dificultad]

        return [[sg.Text(f"{header[index]}: {data[num_carta][index]}", font=GEN_FONT, key=f'-HINT_{index}-')] for index
                in range(cant)]

    def generating_box(data, num_carta):
        """ Genero el box con las otras cartas """

        other_cards = otras_cartas(num_carta, data)
        other_cards.append(num_carta)
        cards = [[sg.Push(), sg.Button(f'{data[other_cards[index]][5]}', font=GEN_FONT, border_width=2, size=(30, 0),
                                       key=f'-CARTA_{index}-'),
                  sg.Push()] for index in range(1, 5)] + [[sg.Push(), sg.Button(f'{data[num_carta][5]}', font=GEN_FONT,
                                                                                border_width=2, size=(30, 0),
                                                                                key='-CARTA_5-'), sg.Push()]]
        return select_randomly(cards)

    box_tarjeta = [
        [sg.Column(datos_tarjeta(header, data, dificultad, num_carta),
                   size=(800, 150))],  # box de cantidad de pistas
        [sg.Text(f"{header[5]}: ")],
        [sg.Column(generating_box(data, num_carta))],  # box de pistas
        [sg.Push(), sg.Button("Pasar >", font=GEN_FONT,
                              border_width=2, size=(10, 0), key="-PASAR-")]
    ]

    col_right = [
        # -> determinar la dificultad
        [sg.Text(f'Nivel: {dificultad}', font=GEN_FONT)],
        # -> determinar el tiempo segun la dificultad o configuracion
        [sg.Push(), sg.Text("00:00", justification="center", key="-TIMER-", text_color='#ff0055', font=("Verdana", 12)),
         sg.Push()],
        [sg.Frame(f'Tarjeta {"1"}', [
                  [sg.Column(layout=box_tarjeta)]], font=GEN_FONT)],
    ]

    return col_right


def window_update(window, dificultad, csv_selected, header, data):
    """ Actualiza la ventana con la información de la carta actual """

    config = get_config()
    cant = config['Cant_pistas'][dificultad]

    # obtengo carta a jugar aleatoriamente
    num_carta = randrange(len(data) - 1)
    otras_cards = otras_cartas(num_carta, data)

    # retorna lista con el dato a encontrar
    cartas = [f'{data[otras_cards[index]][5]}' for index in range(
        len(otras_cards))]
    cartas = select_randomly(cartas)

    window['-TEXTO_DATA-'].update(f"-{csv_selected}-")
    window['-IMGDATA-'].update(PATHS[csv_selected][1])
    for index in range(cant):
        window[f'-HINT_{index}-'].update(
            f"{header[index]}: {data[num_carta][index]}")

    for index in range(1, 6):
        window[f'-CARTA_{index}-'].update(f'{cartas[index - 1]}')
    return num_carta


def countdown(window, time_y_punt, config, data, dificultad, img_act, id_partida, user, genero, csv_selected, header):
    """Controlador del countdown"""

    current_time = int(time() - time_y_punt[0])
    # tiempo restante = inicial -transcurrido
    elapsed_time = config['Tiempo'] - current_time
    if elapsed_time >= 10:
        window['-TIMER-'].update(value=f' {elapsed_time // 60}:{elapsed_time % 60}', font=('verdana', 13),
                                 text_color='#35F64F')
    elif elapsed_time >= 0:
        # -> solo cambio de color
        window['-TIMER-'].update(value=f' {elapsed_time // 60}:0{elapsed_time % 60}', font=('verdana', 13),
                                 text_color='#ff0055')
    else:
        # terminar ventana
        time_y_punt[1] -= config['Puntaje_restar']
        sg.popup('Tiempo terminado', title='Game Over', keep_on_top=True)
        window[f'-IMG_{len(img_act) + 1}-'].update(PATH_NOTCHECK_PNG)
        img_act.append(False)
        time_y_punt[2] = data[window_update(
            window, dificultad, csv_selected, header, data)][5]
        time_y_punt[0] = time()
        guardar_info(int(time()), id_partida, "intento", user,
                     "timeout", "-", time_y_punt[2], dificultad, genero)


def guardar_info(tiempo, id_partida, evento, user, estado, text, respuesta, nivel, genero):
    """Función que guarda la información de las partidas"""
    try:
        with open(PATH_PARTIDAS, 'r', newline='') as file:
            None
    except FileNotFoundError:
        crear_arch_partidas()
    finally:

        dic = {'timestamp': tiempo, 'id': id_partida, 'evento': evento, 'usuarie': user, 'estado': estado,
               'texto-ingresado': text, 'respuesta': respuesta, 'nivel': nivel, 'genero': genero}
        with open(PATH_PARTIDAS, 'a', newline='', encoding='utf-8') as file:
            dict_writer = DictWriter(file, fieldnames=dic.keys())
            dict_writer.writerow(dic)


def crear_arch_partidas():
    with open(PATH_PARTIDAS, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['timestamp', 'id', 'evento', 'usuarie', 'estado',
                      'texto-ingresado', 'respuesta', 'nivel', 'genero']
        wr = csv.DictWriter(file, fieldnames=fieldnames)
        wr.writeheader()


def guardar_puntaje(user, dificultad, puntaje):
    """Función que guarda el puntaje de las partidas"""
    try:
        with open(PATH_SCORES, 'r', newline='') as file:
            None
    except FileNotFoundError:
        crear_archivo_scores()
    finally:
        dic = {'usuarie': user, 'dificultad': dificultad, 'puntaje': puntaje}
        with open(PATH_SCORES, 'a', newline='', encoding='utf-8') as file:
            dict_writer = DictWriter(file, fieldnames=dic.keys())
            dict_writer.writerow(dic)


def crear_archivo_scores():
    """ crea el archivo scores"""

    with open(PATH_SCORES, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['usuarie', 'dificultad', 'puntaje']
        wr = csv.DictWriter(file, fieldnames=fieldnames)
        wr.writeheader()
