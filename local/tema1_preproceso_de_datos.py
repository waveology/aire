# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/tema1_preproceso_de_datos.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # El preproceso de los datos

# * A veces, el acceso a los datos almacenados en ficheros puede resultar tedioso. 
# * Con frecuencia, los datos no se encuentran en el formato que necesitamos.
# * Hay invertir algo de tiempo en adaptarlos a nuestros métodos de análisis.

# ###1. El origen de los datos
# ---

# Vamos a ver un ejemplo de este preproceso en Python, basado en los datos de calidad del aire que publica la Comunidad de Madrid (España) y que están libremente disponibles en [la web](https://datos.comunidad.madrid/catalogo/dataset/calidad_aire_datos_historico)

# Descargamos los datos de algún año del histórico:

# In[2]:


# Seleccionamos un año cualquiera (hay datos disponibles desde 2005)
# -------------------------------------------------------------------
anio = 2023



# Permite manipulación eficiente de tablas de datos
# --------------------------------------------------
import pandas as pd


# A continuación, leemos el fichero de datos que hemos descargado antes, y que está en formato CSV, para generar un ***dataframe*** de Pandas. 
# 
# Para una correcta lectura especificamos que:
# 
# *   el separador de columnas es el punto y coma (;) 
# *   el símbolo usado para designar decimales es la coma (,). 
# 
# NOTA: Otros organismos como el Ayuntamiento de Madrid usan el punto (.) como separador decimal en sus datos de contaminación.

# In[5]:


# Leemos el fichero de datos
# --------------------------
df0 = pd.read_csv('../datos/contaminacion/%s.csv' % anio,  
                 sep=';', 
                 decimal=',')


# * Los datos están ahora en un ***dataframe*** llamado "df0"
# * Inspeccionamos la estructura del fichero.
# * Atención a la forma en la que se indica el tiempo.

# In[ ]:


print(len(df0))        # ¿Cuántas filas de datos tenemos?
print(df0.head(5))     #  Muestra las 5 primeras para hacernos una idea


# ###3. El filtrado de columnas
# ---

# * Para ahorrar memoria filtramos los datos eliminando la información de las filas que no necesitamos.
# 
# * Elegimos una estación de medida. Por ejemplo, **Guadalix de la Sierra**, a la que según el inventario le corresponde:
# 
#  *   **código**    : 28067001 (el campo **estación** solo usa los 3 últimos dígitos) 
#  *   **municipio** : 67
# 
# 
# * Elegimos una magnitud de medida. Por ejemplo, el dióxido de nitrógeno (NO$_{2}$), a la que corresponde:
# 
#  *   **magnitud** : 8

# In[ ]:


# df0 será una versión filtrada de df que solo contiene los datos seleccionados
# ------------------------------------------------------------------------------
df = df0[ (df0['magnitud']  == 8) 

       &  (df0['estacion']  == 1) 

       &  (df0['municipio'] == 67)]
       
# ¿Qué tamaño tiene?
# -------------------
print(len(df))

# Muestra las primeras cinco filas
# ----------------------------------
print(df.head(5))          


# ###4. Eliminación de columnas no necesarias
# ---

# Una vez que hemos filtrado los datos, podemos eliminar las columnas que ya no necesitamos:
# 
# * **provincia**
# * **municipio**
# * **estación**
# * **punto de muestreo**
# * **magnitud**

# In[ ]:


# Elimina de df las columnas indicadas
# --------------------------------------
df = df.drop(columns=['provincia','municipio','estacion','punto_muestreo','magnitud'])

# Muestra las primeras cinco filas
# ---------------------------------
print(df.head(5))     


# ###5. Pivotaje de filas y columnas
# ---

# * Se llama pivotaje al procedimiento por el cual los datos contenidos en columnas pasan a formar parte de filas y viceversa.
# 
# * En este ejemplo, nos gustaría tener en cada fila los datos correspondientes a cada hora. Sin embargo, la información de cada hora aparece en una columna distinta. 
# 
# * Con la función ***melt*** podemos crear un nuevo ***dataframe*** en el que las horas aparezcan en una columna y la magnitud medida en otra: 

# In[ ]:


# df1 será una versión de df en la que las horas aparecerán en filas en lugar de columnas
# ----------------------------------------------------------------------------------------
df1 = df.melt(                 
                 id_vars=['ano','mes','dia'],                        # Columnas que quedan fijas
                 value_vars = [ 'h%02d' % i for i in range(1,25)],   # Columnas que pasan a filas  
                 var_name='hora',                                    # Nombre para la nueva columna de horas          
                 value_name='valor'                                  # Nombre para la columna con la magnitud
                 )
# Muestra un resumen del dataframe
# -----------------------------------
print(df1)


# ###6. Modificación y adaptación de valores
# ---

# Recordatorio de funciones lambda:

# In[ ]:


# Funciones simples que se definen en una línea
# -----------------------------------------------
mifuncion = lambda y : y*y


# In[ ]:


mifuncion(12)


# * Observemos que en la tabla la hora aparece en formato de texto con la letra 'h' seguida de dos dígitos. 
# 
# * Usamos la función ***apply*** que actúa sobre los valores de una columna para corregirla: 

# In[ ]:


