#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/4_caracterizaci%C3%B3n_estadistica_datos.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Caracterización estadística de los datos

# * Vamos a explorar algunas de las posibilidades de análisis de datos de calidad del aire que ofrece Python en ámbito de la estadística. 
# * Usaremos como hasta ahora datos meteorológicos de AEMET y registros de contaminación de la Comunidad de Madrid.

# ###1. Preparación de datos y código
# ---

# * Para trabajar más cómodamente vamos a descargar todos los ficheros del repositorio GitHub
# * De esa manera dispondremos de los datos localmente para nuestro análisis.

# In[ ]:


# * Importamos las extensiones que vamos a necesitar. 
# 
# * Para simplificar la tarea hemos empaquetado las funciones de lectura de datos en un fichero independiente llamado "lectura_de_datos.py"

# In[ ]:


import lectura_de_datos                                   # lee ficheros de datos meteorológicos y de contaminación de Madrid
import matplotlib.pyplot as plt                           # dibujo de gráficos
from scipy import stats                                   # cálculo estadístico
import numpy as np                                        # matrices


# ###2. Inventario de datos
# ---

# * Por conveniencia, hemos introducido en "lectura_de_datos.py" el inventario de estaciones de medida de la contaminación.
# * Listamos los campos: **código | municipio | nombre**

# In[ ]:


# Simplemente escribimos el nombre de la variable para visualizar su contenido
# -----------------------------------------------------------------------------
print(lectura_de_datos.estalist_com)


# * Listamos los contaminantes registrados.
# * **Código  |  Magnitud  | Unidades**
# 

# In[ ]:


print(lectura_de_datos.maglist_com)


# * Hacemos lo mismo con los datos meteorológicos
# * Las estaciones (en este caso son las mismas)
# * **código | municipio | nombre**
# 

# In[ ]:


# Simplemente escribimos el nombre de la variable para visualizar su contenido
# -----------------------------------------------------------------------------
print(lectura_de_datos.estalist_meteo)


# * Y por último, la magnitudes meteorológicas
# * **Código | Magnitud | Unidades**

# In[ ]:


# Simplemente escribimos el nombre de la variable para visualizar su contenido
# -----------------------------------------------------------------------------
print(lectura_de_datos.maglist_meteo)


# ###3. Carga de datos
# ---

# * En el siguiente ejemplo, vamos a cargar datos de concentración de NO2 en la ciudad de Móstoles a lo largo del año 2019: 
# * Esta versión de la funcion lectura_de_datos devuelve:
#   * el dataframe con los datos
#   * el nombre de la estación
#   * la magnitud medida
#   * sus unidades
# * Eso facilita la automatización de los gráficos.
# 
# 

# In[ ]:


# Seleccionamos un año
# ----------------------
anio = 2022

# Cargamos los datos de NO2 de Móstoles
# ---------------------------------------------------
df, magnitud, unidades,estacion = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio,
                                     codigo_magnitud = 8,           # Dióxido de nitrógeno
                                     codigo_estacion = 28092005     # Móstoles  
                                     ) 

# Cargamos los datos de presión atmosférica de Guadalix de la Sierra
# -------------------------------------------------------------------
# df, magnitud, unidades,estacion = lectura_de_datos.meteo(
#                                    '../datos/meteo/%s.csv' % anio,
#                                     codigo_magnitud = 83,         # Temperatura
#                                     codigo_estacion = 28067001    # Guadalix de la Sierra  
#                                     ) 

# Inspeccionamos el contenido
# ----------------------------
print(df)


# ###4. Representación gráfica
# ---

# * Representamos los resultados en un gráfico simple X-Y

# In[ ]:


