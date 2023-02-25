#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/tema5_tecnicas_de_regresion.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Técnicas de regresión de datos

# * Vamos a explorar algunas posibilidades de análisis de datos de calidad del aire que ofrece Python. 
# 
# * Usaremos, como hasta ahora datos, de libre acceso: 
#   * [meteorológicos de AEMET](https://https://datos.comunidad.madrid/catalogo/dataset/calidad_aire_datos_meteo_historico) 
#   * [de contaminación de la Comunidad de Madrid](https://https://datos.comunidad.madrid/catalogo/dataset/calidad_aire_datos_historico).

# ###1. Copia del repositorio de datos
# ---

# * Descargamos el repositorio de código y datos para trabajar más cómodamente:

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
from sklearn.linear_model import LinearRegression         # regresión
from sklearn.preprocessing import PolynomialFeatures      # regresión
from sklearn.metrics import mean_squared_error, r2_score  # regresión


# ###2. Inventario de magnitudes
# ---

# * Por conveniencia, hemos introducido en "lectura_de_datos.py" el inventario de estaciones de medida de la contaminación.
# * Listamos los campos: **código | municipio | nombre**

# In[ ]:


# Simplemente escribimos el nombre de la variable para visualizar su contenido
# -----------------------------------------------------------------------------
lectura_de_datos.estalist_com


# * Listamos los contaminantes registrados.
# * **código | magnitud | unidades**

# In[ ]:


# Simplemente escribimos el nombre de la variable para visualizar su contenido
# -----------------------------------------------------------------------------
lectura_de_datos.maglist_com


# * Y por último, la magnitudes meteorológicas
# * **código | magnitud | unidades**

# In[ ]:


# Simplemente escribimos el nombre de la variable para visualizar su contenido
# -----------------------------------------------------------------------------
lectura_de_datos.maglist_meteo


# ###3. Carga de datos
# ---

# * Vamos a cargar datos de **dos magnitudes** para estudiar posibles relaciones:
# 

# In[ ]:


# # Ejemplo con datos meteorológicos
# # --------------------------------
# anio = 2022
# col1 = 'temperatura'
# col2 = 'humedad'
# df1, magnitud1, unidades1,estacion1 = lectura_de_datos.meteo(
#                                     'datos/meteo/%s.csv' % anio,
#                                      codigo_magnitud = 83,        # Temperatura
#                                      codigo_estacion = 28092005   # Guadalix de la Sierra  
#                                      ) 
# df2, magnitud2, unidades2,estacion2 = lectura_de_datos.meteo(
#                                     'datos/meteo/%s.csv' % anio,
#                                      codigo_magnitud = 86 ,        # Humedad relativa
#                                      codigo_estacion = 28092005    # Guadalix de la Sierra  
#                                      ) 


# Ejemplo con datos de contaminación
# ----------------------------------
anio = 2021
col1 = 'pm2.5'
col2 = 'pm10'
df1, magnitud1, unidades1,estacion1 = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio,
                                     codigo_magnitud = 9,          # PM2.5
                                     codigo_estacion = 28065014    # Getafe
                                     ) 
df2, magnitud2, unidades2,estacion2 = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio,
                                     codigo_magnitud = 10 ,        # PM10
                                     codigo_estacion = 28065014    # Getafe
                                     ) 

# Asignamos un nombre significativo a la columna 'valor'
# -------------------------------------------------------
df1.rename(columns={'valor':col1}, inplace=True)
df2.rename(columns={'valor':col2}, inplace=True)

# Fusionamos ambas series de datos en un mismo dataframe
# --------------------------------------------------------
df = pd.merge(df1, df2, left_index=True, right_index=True)

print(df.describe())


# ###4. Visualización de series temporales
# ---

# * Echamos un vistazo a ambas series temporales para estimar visualmente si evolucionan siguiendo un mismo patrón

# In[ ]:


# Representamos ambas series en el mismo gráfico
# ----------------------------------------------
df.plot(
        marker='o',                                                               # Símbolo
        ms=1,                                                                     # Tamaño del símbolo
        lw=1,                                                                     # Grosor de líneas de conexión
        grid=True,                                                                # Rejilla
        figsize=(12,8),                                                           # Tamaño del gráfico
        legend=True,                                                              # Leyenda
        title='%s VS %s   -    %s  -  %s' % (magnitud2,magnitud1,estacion1,anio), # Titulo        
        xlabel= 'Tiempo',                                                         # Etiqueta X   
        ylabel= '%s' % (unidades2)                                                # Etiqueta Y   
        )
