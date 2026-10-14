import geopandas as gpd

def preparar_vector_puntos(ruta_entrada, ruta_salida, crs_objetivo="EPSG:32621"):
    """
    Carga el archivo vectorial de puntos, verifica su CRS,
    lo reproyecta al sistema de las imágenes Landsat y lo guarda.
    """
    # 1. Cargamos el archivo vectorial original
    puntos_gdf = gpd.read_file(ruta_entrada)
    print(f"CRS original del vector: {puntos_gdf.crs}")

    # 2. Verificamos y reproyectamos si no coincide
    if puntos_gdf.crs != crs_objetivo:
        puntos_gdf = puntos_gdf.to_crs(crs_objetivo)
        print(f"¡Vector reproyectado con éxito a {crs_objetivo}!")
    else:
        print(f"El vector ya se encontraba en el sistema de coordenadas {crs_objetivo}.")

    # 3. Guardamos el resultado procesado
    puntos_gdf.to_file(ruta_salida, driver="GeoJSON")
    print(f"Archivo guardado correctamente en: {ruta_salida}")
    
    return puntos_gdf

if __name__ == "__main__":
    # Definimos rutas relativas asumiendo que estás ejecutando desde la carpeta 'codigos'
    ruta_in = "vectores/puntos_2025.geojson"
    ruta_out = "vectores/puntos_2025_32621.geojson"
    
    # Ejecutamos la función
    puntos_procesados = preparar_vector_puntos(ruta_in, ruta_out)