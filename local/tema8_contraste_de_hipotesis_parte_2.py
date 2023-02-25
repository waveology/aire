#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/tema8_contraste_de_hipotesis_parte_2.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Contraste de hipótesis II

# * Vamos a aplicar el contraste de hipótesis al análisis de datos de calidad del aire. 
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


import lectura_de_datos           # lee ficheros de datos meteorológicos y de contaminación de Madrid
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


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

# * Vamos a cargar datos correspondientes a dos años distintos
# 

# In[ ]:


# Ejemplo con datos de contaminación
# ----------------------------------
anio1 = '2019'
anio2 = '2020'
estacion = 28092005  # Móstoles

# Contaminantes
# ----------------------

# Primer ejemplo
# --------------
magnitud = 10   # PM10

# Segundo ejemplo
# --------------
#magnitud =  8   # NO2

df1, magnitud1, unidades1,estacion1 = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio1,
                                     codigo_magnitud = magnitud,
                                     codigo_estacion = estacion
                                     ) 

df2, magnitud2, unidades2,estacion2 = lectura_de_datos.contaminacion(
                                    '../datos/contaminacion/%s.csv' % anio2,
                                     codigo_magnitud = magnitud,
                                     codigo_estacion = estacion
                                     ) 

df1.rename(columns={'valor':anio1}, inplace=True)
df2.rename(columns={'valor':anio2}, inplace=True)

print(df1.describe())
print(df2.describe())


# * ¿Hay diferencias entre los valores medios de ambas series?
# * ¿Son esas diferencias ***significativas*** o mero producto del azar?
# * Recordemos que lo que observamos es una *realización* de entre múltiples posibilidades similares pero no idénticas.

# In[ ]:


# Diferencia en la media
# -------------------------------------
diff = 100*(df2[anio2].mean()/df1[anio1].mean()-1)

print('Respecto a %s, la media del año %s ha experimentado un cambio del %.1f%%' % (anio2,anio1,diff))


# ###4. Inspección visual
# ---

# * Echamos un vistazo a ambas series temporales para estimar visualmente si hay cambios apreciables

# In[ ]:


# Cada serie en un gráfico independiente
# ---------------------------------------
fig, ax = plt.subplots(nrows=2,ncols=2,figsize=(12,8))

# Serie temporal año 1
# -----------------------------------
ax[0,0].plot(df1[anio1],label=anio1)
ax[0,0].set_ylim(0,180)

# Histograma año 1
# ------------------------------------
ax[0,1].hist(df1[anio1],label=anio1,bins=30)
ax[0,1].set_xlim(0,100)
ax[0,1].set_ylim(0,2600)
ax[0,1].set_title('mediana=%.2f   media=%.2f' %(df1[anio1].median(),df1[anio1].mean()))
ax[0,1].axvline(df1[anio1].mean(),color='red',lw=2,ls='--')
ax[0,1].axvline(df2[anio2].median(),color='black',lw=2,ls='--')

# Serie temporal año 2
# -----------------------------------
ax[1,0].plot(df2[anio2],label=anio2)
ax[1,0].set_ylim(0,180)

# Histograma año 2
# -------------------------------------
ax[1,1].hist(df2[anio2],label=anio2,bins=30)
ax[1,1].set_xlim(0,100)
ax[1,1].set_ylim(0,2600)
ax[1,1].set_title('mediana=%.2f   media=%.2f' %(df2[anio2].median(),df2[anio2].mean()))
ax[1,1].axvline(df2[anio2].mean(),color='red',lw=2,ls='--')
ax[1,1].axvline(df2[anio2].median(),color='black',lw=2,ls='--')

for a in ax.flatten() :
   a.grid(True)
   a.legend()

plt.suptitle('%s %s %s' % (estacion1,magnitud1,unidades1))   
plt.show()


# ###5. ¿Es la misma distribución?
# ---

# * Hay muchos tests estadísticos de uso común en contraste de hipótesis
# * Unos son más robustos que otros.
# * Unos funcionan mejor con muestras de determinado tamaño.
# * El Test **U de Mann-Withney** se usa para comparar distribuciones

# In[ ]:


# Ejemplo de comparación de dos 
# muestras de una misma población
# ---------------------------------------
A = np.random.normal(size=1000,loc=0,scale=1)
B = np.random.normal(size=1000,loc=0,scale=1)
fig,ax = plt.subplots(1,2)
ax[0].hist(A,bins=50)
ax[1].hist(B,bins=50)
for a in ax:
  a.grid(True)
  a.set_ylim(0,70)
  a.set_xlim(-3,3)
plt.show()

st,p_valor = stats.mannwhitneyu(A,B)
print('p_valor=%.4f' % p_valor)


# ###6. Test de hipótesis I
# ---

# * Vamos a suponer que se trata de la misma distribución y que las diferencias observadas en los estadísticos son debidas al azar
# * Esa será la hipótesis de partida
# * Usaremos el test U de Mann Whitney para determinar la probabilidad de que ambas series correspondan a la misma población
# * Compararemos el p-valor resultante con el nivel de significación que atribuimos al test, por ejemplo 5%
# * Decidiremos si aceptamos o rechazamos la hipótesis nula

# In[ ]:


# Aplicamos el test U de Mann-Whitney a nuestras series
# ------------------------------------------------------
st,p_valor = stats.mannwhitneyu(df1[anio1],df2[anio2])
print('p_valor=%e' % p_valor)


# In[ ]:


# Nivel de significación
# ----------------------
alfa = 0.05

# Resultado
# ----------
if p_valor < alfa :
    print('Rechazamos la hipótesis de partida (hay suficiente evidencia en contra)')
else :
    print('Nos quedamos con la hipótesis de partida (no hay suficiente evidencia en contra)')


# ###7. Otro ejemplo
# ---

# In[ ]:


# Ejemplo con datos meteorológicos
# ----------------------------------
anio1 = '2020'
anio2 = '2022'
estacion = 28092005  # Móstoles

# Vabiables meteorológicas
# -------------------------

# Primer ejemplo
# --------------
magnitud = 83   # Temperatura

# Segundo ejemplo
# --------------
magnitud =  87   # Presión atmosférica

df1, magnitud1, unidades1,estacion1 = lectura_de_datos.meteo(
                                    '../datos/meteo/%s.csv' % anio1,
                                     codigo_magnitud = magnitud,
                                     codigo_estacion = estacion
                                     ) 

df2, magnitud2, unidades2,estacion2 = lectura_de_datos.meteo(
                                    '../datos/meteo/%s.csv' % anio2,
                                     codigo_magnitud = magnitud,
                                     codigo_estacion = estacion
                                     ) 

df1.rename(columns={'valor':anio1}, inplace=True)
df2.rename(columns={'valor':anio2}, inplace=True)

print(df1.describe())
print(df2.describe())


# ###7. Resumen
# ---

# * En este notebook hemos visto un caso práctico de aplicación del contraste de hipótesis para la toma de decisiones.
# 
#  * Hemos comparado dos series temporales anuales de manera enteramente subjetiva (visualmente)
#  * Hemos comprobado que las medidas de tendencia central presentan diferencias
#  * Nos preguntamos si las diferencias son **significativas** desde un punto de vista estadístico
#  * Recurrimos a un test U de Mann-Whitney para estimar si ambas series son muestras de una misma población
#  * Comparando el p-valor del test con el nivel de significación decidimos tomamos una decisión.
