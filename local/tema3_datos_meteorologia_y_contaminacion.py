#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/tema3_datos_meteorologia_y_contaminacion.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Datos de meteorología y contaminación

# * En este notebook repetimos las operaciones vistas en el anterior pero en este caso, para el acceso a los [datos meteorológicos AEMET](https://datos.comunidad.madrid/catalogo/dataset/calidad_aire_datos_meteo_historico). 
# 
# * El inventario de contenidos se encuentra [aquí](https://datos.comunidad.madrid/catalogo/dataset/129bbaae-7fa3-4043-8fa8-14c2fbee2502/resource/e79693a5-97b9-4b38-9c1a-a8cf621d7f43/download/descripcion-fichero-open-data-meteorologico.pdf)

# ###1. Definición de la función 
# ---

# * La estructura de los datos es similar a la de los datos de contaminación que vimos en el Notebook anterior:

# In[ ]:


def obtener_datos(anio=2023, magnitud=8, estacion=14, municipio=65) :
   """
   Lee el contenido de un fichero anual de datos de contaminación, selecciona
   los que corresponden a una estación y a una magnitud deseada.
   Devuelve los datos en una tabla 
   """

   # Importamos la extensión Pandas para trabajar con tablas
   # -------------------------------------------------------------------------------
   import pandas as pd


   # Lee el fichero de datos
   # -----------------------
   fichero = '../datos/meteo/%s.csv' % anio
   df = pd.read_csv(fichero,  
                 sep=';', 
                 decimal='.')
   # Filtramos por magnitud, estación y municipio
   # --------------------------------------------      
   df = df[ (df['magnitud']  ==  magnitud) 
       &    (df['estacion']  == estacion) 
       &    (df['municipio'] == municipio)]

   # Eliminamos columnas no necesarias
   # -----------------------------------
   df = df.drop(columns=['provincia','municipio','estacion','punto_muestreo','magnitud'])

   # Pasamos la hora que está en columnas a datos en filas
   # ---------------------------------------------------------
   df1 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'h%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='valor'
                 )

   # Convertimos la cadena de texto con el dato horario a valor numérico
   # --------------------------------------------------------------------
   df1['hora'] = df1['hora'].apply(lambda x : int(x[1:]))

   # Pasamos la validez que está en columnas a datos en filas
   # ---------------------------------------------------------
   df2 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'v%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='flag'
                 )

   # Convertimos la cadena de texto con la validez del dato a valor numérico
   # ------------------------------------------------------------------------   
   df2['hora'] = df2['hora'].apply(lambda x : int(x[1:]))

   # Fusionamos ambos dataframes
   # ----------------------------
   df = df1.merge(df2)

   # Eliminamos los datos no válidos y eliminamos la columna de validez
   # -------------------------------------------------------------------
   df = df[df['flag'] == 'V'].drop(columns='flag')

   # Creamos una columna para el tiempo
   # -----------------------------------
   df['fecha'] = pd.to_datetime({'year':df.ano,'month':df.mes,'day':df.dia,'hour':df.hora})

   # Elimninamos columnas no necesarias
   # -------------------------------------
   df = df.drop(columns=['ano','mes','dia','hora'])

   # Reordenamos las columnas (no es necesario)
   df = df[['fecha','valor']]

   # Establecemos el tiempo como índice
   # ------------------------------------
   df.set_index(['fecha'],inplace=True)

   # Ordenamos los datos por tiempo creciente
   df.sort_index(inplace=True)
   
   #Info
   print('Leídos %d datos' % len(df))
   
   return df


# ###2. Invocando la función
# ---

# * Seleccionamos un año, una estación y una variable meteorológica:

# In[ ]:

    
# Elegimos el año 2022
# --------------------
anio = 2022

# Leemos la temperatura en dos estaciones, Getafe y Guadalix
# --------------------------------------------------------------
temperatura_getafe   = obtener_datos(anio=anio, magnitud=83, estacion=14, municipio=65)
temperatura_guadalix = obtener_datos(anio=anio, magnitud=83, estacion=1,  municipio=67)

# Leemos el viento en dos estaciones, Getafe y Guadalix
# --------------------------------------------------------------
viento_getafe        = obtener_datos(anio=anio, magnitud=81, estacion=14, municipio=65)
viento_guadalix      = obtener_datos(anio=anio, magnitud=81, estacion=1,  municipio=67)

# Leemos la radiación solar en dos estaciones, Getafe y Guadalix
# --------------------------------------------------------------
radiacion_getafe     = obtener_datos(anio=anio, magnitud=88, estacion=14, municipio=65)
radiacion_guadalix   = obtener_datos(anio=anio, magnitud=88, estacion=1,  municipio=67)


# * Representamos la evolución de las temperaturas en ambas estaciones a lo largo de 2022:

# In[ ]:


# Importamos la extensión de gráficos Matplotlib
# ------------------------------------------------
import matplotlib.pyplot as plt

# Definimos el gráfico en el que dibujaremos las dos series
# -----------------------------------------------------------
fig,ax = plt.subplots(figsize=(15,10))

# Dibujamos la serie de temperaturas de Getafe
# ----------------------------------------------
ax.plot(temperatura_getafe.index, temperatura_getafe.valor,     marker='o', ms=1, lw=0, color='black',label='Getafe')

# Dibujamos la serie de temperaturas de Guadalix
# ----------------------------------------------
ax.plot(temperatura_guadalix.index, temperatura_guadalix.valor, marker='o', ms=1, lw=0, color='red',label='Guadalix')

# Ponemos un título
# ------------------
ax.set_title('Evolución de la temperatura a 2 metros a lo largo del año 2022', size=20)

# Añadimos una rejilla de fondo
# ------------------------------
ax.grid()

# Añadimos una leyenda para distinguir las series
# ------------------------------------------------
ax.legend()

# Dibujo
# ----------
plt.show()


# ###3. Ajustes en la presentación de series múltiples
# ---

# * Para comparar visualmente varias series de datos puede ser más adecuado presentarlas en una rejilla.
# * En este ejemplo presentamos los datos de ambas estaciones en dos columnas.

# In[ ]:


# Dimensionamos el gráfico como 3 filas y 2 columnas
# ---------------------------------------------------
fig,ax = plt.subplots(nrows = 3, 
                      ncols = 2,
                      figsize=(16,7)
                      )

# Ahora ax es una matriz tal que:
# --------------------------------
#       ax[0,0] ----> temperatura en Getafe
#       ax[0,1] ----> temperatura en Guadalix
#       ax[1,0] ----> viento en Getafe
#       ax[1,1] ----> viento en Guadalix
#       ax[2,0] ----> radiación en Getafe
#       ax[2,1] ----> radiación en Guadalix

# Temperatura de Getafe
# -----------------------
ax[0,0].plot(temperatura_getafe.index, temperatura_getafe.valor,        marker='o', ms=1, lw=0, color='blue')
ax[0,0].set_title('Getafe     -     Temperatura ($\degree$C)')
ax[0,0].set_ylim(-7,42)

# Temperatura en Guadalix
# ------------------------
ax[0,1].plot(temperatura_guadalix.index, temperatura_guadalix.valor,    marker='o', ms=1, lw=0, color='blue')
ax[0,1].set_title('Guadalix     -     Temperatura ($\degree$C)')
ax[0,1].set_ylim(-7,42)

# Viento en Getafe
# ----------------
ax[1,0].plot(viento_getafe.index,      viento_getafe.valor,             marker='o', ms=1, lw=0, color='green')
ax[1,0].set_title('Getafe     -     Viento (m/s)')
ax[1,0].set_ylim(0,10)

# Viento en Guadalix
# -------------------
ax[1,1].plot(viento_guadalix.index,      viento_guadalix.valor,         marker='o', ms=1, lw=0, color='green')
ax[1,1].set_title('Guadalix     -     Viento (m/s)')
ax[1,1].set_ylim(0,10)

# Radiación en Getafe
# -------------------
ax[2,0].plot(radiacion_getafe.index,      radiacion_getafe.valor,       marker='o', ms=1, lw=0, color='red')
ax[2,0].set_title('Getafe     -     Radiación (W/m$^{2}$)')
ax[2,0].set_ylim(0,1300)

# Radiación en Guadalix
# ---------------------
ax[2,1].plot(radiacion_guadalix.index,      radiacion_guadalix.valor,   marker='o', ms=1, lw=0, color='red')
ax[2,1].set_title('Guadalix     -     Radiación (W/m$^{2}$)')
ax[2,1].set_ylim(0,1300)


# Importamos Numpy para usar la función ravel()
# ----------------------------------------------
import numpy as np


# Para recorrer la matriz como si fuera un vector
# ------------------------------------------------
for a in np.ravel(ax):
  # Asignamos una rejilla a cada gráfico
  # -------------------------------------
  a.grid(True)

# Ponemos un título general
# ---------------------------
plt.suptitle('Año 2022', size=20)

# Realiza ajustes automáticos para mejorar la visibilidad
# ---------------------------------------------------------
plt.tight_layout()

# Dibujo
# -----
plt.show()


# ###4. Resumen
# ---

# En este notebook hemos visto:
# 
# * Cómo aplicamos a los datos meteorológicos un tratamiento similar al de los datos de contaminación
# * Cómo presentar series múltiples de datos en matrices de gráficos
# * Cómo realizar el ajuste automático de posicionamiento y dimensiones
