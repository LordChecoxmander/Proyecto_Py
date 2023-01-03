from uuid import uuid4
from scripts.gamescreen.scripts import *


def build(user, dificultad):
    """ Construyo la ventana de juego"""

    sg.popup("¡Bienvenido!",
             "El juego consiste en que encuentres la opción correcta entre las dadas en la botonera",
             "Guíate por las pistas que te daremos.",
             "Presta atención al tiempo. Cuando presiones 'Comenzar' el tiempo empezará a correr.",
             "¡Que no se te acabe!",
             "¡Mucha suerte!", custom_text='Comenzar')

    config = get_config()
    csv_selected, header, data = get_card_data()
    genero = get_genero(user)
    num_carta = randrange(len(data))  # obtengo carta a jugar aleatoriamente
    puntaje = 0

    # Construccion de la ventana del juego
    sg.theme("LightBlue")

    # Columna izquierda resultado parcial
    col_left = create_col_result(csv_selected, user, puntaje)
    col_right = create_right_col(header, data, dificultad, num_carta)

    layout = [
        [sg.VPush()],
        [sg.Push(), sg.Column(col_left), sg.Push(),
         sg.Column(col_right), sg.Push()],
        [sg.VPush()]
    ]

    window = sg.Window("FiguRace *-* ¡A jugar!", layout,
                       resizable=True, size=(700, 640), auto_size_buttons=True)
    img_act = []
    carta_buena = data[num_carta][5]
    start_time = time()
    time_y_punt = [start_time, puntaje, carta_buena]
    id_partida = uuid4()
    guardar_info(int(time()), id_partida, "inicio_partida", user,
                 "", "-", "-", dificultad, genero)

    while True:

        if len(img_act) != config['Rondas']:
            event, values = window.read(timeout=250, timeout_key='-TIMEOUT-')
            match event:

                case sg.WIN_CLOSED:
                    guardar_info(time(), id_partida, "cancelada", user,
                                 "cancelada", "-", "-", dificultad, '')
                    break

                case '-VOLVER-':
                    guardar_info(time(), id_partida, "cancelada", user,
                                 "cancelada", "-", "-", dificultad, '')
                    window.close()
                    break

                # countdown
                case '-TIMEOUT-':
                    countdown(window, time_y_punt, config, data,
                              dificultad, img_act, id_partida, user, genero, csv_selected, header)

                case _:
                    if window[event].get_text() == carta_buena:
                        guardar_info(int(time()), id_partida, "intento", user, "ok", window[event].get_text(), carta_buena,
                                     dificultad, genero)
                        window[f'-IMG_{len(img_act) + 1}-'].update(PATH_CHECK_PNG)
                        img_act.append(True)
                        time_y_punt[1] += config['Puntaje_sumar']
                        window['-PUNTAJE-'].update(
                            f'Puntos acumulados: {time_y_punt[1]}')
                        carta_buena = data[window_update(
                            window, dificultad, csv_selected, header, data)][5]
                        time_y_punt[0] = time()

                    else:  # si llega aca carta perdida
                        guardar_info(int(time()), id_partida, "intento", user, "error", window[event].get_text(),
                                     carta_buena, dificultad, genero)
                        window[f'-IMG_{len(img_act) + 1}-'].update(PATH_NOTCHECK_PNG)
                        img_act.append(False)
                        time_y_punt[1] -= config['Puntaje_restar']
                        window['-PUNTAJE-'].update(
                            f'Puntos acumulados: {time_y_punt[1]}')
                        carta_buena = data[window_update(
                            window, dificultad, csv_selected, header, data)][5]
                        time_y_punt[0] = time()

        else:
            if time_y_punt[1] <= 0:
                time_y_punt[1] = 0
            sg.popup("No puedes seguir jugando",
                     "Puntaje obtenido: ", f'{time_y_punt[1]}', keep_on_top=True)
            guardar_puntaje(user, dificultad, time_y_punt[1])
            guardar_info(int(time()), id_partida, "fin", user,
                         "finalizada", "", "", dificultad, genero)
            window.close()
            break