#Dibujamos la serie temporal
# ------------------------------------------------------
ax = df.plot(
        marker=None,                                          # Símbolo
        ms=1,                                                 # Tamaño del símbolo
        lw=1,                                                 # Grosor de líneas de conexión
        color='blue',                                         # Color
        grid=True,                                            # Rejilla
        figsize=(14,8),                                       # Tamaño del gráfico
        legend=False,                                         # Leyenda
        fontsize = 12,                                        # Tamaño de las anotaciones en los ejes        
        #xlim=('2022-03-10','2022-04-01'),
        #ylim=(0,700)
        )

# Definimos el título del gráfico
# --------------------------------
titulo = '%s  -  %s     %s %s' % (estacion,anio,magnitud,unidades)
ax.set_title(titulo,    size=16)

# Etiquetas de los ejes X-Y
# --------------------------
ax.set_xlabel('Fecha',  size=16)
ax.set_ylabel(unidades, size=16)


# CONTROL DE ETIQUETAS DE TIEMPO
# Ver "date tickers" y "date formaters" en
# https://matplotlib.org/stable/api/dates_api.html


# Importamos funciones de localización de fechas
# -------------------------------------------------
#from matplotlib.dates import DayLocator, WeekdayLocator, MonthLocator, YearLocator

# 1) DÓNDE COLOCAR LOS TICS MAYORES
# ===============================

# Pone tics mayores los días 5 y 20 de cada mes, cada dos meses
# --------------------------------------------------------------
# ax.xaxis.set_major_locator(dates.MonthLocator(bymonthday=(5,20), interval=2))

# Pone tics mayores solo los domingos de cada tres semanas
# lunes=0 | martes=1 | miércoles=2 | jueves=3 | viernes=4 | sábado=5 | domingo=6
# --------------------------------------------------------------------------------
#ax.xaxis.set_major_locator(dates.WeekdayLocator(byweekday=(6), interval=3))       

# 2) QUÉ FORMATO TIENEN LOS TICS MAYORES
# ====================================

# Establece el formato de la fecha para los tics mayores
# -------------------------------------------------------
#ax.xaxis.set_major_formatter(dates.DateFormatter("%d %B %y"))                

# 3) DÓNDE COLOCAR LOS TICS MENORES
# ===============================

# Pone tics menores el día 15 de cada mes
# -----------------------------------------
#ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))                

# 4) QUÉ FORMATO TIENEN LOS TICS MENORES
# ====================================

# Establece el formato de la fecha para los tics menores
# ---------------------------------------------------------
#ax.xaxis.set_minor_formatter(dates.DateFormatter('%d'))

# inclinación de las etiquetas
# ----------------------------
#ax.tick_params(axis="x", labelrotation= 45)                           


plt.show()


# ###5. El histograma
# ---

# In[ ]:


# Configuramos el gráfico
# ------------------------
fig, ax = plt.subplots(figsize=(12,7))

# Generamos el histograma correspondiente a los datos de la tabla df
# -------------------------------------------------------------------
a=df.hist(  
         bins     =  range(0,150,10),
         stacked  =  False,
         density  =  False,    # ¿Número de casos o frecuencia estadística?
         log      =  False,    # Logarítimico
         rwidth   =  0.9,
         ax = ax
)

# Ponemos un título ilustrativo
# --------------------------------
ax.set_title('Histograma    -    %s    -    %s    -     %s (%s)' % (anio,estacion,magnitud,unidades),size=14)

# Ponemos límites al eje Y (frecuencias estadísticas)
# ----------------------------------------------------
#ax.set_ylim(0,20)

# Ponemos etiquetas a los ejes X-Y
# ----------------------------------
ax.set_ylabel('Número de registros',size=15)
#ax.set_ylabel('Frecuencia estadística',size=15)
ax.set_xlabel(unidades,size=15)

# Dibujo
# ------
plt.show()


# ###6. La moda
# ---

# * La moda es el valor más probable, el que se repite con más frecuencia en una serie de datos:

# In[ ]:


# La moda se puede calcular con el método mode
# ---------------------------------------------
moda = df.mode()
print(moda)


# ###7. El valor medio
# ---

