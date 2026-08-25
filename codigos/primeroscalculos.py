#cargo las libreriaas

import geopandas as gpd
import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt

#leemos el vector

ruta_vector = "vectores/area_de_estudio.gpkg"
vector = gpd.read_file(ruta_vector)

# Imprimimos las primeras filas para ver que se cargó bien
print(vector.head())