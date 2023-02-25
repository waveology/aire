#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/tema2_funciones_y_presentaci%C3%B3n_de_datos.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Funciones y presentación de datos

# * En este notebook empaquetaremos las instrucciones del preproceso de datos que hemos visto anteriormente en una función
# * De esa manera podemos darle más versatilidad en su uso.

# ###2. Definición de la función de preproceso
# ---
# 

# En Python, las funciones se definen con la instrucción ***def***, anidando instrucciones en un bloque:

# In[ ]:


# Definimos una función que realiza el preproceso que se describe en el anterior notebook
# ----------------------------------------------------------------------------------------
def obtener_datos(anio=2023, magnitud=8, estacion=14, municipio=65) :
   """
   Lee el contenido de un fichero anual de datos de contaminación, selecciona
   los que corresponden a una estación y a una magnitud deseada.
   Devuelve los datos en una tabla 
   """

   # Importamos la extensión Pandas
   # --------------------------------
   import pandas as pd


   # Lee el fichero de datos
   # -----------------------
   fichero = '../datos/contaminacion/%s.csv' % anio
   df = pd.read_csv(fichero,  
                 sep=';', 
                 decimal=',')
   
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
   
   # Devuelve la tabla con los resultados
   # --------------------------------------
   return df


# ###2. Invocar la función de preproceso
# ---

# * Seleccionamos, por ejemplo, el año 2022
# * Seleccionamos el contaminante NO$_{2}$
# * Y elegimos dos estaciones, la de Guadalix de la Sierra y la de Getafe.

# In[ ]:


# Selección del año de los datos
# -------------------------------
anio = 2022

# Leemos los datos de NO2 de Getafe en 2022
# ---------------------------------------
no2_getafe   = obtener_datos(anio=anio, magnitud=8, estacion=14, municipio=65)

# Leemos los datos de NO2 de Guadalix de la Sierra en 2022
# ---------------------------------------------------------
no2_guadalix = obtener_datos(anio=anio, magnitud=8, estacion=1,  municipio=67)


# * Vemos que los datos están ya formateados en dos columnas, una con el tiempo y otra con la concentración de contaminante:

# In[ ]:


# Echamos un vistazo a las dos tablas obtenidas
# ---------------------------------------------
print(no2_getafe)
print(no2_guadalix)


# ###3. Presentación de series
# ---
# 

# Generamos graficos para ambos registros como ya hemos visto anteriormente usando las capacidades gráficas de Pandas:

# In[ ]:


no2_getafe.plot(
        fontsize=12,
        figsize=(15,10),
        marker='o',
        ms=5,
        lw=1,
        grid=True,
        legend=False,
        title = 'Concentración de NO$_{2}$ ($\mu$g/m$^{3}$) medida en la estación de Getafe'
        )

no2_guadalix.plot(
        fontsize=12,
        figsize=(15,10),
        marker='o',
        ms=5,
        lw=1,
        grid=True,
        legend=False,
        title = 'Concentración de NO$_{2}$ ($\mu$g/m$^{3}$) medida en la estación de Guadalix de la Sierra'
        )


# Para determinados ajustes será necesario recurrir a la extensión Matplotlib:

# In[ ]:


# Importamos la extensión de gráficos Matplotlib
# -----------------------------------------------
import matplotlib.pyplot as plt

# Creamos una figura para nuestro gráfico
# -----------------------------------------
fig,ax = plt.subplots(figsize=(15,10))

# Dibujamos AMBAS series temporales en el mismo gráfico:
# --------------------------------------------------------
ax.plot(no2_getafe.index, no2_getafe.valor, marker='o', ms=5, lw=1, color='blue',label='Getafe')
ax.plot(no2_guadalix.index, no2_guadalix.valor, marker='o', ms=5, lw=1, color='red',label='Guadalix')

# Añadimos una rejilla de fondo
# ------------------------------
ax.grid()

# Añadimos una leyenda que identifique cada estación
# -------------------------------------------------------
ax.legend()

# Dibuja
# --------
plt.show()


# ###4. Múltiples series
# ---
# 

# * Los gráficos que contienen varias series temporales en el mismo periodo de tiempo pueden resultar difíciles de interpretar. 
# * Podemos utilizar la función subplots para organizar nuestros gráficos de una forma más legible.

# In[ ]:


# Prepara el dibujo para presentar 1 columna de gráficos con dos 2 filas
# --------------------------------------------------------------------------
fig,ax = plt.subplots(
                       nrows = 2, 
                       ncols = 1, 
                       figsize=(14,7))

# Dibuja la serie de Getafe
# --------------------------
ax[0].plot(no2_getafe.index, no2_getafe.valor, marker='o', ms=5, lw=1, color='blue')
ax[0].set_title('Getafe',size=18)

