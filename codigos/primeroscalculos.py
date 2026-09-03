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

    
# LECTURA Y RECORTE DE LA BANDA 6 (Infrarrojo de onda corta - SWIR 1)

# Apuntamos a la ruta exacta de la Banda 6
ruta_banda6 = "raster/LC08_L2SP_226079_20260125_20260130_02_T1/LC08_L2SP_226079_20260125_20260130_02_T1_SR_B6.TIF"

with rio.open(ruta_banda6) as src6:
    # Recortamos usando la misma geometría del vector que ya transformamos antes
    imagen_recortada_b6, transform_b6 = mask(src6, geometria_vector, crop=True)
    
    print("¡Banda 6 recortada con éxito!")
    print("Nueva forma (shape) de la Banda 6:", imagen_recortada_b6.shape)


# LECTURA Y RECORTE DE LA BANDA 4 (Rojo)

ruta_banda4 = "raster/LC08_L2SP_226079_20260125_20260130_02_T1/LC08_L2SP_226079_20260125_20260130_02_T1_SR_B4.TIF"

with rio.open(ruta_banda4) as src4:
    # 1. Reproyectamos el vector al sistema de coordenadas de la banda 4
    vector_reproyectado_4 = vector.to_crs(src4.crs)
    
    # 2. Recortamos usando la máscara y el crop
    imagen_recortada_b4, _ = mask(src4, vector_reproyectado_4.geometry, crop=True)
    
    print("¡Banda 4 recortada con éxito!")
    print("Nueva forma (shape) de la Banda 4:", imagen_recortada_b4.shape)

# LECTURA Y RECORTE DE LA BANDA 5 (Infrarrojo cercano - NIR)

ruta_banda5 = "raster/LC08_L2SP_226079_20260125_20260130_02_T1/LC08_L2SP_226079_20260125_20260130_02_T1_SR_B5.TIF"

with rio.open(ruta_banda5) as src5:
    # 1. Reproyectamos el vector al sistema de coordenadas de la banda 5
    vector_reproyectado_5 = vector.to_crs(src5.crs)
    
    # 2. Recortamos usando la máscara
    imagen_recortada_b5, _ = mask(src5, vector_reproyectado_5.geometry, crop=True)
    
    print("¡Banda 5 recortada con éxito!")
    print("Nueva forma (shape) de la Banda 5:", imagen_recortada_b5.shape)

# LECTURA Y RECORTE DE LA BANDA 7 (Infrarrojo de onda corta 2 - SWIR 2)

ruta_banda7 = "raster/LC08_L2SP_226079_20260125_20260130_02_T1/LC08_L2SP_226079_20260125_20260130_02_T1_SR_B7.TIF"

with rio.open(ruta_banda7) as src7:
    # 1. Reproyectamos el vector al sistema de coordenadas de la banda 7
    vector_reproyectado_7 = vector.to_crs(src7.crs)
    
    # 2. Recortamos usando la máscara
    imagen_recortada_b7, _ = mask(src7, vector_reproyectado_7.geometry, crop=True)
    
    print("¡Banda 7 recortada con éxito!")
    print("Nueva forma (shape) de la Banda 7:", imagen_recortada_b7.shape)