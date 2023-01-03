import os

# path imagenes
PATH_IMAGES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets'))
PATH_FIFA_PNG = os.path.join(PATH_IMAGES, 'FIFA21.png')
PATH_ERUPCIONES_PNG = os.path.join(PATH_IMAGES, 'Erupciones-volcanicas.png')
PATH_SPOTIFY_PNG = os.path.join(PATH_IMAGES, 'Spotify_2.png')
PATH_CHECK_PNG = os.path.join(PATH_IMAGES, 'check.png')
PATH_NOTCHECK_PNG = os.path.join(PATH_IMAGES, 'not_check.png')

# path csv
PATH_DATASETS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data_sets'))
PATH_SPOTIFTY_CSV = os.path.join(PATH_DATASETS, 'New-Spotify-2010-2019-Top-100.csv')
PATH_ERUPCIONES_CSV = os.path.join(PATH_DATASETS, 'new-significant-volcanic-eruption-database.csv')
PATH_FIFA_CSV = os.path.join(PATH_DATASETS, 'New-FIFA-21-Complete.csv')

# path json
PATH_USERS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'users'))
PATH_CONFIG = os.path.join(PATH_USERS, 'config.json')
PATH_SCORES = os.path.join(PATH_USERS, 'scores.csv')

PATH_PARTIDAS = os.path.join(PATH_USERS, 'registro_partidas.csv')

GEN_FONT = 'Verdana', 12

PATHS = {"Volcanes": (PATH_ERUPCIONES_CSV, PATH_ERUPCIONES_PNG), "FIFA": (PATH_FIFA_CSV, PATH_FIFA_PNG),
         "Spotify": (PATH_SPOTIFTY_CSV, PATH_SPOTIFY_PNG)}