plt.show()

# # Desplazamiento (offset)
# # ---------------------------
# df1 = df.copy()
# df1['pm10'] = df1['pm10'] + 50
# df1.plot(grid=True,figsize=(12,8),title='Aquí, PM10 tiene un offset de 50 %s' % unidades1)
# plt.show()

# # Cada serie en un gráfico independiente
# # ---------------------------------------
# fig, ax = plt.subplots(nrows=2,ncols=1,figsize=(12,8))
# ax[0].plot(df[col1])
# ax[1].plot(df[col2])
# for a in ax :
#    a.grid(True)
#    a.set_ylim(0,200)
# plt.show()


# ###5. Comparación de series
# ---

# * Representamos una serie de datos respecto a la otra:

# In[ ]:


# Dibujamos la columna 1 (PM10) frente a la columna 2 (PM2.5)
# --------------------------------------------------------------
ax = df.plot(x=col1, y=col2,
    marker='o',                                           # Símbolo
    ms=3,                                                 # Tamaño del símbolo
    lw=0,                                                 # Grosor de líneas de conexión
    color='blue',                                         # Color
    grid=True,                                            # Rejilla
    figsize=(12,8),                                       # Tamaño del gráfico
    legend=False,                                         # Leyenda
    title='%s vs %s   -    %s  -  %s' % (magnitud2,magnitud1,estacion1,anio),                 # Titulo        
    xlabel= '%s %s' % (magnitud1,unidades1),              # Etiqueta X   
    ylabel= '%s %s' % (magnitud2,unidades2),              # Etiqueta Y   
    xlim=(0,125),
    ylim=(0,125)
)

# Para facilitar la comparación hacemos que los ejes tengan las mismas dimensiones
# ----------------------------------------------------------------------------------
ax.set_aspect('equal')

# Añadimos una línea en la diagonal
# ----------------------------------------------------------------------------------
ax.plot([0,125],[0,125], color='red', ls='--', lw=2)



# Dibujamos
# ---------
plt.show()


# ###6. Regresión a una recta
# ---

# * Vamos a buscar la expresión de la recta que ***describe*** el comportamiento conjunto de ambas variables
# * Creamos un modelo lineal para ajustar los datos

# * Antes que nada:

# In[ ]:


# Nuestros datos son leídos en filas 
# -----------------------------------
print('datos en fila ', np.array(df[col1]))

# Sin embargo las funciones que vamos a usar requieren
# que una de ellas tenga formato de columna
# -----------------------------------------
print('datos en columna ', np.array(df[col1]).reshape(-1,1))

# Por eso las redefinimos así:
# -----------------------------
x = np.array(df[col1]).reshape(-1,1)  # Convierte una fila en una columna
y = np.array(df[col2])


# * Ahora podemos continuar

# In[ ]:


# Definimos nuestro modelo de regresión
# ---------------------------------------
model     = LinearRegression().fit(x,y)

# Calculamos los valores resultantes del ajuste
# ----------------------------------------------
ajuste    = model.predict(x)


# * Representamos el resultado

# In[ ]:


# Definimos el dibujo
# ---------------------------------------
fig, ax = plt.subplots(figsize=(12,8))

# Dibujamos x respecto a y
# ------------------------------
ax.plot(x,y,
        marker = 'o',
        ms     =  3,
        lw     =  0,
        color  = 'blue'
        )

# Superponemos los valores calculados del ajuste
# -----------------------------------------------
ax.plot(x,ajuste, ls='-', lw=3, color='black')

# Fija los límites del gráfico
# ------------------------------
ax.set_xlim(0,125),
ax.set_ylim(0,125)        

# Añadimos una línea en la diagonal
# ----------------------------------------------------------------------------------
ax.plot([0,125],[0,125], color='red', ls='--', lw=2)

# Para facilitar la comparación hacemos que los ejes tengan las mismas dimensiones
# ----------------------------------------------------------------------------------
ax.set_aspect('equal')

# Añadimos una rejilla de fondo
# -------------------------------
ax.grid(True)

# Añadimos un título
# -------------------
ax.set_title('%s VS %s   -    %s  -  %s' % (magnitud2,magnitud1,estacion1,anio)) # Titulo        

# Añadimos etiquetas a los ejes
# -----------------------------
ax.set_xlabel('%s %s' % (magnitud1,unidades1))                                   # Etiqueta X   
ax.set_ylabel('%s %s' % (magnitud2,unidades2))                                   # Etiqueta Y 