# * El valor medio pondera los valores observados con la frecuencia con la que se presentan.

# In[ ]:


# La media se puede calcular con el método mean
# ---------------------------------------------
media = df.mean()[0] 


# * Vamos a representar gráficamente los valores estadísticos
# * Para poder reutilizar el código que realiza el gráfico, lo metemos en una función

# In[ ]:


# Definimos nuestra función llamada "dibuja"
# ------------------------------------------

def dibuja(df, estadisticos) :
  """
  Entrada: 
             df           : dataframe
             estadísticos : valores estadísticos a dibujar
  Salida:
             Ninguna          
  """

  from matplotlib.dates import MonthLocator, DateFormatter

  # Dimensiona el gráfico
  # ----------------------
  fig, ax = plt.subplots(2,1,figsize=(12,7))

  # Busca los valores máximos y mínimos del registro de datos
  # ---------------------------------------------------------
  min = df.min()
  max = df.max()

  # Dibujamos la serie temporal
  # ---------------------------
  df.plot(grid=True,             ax = ax[0], color='#444444')

  # Ponemos un título
  # ------------------
  titulo = '%s    -    %s    -     %s (%s)     [min=%.1f,  max=%.1f]'
  ax[0].set_title(titulo % (anio,estacion,magnitud,unidades,min,max),size=14)

  # Añadimos una etiqueta al eje Y con las unidades de medida
  # -----------------------------------------------------------
  ax[0].set_ylabel(unidades,size=12)

  # Formato de fechas
  # -----------------
  ax[0].xaxis.set_major_locator(MonthLocator())                             # Poner tics mayores al inicio de cada mes
  ax[0].xaxis.set_minor_locator(MonthLocator(bymonthday=15))                # poner tics menores el día 15 de cada mes
  ax[0].xaxis.set_major_formatter(DateFormatter("%d %B %y"))                # formato de la fecha para los tics mayores
  ax[0].xaxis.set_minor_formatter(DateFormatter(''))                        # formato de la fecha para los tics menores
  ax[0].tick_params(axis="x", labelrotation= 45)                            # inclinación de las etiquetas

  # Dibujamos el histograma
  # -------------------------
  df.hist(bins = range(0,175,5), ax = ax[1], color='#444444')
  ax[1].set_title(None)
  ax[1].set_xlabel(unidades,size=12)

  # Definimos unos cuantos colores
  # -----------------------------------------
  color = ('b','r','g','c','orange','m','y','k')

  # Inicializamos el contador de colores
  # -------------------------------------
  n = 0

  # Dibujamos líneas que identifican los valores estadísticos en la
  # serie temporal y en el histograma
  # -----------------------------------------------------------------
  for nombre,valor in estadisticos.items() :

     # Añade una línea horizontal a la serie temporal
     # -----------------------------------------------
     ax[0].axhline(y=valor, ls='--', lw=3, label='%s=%.1f' % (nombre,valor), color=color[n])

     # Añade una línea vertical al histograma
     # -----------------------------------------------
     ax[1].axvline(x=valor, ls='--', lw=3,label='%s=%.1f' % (nombre,valor), color=color[n])

     # Incrementa el contador
     # -----------------------
     n += 1

  # Añadimos una leyenda
  # --------------------
  ax[1].legend()

  # Ajustamos visualmente los gráficos
  # -----------------------------------
  plt.tight_layout()

  return


# * Una vez creada la función podemos llamarla para que nos dibuje el valor medio de nuestros datos:

# In[ ]:


# Creamos un diccionario en el que se asigna el valor de la media que calculamos antes
# -------------------------------------------------------------------------------------
esta = {'media': media}

# Llamamos a la función de dibujo
# --------------------------------
dibuja(df,esta)


# ###8. **La dispersión**
# ---
# 
# 