# En la columna 'hora', elimina el primer carácter y convierte el resultado en numérico
# --------------------------------------------------------------------------------------
df1['hora'] = df1['hora'].apply(lambda x : int(x[1:]))

print(df1)


# * Recordemos que en este proceso nos hemos dejado por el camino la información sobre la validez de los datos.
# * Por eso repetimos la misma operación con esas columnas generando un nuevo dataframe ***df2***

# In[ ]:


# df2 será una versión de df en la que la validez del dato aparecerán en filas en lugar de columnas
# -------------------------------------------------------------------------------------------------
df2 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'v%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='flag'
                 )
df2['hora'] = df2['hora'].apply(lambda x : int(x[1:]))
print(df2)


# ###7. Fusión de tablas
# ---

# * Hemos creado dos ***dataframes*** (df1 y df2) que contienen los registros de concentración del contaminante y la validez de los datos respectivamente. 
# 
# * A continuación los fusionamos con la función ***merge***:

# In[ ]:


# Muestra df1
# -----------
print(df1)

# Muestra df2
# ------------
print(df2)

# Fusiona ambas tablas
# --------------------
df = df1.merge(df2)

# Muestra el resultado
# ----------------------
print(df)


# ###8. Eliminación de datos no válidos
# ---

# * Puesto que no nos interesan los datos no válidos, los eliminamos de la tabla.
# * Después podemos eliminar la columna 'flag' que no necesitamos para nada.

# In[ ]:


# ¿Cuántos datos tenemos antes de eliminar los no válidos?
n_antes = len(df)

# Eliminamos los datos no válidos y borramos la columna flag en un mismo paso
# ----------------------------------------------------------------------------
df = df[df['flag'] == 'V'].drop(columns='flag')

# Mostramos el resultado
# ----------------------
print(df)

# ¿Cuántos datos no válidos fueron eliminados?
n_despues = len(df)
print('Eliminados %d datos no válidos' % (n_antes - n_despues))


# ###9. El tiempo
# ---

# * Para operar eficientemente con series temporales es conveniente que el tiempo se almacene en un tipo de variable especial (*datetime*) que incorpore la fecha y la hora.
# 
# * El siguiente paso consiste en combinar las columnas de 'año', 'mes', 'día' y 'hora' en otra llamada 'fecha':

# In[ ]:


# Creamos una columna de tiempo indicando qué columnas tienen el año, el mes, el día y la hora
# ---------------------------------------------------------------------------------------------
df['fecha'] = pd.to_datetime({'year':df.ano,'month':df.mes,'day':df.dia,'hour':df.hora})

# Muestra el resultado
# --------------------
print(df)


# * Ya no necesitamos las columnas de año, mes, día y hora:

# In[ ]:


# Eliminamos columnas superfluas
# -------------------------------
df = df.drop(columns=['ano','mes','dia','hora'])

# Mostrar resultado
# ------------------
print(df)


# ###10. Reordenación de columnas si es necesario
# ---

# * No es necesario reordenar las columnas para operar con ellas.
# * Pero si queremos hacerlo resulta sencillo::

# In[ ]:


# Basta con hacer una reasignación especificando el orden deseado para las columnas
# ----------------------------------------------------------------------------------
df = df[['fecha','valor']]

# Mostrar resultado
# -----------------
print(df)


# ###11. Resultado final
# ---

# * Ahora nuestros datos están dispuestos en un formato que simplifica mucho las tareas de análisis.
# * Por ejemplo, la representación gráfica de las series temporales:

# In[ ]:


# Importamos la extensión de gráficos Matplotlib
# ------------------------------------------------
import matplotlib.pyplot as plt

# Dibujamos la serie temporal de datos
# -------------------------------------
df.plot(x='fecha',y='valor')
plt.show()


# * Podemos añadir detales al gráfico especificando parámetros en la función plot.
# * Hay múltiples opciones en la [documentación](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html).

# In[ ]:


# Un título explicativo
# -----------------------
titulo = 'Concentración de NO$_{2}$ ($\mu$g/m$^{3}$) medida en la estación de Guadalix de la Sierra'


# Gráfico
# -------
df.plot(x='fecha',y='valor',
        fontsize = 12,       # Tamaño de etiquetas en los ejes X-Y
        figsize  = (15,10),  # Dimensiones del gráfico (pulgadas)
        marker   = 'o',      # Símbolo marcador del dato
        ms       = 5,        # Tamaño del marcador
        lw       = 1,        # Grosor de líneas conectoras    
        grid     = True,     # Rejilla de fondo           
        legend   = False,    # Leyenda del gráfico      
        title    = titulo    # Título del gráfico  
        )

# ¿Modificar el tamaño del títlo?
# --------------------------------
# plt.title(titulo,size=20)


# Mostrar gráfico
# ---------------
plt.show()


# ###12. Resumen
# ---

# En este notebook hemos tratado:
# 
# * la lectura de datos de contaminación de un fichero en formato CVS
# * El filtrado de filas de interés
# * La eliminación de columnas no requeridas
# * El pivotaje de tablas
# * La modificación condicional de contenidos de las tablas
# * La fusión de tablas basada en columnas comunes
# * El tratamiento del tiempo
# * La reordenación de columnas
# * La representacion gráfica simple de series temporales
# 
