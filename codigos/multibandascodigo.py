import os 
import glob #os y glob se usan para buscar archivos en las carpetas y crear directorios automaticamente
import geopandas as gpd #permite leer y manipular archivos vectoriales
import rasterio as rio
from rasterio.mask import mask #ambas para abrir, leer, recortar y escribir archivos raster
import numpy as np #para manejas las matrices de pixeles y convertir los tipos de datos numericos

def procesar_raster_multibanda():
    print("Iniciando el proceso de creación del raster multibanda...")

    # 1. Cargar el vector oficial UTM (se utiliza para hacer el recorte del area de estudio en las bandas)
    ruta_vector = "vectores/area_de_estudio_utm.gpkg"
    print(f"Cargando vector desde: {ruta_vector}")
    vector = gpd.read_file(ruta_vector)

    # 2. Definir la carpeta de la escena actual de Landsat
    nombre_carpeta_escena = "LC08_L2SP_226079_20260125_20260130_02_T1"
    base_carpeta = f"raster/{nombre_carpeta_escena}/"

    # 3. Extraer automáticamente la fecha de adquisición (ej: '20260125')
    fecha_escena = nombre_carpeta_escena.split("_")[3] #.split y lo demas trocea el nombre de la carpeta usando los guiones bajos
    print(f"Fecha detectada para el archivo: {fecha_escena}")

    # 4. Crear la carpeta 'multibandas' en la raíz del proyecto si no existe
    carpeta_multibandas = "multibandas"
    os.makedirs(carpeta_multibandas, exist_ok=True)

    # 5. Buscar todas las bandas de reflectancia superficial disponibles
    patron_busqueda = os.path.join(base_carpeta, "*_SR_B*.TIF") #busca dentro de la carpeta todos los archivos que terminen asi y con sorted los ordena
    archivos_bandas = sorted(glob.glob(patron_busqueda))

    if not archivos_bandas: #revida que no haya una lista vacia que luego genere error
        print("Error: No se encontraron bandas con el patrón especificado.")
        return

    arrays_recortados = []
    meta_base = None
    transform_out = None

    print(f"Recortando {len(archivos_bandas)} bandas con el vector UTM...")
    
    # 6. Recortar cada banda iterativamente (al recortar las imagenes reducimos drasticamente su peso, y no analizamos de mas al pe2)
    for ruta_banda in archivos_bandas:
        with rio.open(ruta_banda) as src:
            out_image, out_transform = mask(src, vector.geometry, crop=True)
            
            if meta_base is None:
                meta_base = src.meta.copy()
                transform_out = out_transform
                
            arrays_recortados.append(out_image[0].astype(np.float32))

    print("¡Recorte de todas las bandas completado con éxito!")

    # 7. Actualizar los metadatos para el archivo multibanda definitivo
    meta_base.update({
        "driver": "GTiff",
        "height": arrays_recortados[0].shape[0],
        "width": arrays_recortados[0].shape[1],
        "transform": transform_out,
        "count": len(arrays_recortados), # Cantidad total de bandas recopiladas
        "dtype": 'float32'
    })

    # 8. Guardar el archivo multibanda final en la carpeta 'multibandas'
    ruta_salida = os.path.join(carpeta_multibandas, f"{fecha_escena}.tif")

    with rio.open(ruta_salida, 'w', **meta_base) as dst:
        for idx, arr in enumerate(arrays_recortados, start=1):
            dst.write(arr, idx)

    print(f"¡Éxito total! Archivo multibanda guardado en: {ruta_salida}")

if __name__ == "__main__":
    procesar_raster_multibanda()