# * Mide en que grado se compactan los datos alrededor de la tendencia central.
# * Un registro disperso presenta un amplio rango de valores.
# * Un registro poco disperso toma valores que distan poco de la media.
# * La ***varianza*** se corresponde con el valor medio de las desviaciones cuadráticas respecto del valor medio. 
# * Tiene una potente significación en estadística
# * La ***desviación típica*** es la raiz cuadrada de la ***varianza***
# * Tiene las mismas unidades que la magnitud

# In[ ]:


# Podemos calcular la varianza con la función var()
# ---------------------------------------------------
varianza          = df.var()[0]
print('varianza = %.1f (%s)**2' % (varianza,unidades))


# Podemos calcular la desviación típica con la función std
# -----------------------------------------------------------
desviacion_tipica = df.std()[0]
print('desviación típica = %.1f (%s)' % (desviacion_tipica,unidades))

# Añadimos los nuevos estadísticos al diccionario
# -----------------------------------------------
esta['s1'] = media - desviacion_tipica
esta['s2'] = media + desviacion_tipica

# Dibujamos
# --------------
dibuja(df,esta)

# Borramos los valores del diccionario para no arrastrarlos en el futuro
# -----------------------------------------------------------------------
del esta['s1']
del esta['s2']


# ###9. **La mediana**
# ---

# * Se trata de otra medida de tendencia central, como la media
# * Corresponde al valor que tiene igual número de registros mayores y menores
# * Equivale al percentil 50 de la distribución
# * Es más robusta porque es menos sensible a los valores extremos

# In[ ]:


# Podemos clacular la mediana con la función median()
# -------------------------------------------------------
mediana = df.median()[0] 

# Añadimos el nuevo estadístico al diccionario
# ---------------------------------------------
esta['mediana'] = mediana

# Dibujamos
# --------------
dibuja(df,esta)


# ###10. **Percentiles**
# ---

# * Son los valores por debajo de los cuales se encuentra un determinado porcentaje de los registros
# * Por ejemplo, el percentil 75 de una serie de datos es el valor tal que el 75% de los registros es menor y el 25% es mayor
# * A menudo es más interesante usar los percentiles P1 y P99 en lugar del mínimo y el máximo de una serie
# * Hay más de una forma de calcularlos
# * Los límites de los intervalos dependen de la definición 

# In[ ]:


# Para obtener los percentiles 1, 5, 25, 75, 95 y 99 de una serie
# los incluimos en una tupla:
# ----------------------------------------------------------------
nivel = (1, 5, 25, 75, 95, 99)

# A continuación invocamos la función percentile
# -------------------------------------------------
p = np.percentile(df,nivel)
print(p)

# Los añadimos todos al diccionario
# ----------------------------------
for n in range(len(nivel)) :
   label = 'P%d' % nivel[n]
   esta[label] = p[n]

# Dibujamos los percentiles
# --------------------------
dibuja(df,esta)


# ###11. **Valores atípicos (outliers)**
# ---

# * Son datos alejados de los valores de tendencia central, que pueden ser sospechosos de deberse a errores de medida.
# * No existe un método objetivo para eliminarlos.
# * Pese a sus valores extremos pueden ser datos válidos.
# * Distinguimos entre valores atípicos leves y extremos

# * Un método popular para determinar qué datos son atípicos y eliminarlos de la muestra se basa en el ***rango intercuartílico*** (***RIQ***).
# 
# * El ***RIQ***  es la diferencia entre los percentiles 75 y 25.
# 
# * Si un registro se encuentra a una distancia de P25 o P75 que supera 1.5 veces el **RIQ**, se considera un **valor atípico leve**.
# 
# * Si un registro se encuentra a una distancia de P25 o P75 que supera 3 veces el **RIQ**, se considera un **valor atípico extremo**.

# In[ ]:


# Calculamos los percentiles 25 y 75
# ---------------------------------------
P25, P75 = np.percentile(df, (25 ,75))

# El rango intercuartílico es la diferencia
# --------------------------------------------
RIQ = P75 - P25