# Dibujamos
# ---------
plt.show()  


# * La línea en negro sintetiza el mejor ajuste lineal a nuestra nube de puntos
# * Para cuantificar la calidad del ajuste se suele recurrir al llamado coeficiente de determinación $R^{2}$
# * $R^{2}$ toma valores entre cero (mal ajuste) y 1 (ajuste perfecto).

# In[ ]:


# Podemos calcular fácilmente el valor del coeficiente de determinación
# -----------------------------------------------------------------------
r2 = model.score(x,y)

# Mostramos en pantalla
# ------------------------
print('R\u00b2 = %f' % r2)


# * El valor en el que la recta de ajuste intercepta al eje y se obtiene mediante:

# In[ ]:


# Valor con el que la recta de ajuste intercepta al eje Y
# ----------------------------------------------------------
b = model.intercept_

# Mostramos en pantalla
# ---------------------
print('b = %f' % b)


# * Y también podemos obtener la pendiente de la recta:

# In[ ]:


# Pendiente de la recta de ajuste
# -----------------------------------
a = model.coef_

# Mostramos en pantalla
# ----------------------
print('a = %f' % a[0])


# * De manera que nuestra recta de ajuste viene dada por:
# 
# ### <center>$Y  = a * X + b$</center>
# 
# * Podemos incorporar esta información al gráfico:

# In[ ]:


# Expresión de la recta de ajuste en texto
# ------------------------------------------
info_ajuste  = 'Y = %.3f * X + %.3f\nR$^{2}=%.3f$' % (a,b,r2)

# Título para el gráfico
# ----------------------
titulo       = '\n%s VS %s   -    %s  -  %s\n%s' % (magnitud2,magnitud1,estacion1,anio,info_ajuste)

# Dimensionamos el gráfico
# -------------------------
fig, ax = plt.subplots(figsize=(12,8))

# Dibujamos los datos 
# -------------------
ax.plot(x,y,
        marker = 'o',
        ms     =  3,
        lw     =  0,
        color  = 'blue'
        )

# Fija los límites del gráfico
# ------------------------------
ax.set_xlim(0,125)
ax.set_ylim(0,125)        

# Añadimos una línea en la diagonal
# ----------------------------------------------------------------------------------
ax.plot([0,125],[0,125], color='red', ls='--', lw=2)

# Para facilitar la comparación hacemos que los ejes tengan las mismas dimensiones
# ----------------------------------------------------------------------------------
ax.set_aspect('equal')

# Dibujamos la recta de ajuste
# -----------------------------
ax.plot(x,ajuste, ls='-', lw=3, color='black')

# Ponemos una rejilla de fondo
# ----------------------------
ax.grid(True)

# Posicionamos el título
# -----------------------
ax.set_title(titulo, loc='center')                             # Titulo        

# Etiquetas para los ejes
# ------------------------
ax.set_xlabel('%s %s' % (magnitud1,unidades1))   # Etiqueta X   
ax.set_ylabel('%s %s' % (magnitud2,unidades2))   # Etiqueta Y 

# Dibujo
# --------
plt.show()  


# ###7. Regresión a un polinomio
# ---

# * Una línea recta puede no ser el mejor ajuste para determinados conjuntos de datos
# * Podemos aumentar los grados de libertad del ajuste usando funciones que admitan diferentes grados de curvatura
# * Por ejemplo un polinomio cúbico:
# 
# ### <center>$Y = a\ X^{3} + b\ X^{2} + c\ X + d$</center>

# In[ ]:


# En este caso no es necesario la conversión de filas en columnas
# ---------------------------------------------------------------

# Volvemos a extraer las columnas de datos del dataframe
# -------------------------------------------------------
x = np.array(df[col1])
y = np.array(df[col2])


# In[ ]:


# Regresión polinomial de grado n
# -------------------------------
poly = PolynomialFeatures(degree=3, include_bias=False)

# Preparación de datos
# ---------------------
poly_features = poly.fit_transform(x.reshape(-1, 1))

# Realizamos el ajuste
# ---------------------
model = LinearRegression()
model.fit(poly_features,y)

# Resultados
ajuste = model.predict(poly_features)

# Estos son los coeficientes del polinomio
c, b, a   = model.coef_
d         = model.intercept_

# El coeficiente de determinación
# --------------------------------
r2    = r2_score(y, ajuste)

# El error cuadrático medio (RMSE)
# ----------------------------------
rmse  = np.sqrt(mean_squared_error(y, ajuste ))

