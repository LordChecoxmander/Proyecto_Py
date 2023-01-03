from csv import reader

import pandas as pd
import PySimpleGUI as sg
import os


def build():
    """Construye la ventana de las puntuaciones"""
    sg.theme("LightBlue")

    path_csv = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'users'))
    path_scores = os.path.join(path_csv, 'scores.csv')

    scores_dicctionary = {'Facil': [], 'Normal': [], 'Dificil': []}
    headings_array = ["FACIL", "NORMAL", "DIFICIL"]
    headings_array2 = ["PROMEDIO FACIL", "PROMEDIO NORMAL", "PROMEDIO DIFICIL"]

    def load_score_dicctionary():
        """ funcion que lee el archivo csv y devuelve un diccionario con key: dificultad y value: lista de tuplas """
        try:
            with open(path_scores, 'r') as csv_file:
                csv_reader = reader(csv_file, delimiter=',')
                next(csv_reader)
                for row in csv_reader:
                    scores_dicctionary[row[1]].append((row[0], row[2]))
            return scores_dicctionary
        except FileNotFoundError:
            sg.popup("Juega algunas partidas para ver puntuaciones aquí ;).", title='¡Ups!', keep_on_top=True)
    load_score_dicctionary()

    def sort_scores(dicctionary):
        """ funcion que ordena los scores de mayor a menor en el dicionario"""
        for key in dicctionary:
            dicctionary[key].sort(key=lambda tup: int(tup[1]), reverse=True)
        return dicctionary

    sort_scores(scores_dicctionary)

    averages = {}

    def create_averages(dictionary):
        """ funcion que calcula el promedio de puntajes de cada usuario por dificultad"""
        for difficulty, scores in dictionary.items():
            mapping = {}
            for score in scores:
                player = score[0]
                points = score[1]
                mapping.setdefault(
                    player, {"total_points": 0, "games_played": 0})
                mapping[player]["total_points"] += int(points)
                mapping[player]["games_played"] += int(1)

            for player, data in mapping.items():
                averages.setdefault(difficulty, [])
                averages[difficulty].append(
                    (player, round(data["total_points"] / data["games_played"], 2)))

    create_averages(scores_dicctionary)

    # usando pandas se convierte el diccionario en un dataframe
    df = pd.DataFrame(scores_dicctionary.values()).fillna('-')

    df2 = pd.DataFrame(averages.values()).fillna('-')

    result2 = [list(x) for x in zip(*df.values)][0:20]

    result = [list(x) for x in zip(*df2.values)][0:20]

    layout1 = [
        [sg.Push(), sg.Button("Maximos", font="Verdana 11", border_width=2, size=(10, 1), key="-MAXIMOS-"), sg.Button("Promedio", font="Verdana 11",
                                                                                                                      border_width=2, size=(10, 1), key="-PROMEDIO-"), sg.Button("Volver", font="Verdana 11", border_width=2, size=(10, 1), key="-VOLVER-"), sg.Push()],
        [sg.Text("PUNTAJES MAXIMOS", key="-ACTUAL-")],
        [sg.Table(values=result2, headings=headings_array,
                  # background_color='light blue',
                  auto_size_columns=False,
                  display_row_numbers=False,
                  justification='center',
                  num_rows=20,
                  alternating_row_color='lightyellow',
                  key='-TABLE1-',
                  row_height=35)

         ]
    ]

    window = sg.Window("FiguRace *-* Puntajes", layout1, resizable=True,
                       size=(600, 640), auto_size_text=True, element_justification='center')

    while True:
        event, values = window.read()
        match event:

            case sg.WIN_CLOSED:
                break

            case "-MAXIMOS-":
                window['-TABLE1-'].update(values=result2)
                window['-ACTUAL-'].update("PUNTAJES MAXIMOS")

            case "-PROMEDIO-":
                window['-TABLE1-'].update(values=result)
                window['-ACTUAL-'].update("PUNTAJES PROMEDIO")

            case "-VOLVER-":
                window.close()
                break