# Dibuja la serie de Guadalix
# --------------------------
ax[1].plot(no2_guadalix.index, no2_guadalix.valor, marker='o', ms=5, lw=1, color='red')
ax[1].set_title('Guadalix',size=18)

# Genera un título de encabezado general
# ----------------------------------------
plt.suptitle('Concentración de NO$_{2}$ ($\mu$g/m$^{3}$)    -    Año %s' % (anio),size=20)

# Añade rejilla a ambos dibujos
# ------------------------------
for a in ax :
  a.grid(True)

plt.show()


# * Para extender el rango temporal de los datos, basta con leer los ficheros correspondientes y añadirlos al dibujo.

# In[ ]:


# Leemos las concentraciones de NO2 en Getafe en los años 2019 y 2020
# --------------------------------------------------------------------
no2_getafe_2019   = obtener_datos(anio=2019, magnitud=8, estacion=14,  municipio=65)
no2_getafe_2020   = obtener_datos(anio=2020, magnitud=8, estacion=14,  municipio=65)
no2_getafe_2021   = obtener_datos(anio=2021, magnitud=8, estacion=14,  municipio=65)


# In[ ]:


# Preparamos un único gráfico
# ----------------------------
fig,ax = plt.subplots(figsize=(15,10))

# Dibujamos todas las series en el mismo gráfico
# -----------------------------------------------
ax.plot(no2_getafe_2019.index, no2_getafe_2019.valor, marker='o', ms=3, lw=0, color='blue'   ,label='2019')
ax.plot(no2_getafe_2020.index, no2_getafe_2020.valor, marker='o', ms=3, lw=0, color='red'    ,label='2020')
ax.plot(no2_getafe_2021.index, no2_getafe_2021.valor, marker='o', ms=3, lw=0, color='green'  ,label='2021')
ax.plot(no2_getafe.index,      no2_getafe.valor,      marker='o', ms=3, lw=0, color='magenta',label='2022')

# Limitamos la escala de concentraciones
# ----------------------------------------
ax.set_ylim(0,225)

# Ponemos el título
# -------------------
ax.set_title('Evolución de la concentración de NO$_{2}$ ($\mu$g/m$^{3}$) en Getafe', size = 20)

# Añadimos una rejilla de fondo
# ------------------------------
ax.grid()

# Añadimos una leyenda para identificar las series
# -------------------------------------------------
ax.legend()

# Dibujo
# ---------
plt.show()


# * Comparemos estos resultados con los de otra ciudad como Móstoles:

# In[ ]:


no2_mostoles_2019   = obtener_datos(anio=2019, magnitud=8, estacion=5,  municipio=92)
no2_mostoles_2020   = obtener_datos(anio=2020, magnitud=8, estacion=5,  municipio=92)
no2_mostoles_2021   = obtener_datos(anio=2021, magnitud=8, estacion=5,  municipio=92)
no2_mostoles_2022   = obtener_datos(anio=2022, magnitud=8, estacion=5,  municipio=92)


# In[ ]:


# Preparamos un único gráfico
# ----------------------------
fig,ax = plt.subplots(figsize=(15,10))

# Dibujamos todas las series en el mismo gráfico
# -----------------------------------------------
ax.plot(no2_mostoles_2019.index, no2_mostoles_2019.valor, marker='o', ms=3, lw=0, color='blue'   ,label='2019')
ax.plot(no2_mostoles_2020.index, no2_mostoles_2020.valor, marker='o', ms=3, lw=0, color='red'    ,label='2020')
ax.plot(no2_mostoles_2021.index, no2_mostoles_2021.valor, marker='o', ms=3, lw=0, color='green'  ,label='2021')
ax.plot(no2_mostoles_2022.index, no2_mostoles_2022.valor, marker='o', ms=3, lw=0, color='magenta',label='2022')

# Limitamos la escala de concentraciones
# ----------------------------------------
ax.set_ylim(0,225)

# Ponemos el título
# -------------------
ax.set_title('Evolución de la concentración de NO$_{2}$ ($\mu$g/m$^{3}$) en Móstoles', size = 20)

# Añadimos una rejilla de fondo
# ------------------------------
ax.grid()

# Añadimos una leyenda para identificar las series
# -------------------------------------------------
ax.legend()

# Dibujo
# ---------
plt.show()


# ###6. Resumen
# ---
# 

# En este notebook hemos visto:
# 
# * Cómo se empaqueta una función de preprocesos de datos para un uso más versátil.
# * Como invocar la función con diferentes parámetros y acceder a los resultados.
# * Una introducción a la presentación gráfica de series temporales.
# * Cómo añadir elementos descriptivos a la representación.
# * Cómo enfocar la presentación de series múltiples en un único gráfico.