# Mostramos valores
# ------------------
print('P25=%.1f  P75=%.1f ====>  RIQ=%.1f' % (P25, P75, RIQ))


# In[ ]:


# Valores atípicos leves son los que:
#     a) superan por ENCIMA del P75 la distancia 1.5 * RIQ
#     b) superan por DEBAJO del P25 la distancia 1.5 * RIQ 
# ----------------------
L1 = P25 - 1.5 * RIQ
L2 = P75 + 1.5 * RIQ

# Mostramos los valores atípicos leves
# ----------------------------------------
print('Los valores inferiones a %.1f son ATÍPICOS LEVES' % L1)
print('Los valores superiores a %.1f son ATÍPICOS LEVES' % L2)


# In[ ]:


# Valores atípicos extremos son los que:
#     a) superan por ENCIMA del P75 la distancia 3.0 * RIQ
#     b) superan por DEBAJO del P25 la distancia 3.0 * RIQ 
# ----------------------
E1 = P25 - 3 * RIQ
E2 = P75 + 3 * RIQ

# Mostramos los valores atípicos leves
# ----------------------------------------
print('Los valores inferiones a %.1f son ATÍPICOS EXTREMOS' % E1)
print('Los valores superiores a %.1f son ATÍPICOS EXTREMOS' % E2)


# * Añadimos los valores extremos al diccionario y dibujamos

# In[ ]:


# Añadimos al diccionario 
# ---------------------------------------
esta = {'L1':L1,'L2':L2,'E1':E1,'E2':E2}

# Dibujamos los valores extremos
# --------------------------------
dibuja(df,esta)


# ###12. **Depuración de valores atípicos**
# ---

# * Veamos qué ocurre si eliminamos los valores atípicos extremos:

# In[ ]:


# Seleccionamos de nuestra tabla los registros que NO corresponden a valores atípicos extremos
# ---------------------------------------------------------------------------------------------
df1 = df[ (df.valor >= E1) & (df.valor <= E2) ]

# ¿Qué diferencia hay en en número de datos?
# -------------------------------------------
n = len(df) - len(df1)

# Mostrar número de valores atípicos eliminados
# ----------------------------------------------
print('Se eliminaron %d valores atípicos extremos de una muestra de %d datos (%.2f%%)' % (n,len(df),100*n/len(df)))


# * Recalculamos la media y la mediana con la serie de dato "*depurada*" de outliers extemos:

# In[ ]:


# Añadimos al diccionario
# ------------------------
esta = {'media': df1.mean()[0],'mediana': df1.median()[0]}

# Dibujamos
# -----------------
dibuja(df1,esta)


# * ¿Y si hubiéramos eliminado todos los valores atípicos?

# In[ ]:


# Seleccionamos de nuestra tabla los registros que NO corresponden a valores atípicos extremos
# ---------------------------------------------------------------------------------------------
df1 = df[ (df.valor >= L1) & (df.valor <= L2) ]

# ¿Qué diferencia hay en en número de datos?
# -------------------------------------------
n = len(df) - len(df1)
print('Se eliminaron %d valores atípicos leves de una muestra de %d datos (%.2f%%)' % (n,len(df),100*n/len(df)))


# * Recalculamos la media y la mediana con la serie de dato "depurada" de todos los outliers:

# In[ ]:


# Añadimos al diccionario
# ------------------------
esta = {'media': df1.mean()[0],'mediana': df1.median()[0]}


# Dibujamos
# -----------------
dibuja(df1,esta)


# ###13. **Resumen**
# ---

# * En este notebook hemos visto como analiza en nuestros datos algunos tópicos de estadística descriptiva:
# 
#   * El histograma de frecuencias 
#   * La moda 
#   * El valor medio
#   * La mediana
#   * La dispersión
#   * Los percentiles
#   * Los valores atípicos leves y extremos
#   * La depuración de series
# 
# 
