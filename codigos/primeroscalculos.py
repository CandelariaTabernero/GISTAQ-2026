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

# Lectura del raster. Apuntamos a la ruta exacta de la banda verde dentro de la carpeta raster
ruta_banda3 = "raster/LC08_L2SP_226079_20260125_20260130_02_T1/LC08_L2SP_226079_20260125_20260130_02_T1_SR_B3.TIF"

# Abrimos el archivo con rasterio (usamos 'rio' porque así lo importamos arriba)
with rio.open(ruta_banda3) as dataset:
    print("¡Raster abierto con éxito!") #feedback visual
    print("Ancho de la imagen (píxeles):", dataset.width)
    print("Alto de la imagen (píxeles):", dataset.height)
    print("Sistema de coordenadas (CRS):", dataset.crs)

from rasterio.mask import mask

# 1. Abrimos la banda verde de Landsat
ruta_banda3 = "raster/LC08_L2SP_226079_20260125_20260130_02_T1/LC08_L2SP_226079_20260125_20260130_02_T1_SR_B3.TIF"

with rio.open(ruta_banda3) as src:
    
    # 2. Convertimos el vector al mismo sistema de coordenadas (CRS) que la imagen
    vector_reproyectado = vector.to_crs(src.crs)
    
    # 3. Extraemos la geometría ya transformada
    geometria_vector = vector_reproyectado.geometry
    
    # 4. Ahora sí, recortamos la imagen usando el molde adaptado
    imagen_recortada, transform_out = mask(src, geometria_vector, crop=True)
    
    print("¡Recorte realizado con éxito!")
    print("Nueva forma (shape) de la matriz recortada:", imagen_recortada.shape)