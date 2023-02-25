#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/tema6_analisis_multivariante.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Análisis multivariante

# * Vamos a explorar algunas posibilidades de análisis de datos de calidad del aire que ofrece Python. 
# * Usaremos como hasta ahora datos meteorológicos de AEMET y de contaminación de la Comunidad de Madrid.

# ###1. Copia del repositorio de datos
# ---

# Descargamos el repositorio de código y datos para trabajar más cómodamente:

# In[ ]:



# * Importamos las extensiones que vamos a necesitar. 
# 
# * Para simplificar la tarea hemos empaquetado las funciones de lectura de datos en un fichero independiente (lectura_de_datos.py) 

# In[ ]:


import lectura_de_datos                                   # lee ficheros de datos meteorológicos y de contaminación de Madrid
import matplotlib.pyplot as plt                           # dibujo de gráficos
from matplotlib.dates import MonthLocator, DateFormatter  # formato de fechas 
from scipy import stats                                   # cálculo estadístico
import numpy as np                                        # matrices
import pandas as pd                                       # dataframes
import seaborn as sns


# ###2. Inventario de magnitudes
# ---

# * Por conveniencia, hemos introducido en "lectura_de_datos.py" el inventario de estaciones de medida de la contaminación.
# 
# * Listamos los campos: código | municipio | nombre
# 
# 

# In[ ]:


# Simplemente escribimos el nombre de la variable para listar las estaciones
# -----------------------------------------------------------------------------
lectura_de_datos.estalist_com


# In[ ]:


# Simplemente escribimos el nombre de la variable para listar los contaminantes
# -----------------------------------------------------------------------------
lectura_de_datos.maglist_com


# In[ ]:


# Simplemente escribimos el nombre de la variable para listar los parámetros meteorológicos
# -----------------------------------------------------------------------------
lectura_de_datos.maglist_meteo


# ###3. Carga de datos
# ---

# * Vamos a cargar datos de algunas magnitudes para estudiar posibles relaciones:
# 

# In[ ]:


# Ejemplo con datos de contaminación
# ----------------------------------
anio = 2021
col1 = 'PM2.5'
col2 = 'PM10'
col3 = 'NO2'

df1, magnitud1, unidades1, estacion = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio,
                                     codigo_magnitud = 9,          # PM2.5
                                     codigo_estacion = 28065014    # Getafe
                                     ) 
df2, magnitud2, unidades2, estacion = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio,
                                     codigo_magnitud = 10 ,        # PM10
                                     codigo_estacion = 28065014    # Getafe
                                     ) 
df3, magnitud2, unidades2, estacion = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio,
                                     codigo_magnitud = 8,        # NO2
                                     codigo_estacion = 28065014    # Getafe
                                     ) 

# Asignamos un nombre significativo a la columna 'valor'
# -------------------------------------------------------
df1.rename(columns={'valor':col1}, inplace=True)
df2.rename(columns={'valor':col2}, inplace=True)
df3.rename(columns={'valor':col3}, inplace=True)

# Fusionamos las series de datos en un mismo dataframe
# --------------------------------------------------------
dlist = (df1,df2,df3)
df = dlist[0]
for d in dlist[1:] :
    df = df.merge(d,left_index=True, right_index=True)
print(df)


# ###4. Matriz de dispersión
# ---

# * Usamos la función pairplot de la extensión seaborn
# * Vamos a echar un vistazo a los datos representados unos respecto a otros
# * En la diagonal se presenta el histograma de cada variable

# In[ ]:


sns.pairplot(df, height=5)
plt.show()


# * Vamos a añadir a nuestro dataframe una columna que contenga la estación del año del dato
# * Usaremos el criterio estándar:
#  * Primavera: Marzo-Abril-Mayo
#  * Verano: Junio-Julio-Agosto
#  * Otoño: Septiembre-Octubre-Noviembre
#  * invierno: Diciembre-Enero-Febrero
# 

# In[ ]:


# Creamos un diccionario que atribuye al ordinal de cada mes
# la estación del año a que corresponde
# ------------------------------------------------------------
est = {1:'invierno',2:'invierno',3:'primavera',
       4:'primavera',5:'primavera',6:'verano',
       7:'verano',8:'verano',9:'otoño',
       10:'otoño',11:'otoño',12:'invierno'}

# Creamos una columna nueva llamada 'estacion' a la que 
# asignamos el número del mes       
# -------------------------------
df['estacion'] = df.index.month

# Reasignamos el número del mes a la estación correspondiente
# ------------------------------------------------------------
df['estacion'] = df['estacion'].apply(lambda x : est[x])


# * Volvemos a ejecutar pairplot, ahora con la opción 'hue' para que distinga las estaciones
# * Para eliminar los gráficos redundantes podemos usar la opción 'corner'
# * Los rangos en los ejes pueden ajustarse individualmente

# In[ ]:


# Llamada a pairplot
z = sns.pairplot(df, 
             hue='estacion', 
             height=3, 
             # Tamaño de los marcadores
             # -----------------
             #plot_kws={"s": 15},
             #
             # Tipo de histograma
             # kde o hist
             # ---------------------
             kind="kde", 
             corner = True
             )

# Modificación de los rangos
# -------------------------------
# Esquina inferior izquierda
# -------------------------------
z.axes[0,0].set_xlim((0,50))
z.axes[0,0].set_ylim((0,125))

# Dibujo
# ----------
plt.show()


# * También podemos optar por combinaciones de diagramas de dispersión con isolíneas de densidad de puntos

# In[ ]:


z = sns.pairplot(df, 
                 height = 5,
                 diag_kind="kde"
                 )
z.map_lower(sns.kdeplot, 
            levels=4, 
            color="red"
            )
plt.show()


# ###5. Dispersión con histogramas laterales
# ---

# * Para obtener digramas de dispersión con histogramas laterales recurrimos a la función jointplot

# In[ ]:


# Invocamos la función jointplot
# -----------------------------------
sns.jointplot(data=df, 
              x=col1, 
              y=col2, 
              hue = 'estacion',              
              #kind = 'kde',   # kde o reg
              #xlim = (0,60),
              #ylim = (0,100),              
              )

# Mostrar dibujo
# ---------------
plt.show()


# * Veamos un ejemplo con datos sintéticos
# * Construimos dos series de distribución normal
# * La primera (A) con media 100
# * La segunda (B) con media 0

# In[ ]:


# Creamos dos series aleatorias de distribución normal (gausiana)
# ----------------------------------------------------------------
# Media=100, varianza=10
# -----------------------
x = np.random.rayleigh(scale=1,size=1000)
# Media=0, varianza=10
# -----------------------
y = np.random.rayleigh(scale=1,size=1000)

# Creamos una tabla (dataframe) vacío
# ------------------------------------
df0 = pd.DataFrame()

# Insertamos nuestras series en la tabla
# como columnas A y B
# --------------------
df0['A'] = x
df0['B'] = x + y

df0['clase'] = df0['B'].apply(lambda w: '%d' % w)
print(df0)

# Dibujamos sus histogramas
# ---------------------------
df0.hist(bins=20)

sns.jointplot(data=df0, 
              x="A", 
              y="B", 
              hue="clase",   # no reg
              #kind = 'reg'   # kde o reg
              )
plt.show()


# ###6. Heatmaps
# ---

# * Otra presentación popular para datos multivariables son los llamados 'heatmaps'
# * Para ver un ejemplo, usaremos los datos de radiación solar de todas las estaciones de nuestra base de datos

# In[ ]:


anio = 2022

# Creamos una lista vacía para nuestros datos
# -------------------------------------------
dlist =[]

# Bucle que recorre todas las estaciones
# --------------------------------------
for idx in lectura_de_datos.estalist_com:

  # Lee los datos de cada estación
  # ---------------------------------
  print(idx,lectura_de_datos.estalist_com[idx][1])
  df, mag, uni, est = lectura_de_datos.meteo(
                                    '../datos/meteo/%s.csv' % anio,
                                     codigo_magnitud = 88,          
                                     codigo_estacion = idx) 
  
  # Sustituye la columna 'valor' por el nombre de la estación
  # ----------------------------------------------------------
  df.rename(columns={'valor':lectura_de_datos.estalist_com[idx][1]}, inplace=True)

  # Añade los datos de esta estación a la lista
  # --------------------------------------------
  dlist.append(df)

# La primera estación de la lista
# ----------------------------------
df = dlist[0]

# Fusiona los datos de todas las estaciones en una única tabla
# -------------------------------------------------------------
for d in dlist[1:] :
    df = df.merge(d,left_index=True, right_index=True)

# Muestra el resultado
# --------------------    
print(df)



# * Presentación del "heatmap"
# 
# 

# In[ ]:


# Agrupamos los datos por meses y calculamos la media
# ----------------------------------------------------
w = df.groupby(df.index.month).mean()

# Dimensionamos un gráfico
# -------------------------
fig, ax = plt.subplots(figsize=(12,12))

# Generamos el "heatmap"
# ------------------------
sns.heatmap(w, annot=True, fmt='.0f',ax=ax)

# Ponemos un título
# ------------------
ax.set_title('%s   -   Media mensual    -    %s (%s)' % (anio,mag,uni))

# Mostramos el dibujo
# ----------------------
plt.show()


# ###7. Resumen
# ---

# * En este notebook hemos explorado algunas posibilidades que permiten identificar relaciones entre múltiples variables
# * En general se trata de un análisis complejo
# * Hemos dibujado matrices de dispersión, con y sin clases.
# * Hemos generado diagramas de dispersión con histogramas laterales.
# * Hemos realizado un ejemplo de heatmap.