# Mostramos los coeficientes del polinomio
# ----------------------------------------
print('a = %f\nb = %f\nc = %f\nd = %f' % (a,b,c,d))

# Mostramos el error/calidad del ajuste
# ---------------------------------------
print('\nEl coeficiente de determinación es: %.2f' % r2)
print('El error RMS es : %.2f' % rmse)


# * Representamos gráficamente

# In[ ]:


# Vamos a generar los valores del polinomio de tercer grado
# ---------------------------------------------------------
xn        = np.arange(x.min(),x.max(),step=1)
polinomio = a * xn**3 + b * xn**2 + c * xn + d


# In[ ]:


# Configuramos el gráfico
# ------------------------
fig, ax = plt.subplots(figsize=(12,8))

# Dibujamos los puntos
# ----------------------
ax.plot(x,y,
        marker = 'o',
        ms     = 3,
        lw     = 0,
        color  = 'blue'
        )

# Fija los límites del gráfico
# ------------------------------
ax.set_xlim(0,125)
ax.set_ylim(0,125)        

# Añadimos una línea en la diagonal
# ----------------------------------------------------------------------------------
ax.plot([0,125],[0,125], color='red', ls='--', lw=2)

# Para facilitar la comparación hacemos que los ejes tengan las mismas dimensiones
# ----------------------------------------------------------------------------------
ax.set_aspect('equal')

# Dibujamos el polinomio
# -----------------------
ax.plot(xn,polinomio, marker=None, ms=0, lw=3,color='black')

# Añadimos una rejilla
# ---------------------
ax.grid(True)

# Escribimos el polinomio en texto para el título
# -------------------------------------------------
poli  = 'Y = (%.4f) * x$^{3}$ + (%.4f) * x$^{2}$ + (%.4f) * X + (%.4f)' % (a,b,c,d)
error = 'R$^{2}$ = %.2f\nRMSE = %.1f' % (r2,rmse)

# Ponemos el título
# ------------------
ax.set_title('%s VS %s   -    %s  -  %s\n%s\n%s' % (magnitud2,magnitud1,estacion1,anio,poli,error)) # Titulo  

# Etiquetas para los ejes
# -------------------------
ax.set_xlabel('%s %s' % (magnitud1,unidades1))                                   # Etiqueta X   
ax.set_ylabel('%s %s' % (magnitud2,unidades2))                                   # Etiqueta Y  

# Dibujo
plt.show()


# ###8. Eliminación de datos atípicos
# ---

# * ¿Cómo cambia el resultado de los ajustes cuando se depuran los datos?
# * Vamos a eliminar los valores **atípicos extremos** 

# In[ ]:


# Calculamos los percentiles 25 y 75 de la primera columna
# ---------------------------------------------------------
p25_x, p75_x = df['pm2.5'].quantile((0.25,0.75))

# Calculamos el rango intercuartílico de la primera columna
# --------------------------------------------------------
riq_x = p75_x - p25_x

# Calculamos los percentiles 25 y 75 de la segunda  columna
# ---------------------------------------------------------
p25_y, p75_y = df['pm10'].quantile((0.25,0.75))

# Calculamos el rango intercuartílico de la primera columna
# --------------------------------------------------------
riq_y = p75_y - p25_y

# Eliminamos los valores que se encuentran más allá
# de 1.5 veces el rango intercuartílico
# ---------------------------------------------------
df1 = df[
        (df['pm2.5'] > (p25_x - 3.0 * riq_x))  & 
        (df['pm2.5'] < (p75_x + 3.0 * riq_x))  & 
        (df['pm10']  > (p25_y - 3.0 * riq_y))  & 
        (df['pm10']  < (p75_y + 3.0 * riq_y)) 
        ]

print(p25_x-3.0*riq_x,  p75_x+3.0*riq_x)
print(p25_y-3.0*riq_y,  p75_y+3.0*riq_y)
print('Eliminados %d datos atípicos' % (len(df)-len(df1)))


# * Para ver los nuevos resultados:
#   * volvemos a extraer los datos del dataframe
#   * ejecutamos de nuevo los bloques 7 y 8

# In[ ]:


x = np.array(df1[col1])
y = np.array(df1[col2])


# ###9. Resumen
# ---

# * En este notebook hemos visto algunos aspectos relacionados con la correlación de series temporales:
#   * Comparación visual
#   * Regresión a una recta
#   * Regresión polinomial
#   * Evaluación de la calidad de los ajustes
#   * Efecto de la depuracion en las regresiones
