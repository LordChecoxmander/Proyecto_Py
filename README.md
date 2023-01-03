# Figurace -By Grupo 20

<p align="center" width="100%">
    <img  src="assets/logo.png" width="180" height="180">
</p>

Figurace es un proyecto desarrollado para la materia Seminario de Lenguajes de la Facultad de Informatica opcion Python de la Universidad Nacional de La Plata.

Este proyecto funciona tanto en Windows como en GNU/Linux donde el jugador puede ingresar como invitado o registrase con sus datos y seleccionar una dificultad para acceder a una partida que consiste en un juego de tarjetas, en el cual se debe adivinar el nombre de la misma entre varias opciones. Cuenta con tres dificultades y tres temas distintos procesados de una serie de datasets; en este juego se usaron volcanes, música y fútbol.

También existe una ventana de configuracion donde se pueden modificar algunos parametros de la partida; otra ventana donde se muestran dos tablas, la primera con los 20 mejores puntajes de cada dificultad y la segunda con los 20 mejores promedios por cada dificultad.



## Integrantes del grupo 20

```text
Mattei Juliana Edda            | Legajo ------> 17712/6
Cecconato Santiago Andres      | Legajo ------> 18340/1
Montes De Oca Fernando Nahuel  | Legajo ------> 16107/5
Pelli Isidro Emir              | Legajo ------> 15959/1
```

## Ejecución del juego

-En un principio se debe contar con python 3.10.2 o superior instalado de forma global en su pc o en un entorno virtual.

-Para instalar todas las librerias necesarias se debe ejecutar el siguiente comando en la terminal:

```python
    pip install -r requirements.txt
```

-Para comenzar a jugar se debe ejecutar el siguiente comando en la terminal:

```python
    python3 figurace.py
```

-Tambien se dispone de varias jupyter notebooks para poder procesar los distintos datasets.
Para ejecutar un jupyer notebook se debe abrir la terminal y escribir la siguiente instruccion estando posicionado en la carpeta del juego:

```python
    jupyter notebook
```

Al ejecutarse se abrira una pestaña en el navegador, allí busque la carpeta data sets y abra los archivos correspodientes a cada data set. Una vez dentro seleccione el boton ```run all cells```

## Sitios de  donde se obtuvieron cada data sets  

[Spotify](https://www.kaggle.com/datasets/muhmores/spotify-top-100-songs-of-20152019)

[Erupciones Volcanicas](https://public.opendatasoft.com/explore/dataset/significant-volcanic-eruption-database/table/)

[FIFA 2021 Complete Player Dataset](https://www.kaggle.com/datasets/aayushmishra1512/fifa-2021-complete-player-data?resource=download)
