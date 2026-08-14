import pandas as pd

DATOS = pd.read_csv(r"C:\Users\cande\OneDrive\Documentos\Python C\Proyectos-Python\tipos de datos\base_de_datos_lab.csv") #con copy path
print(DATOS)

DATOS_filtrados = DATOS[["fecha","param","valor"]]
print(DATOS_filtrados) #head() imprime las primeras filas, dentro del parentesis indico cuantas

ph = DATOS_filtrados[DATOS_filtrados["param"] == "ph"]
print(ph)

import matplotlib.pyplot as plt #pip matplotlib para descargar

promedios = ph.groupby("fecha")["valor"].mean().reset_index() #dentro de promedios se agrupa, y de ahi sale la fecha y valor medio

plt.plot(promedios["fecha"], promedios["valor"]) 
plt.title("pH vs fecha")
plt.show()

#hola