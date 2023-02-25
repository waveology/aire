#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/waveology/aire/blob/main/tema7_contraste_de_hipotesis.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Contraste de hipótesis_I

# ### **1. Probabilidad de obtener determinados resultados en una moneda normal**
# ---
# 
# 

# * Todos sabemos que la probabilidad de obtener cara en el lanzamiento de una moneda *correcta* es del 50%
# <div><center><img src="https://github.com/waveology/aire/raw/main/img/quetzal.jpg" width="150"/></center></div>
# 
# * ¿Cuál será la probabilidad de obtener dos caras en dos lanzamientos?
# 
# * Al tratarse de un solo caso favorable entre cuatro posibles, la probabilidad será de 1/4 o del 25%
# 
# * La probabilidad de obtener, como mínimo, $k$ caras en una secuencia de $n$ lanzamientos viene dada por la distribución binomial:
# 
# $$\sum‎_{i=k}^{n} \binom{n}{i} \cdot p^i \space (1-p)^{n-i}$$
# 
# * Veamos algunos ejemplos con Python.
# 
# 
# 
# 
# 
# 
# 
# 

# In[ ]:


# Importamos la función binomial de la extensión de estadística scipy
# ---------------------------------------------------------------------
from scipy.stats import binom


# * Creamos una función que calcula la probabilidad de obtener **al menos** un número de caras en una secuencia de lanzamientos de una moneda
# 
# * El método cdf calcula la probabilidad de que el número de caras sea menor que un determinado umbral. Para obtener la probabilidad de que sea mayor o igual que ese umbral basta con restar ese valor a 1:

# In[ ]:


def probabilidad_caras(lanzamientos=1, numero_de_caras=1) :
    """
    Probabilidad de obtener caras al menos un número de veces
    al realizar varios lanzamientos de una moneda equilibrada
    """

    # Calcula
    # -------
    prob = 1-binom.cdf(k=numero_de_caras-1, n=lanzamientos, p=0.5)

    # Devuelve el valor resultante
    # ----------------------------
    return prob


# * Determinamos cuántos lanzamientos de moneda se realizan y cuántas caras esperamos obtener al menos:

# In[ ]:


# Número de lanzamientos
# ------------------------
lanzamientos     = 100

# Número mínimo de caras esperado
# -------------------------------
numero_de_caras  =  60

# Llamamos a la función
# -------------------------
probabilidad = 100 * probabilidad_caras(lanzamientos=lanzamientos, numero_de_caras=numero_de_caras)

# Muestra resultados
# -------------------
print('La probablidad de obtener al menos %d caras en %d lanzamientos es del %.3f %%' % (numero_de_caras,lanzamientos,probabilidad))


# ###**2. ¿Qué es un resultado aceptable?**
# ---

# * Nos preguntamos qué número de caras debería hacernos sospechar de que la moneda pudiera haber sido manipulada. 
# * La probabilidad de obtener al menos 60 caras en 100 lanzamientos es baja (2.8%) pero el caso puede darse. 
# * ¿Cómo podemos tomar una decisión sobre la  calidad de la moneda?

# ### **3. El contraste de hipótesis**
# ---

# * Se trata de un procedimiento para inferir si lo que observamos es compatible con lo que asumimos como cierto. 
# 
# * Proporciona un criterio para la toma de decisiones basado en la inferencia estadística.
# 
# * Se organiza típicamente en los siguientes pasos:
# 
#  * Se establece una hipótesis de partida (*hipótesis nula*)
#  * Se busca un test que determine la probabilidad del resultado observado de acuerdo a la hipótesis (p-valor)
#  * Atribuimos un nivel de significación al test ($\alpha$) 
#  * Si p-valor $\lt$ $\alpha$ rechazamos la hipótesis de partida
#  * Si el p-valor $\ge$ $\alpha$ conservamos la hipótesis de partida
# 
# 
# 
# 
# 

# ### **4. Ejemplo con la moneda**
# ---

# *   Hipótesis nula: la moneda está equilibrada.
# *   Hipótesis alternativa: la moneda no está equilibrada.
# *   Test: probabilidad de obtener al menos un determinado número de caras
# *   Nivel de significación:  $\alpha = 0.05$ (5%)

# In[ ]:


# Elegimos un nivel de significación del 5%
# Se trata de una opción de uso extendido
# --------------------------------------------
alfa   = 0.05

# Calculamos la probabilidad de obtener el resultado observado (p-valor)
# -----------------------------------------------------------------------
p_valor = probabilidad_caras(lanzamientos=100, numero_de_caras=59)

# Comparamos el p-valor con el nivel de significación del test
# --------------------------------------------------------------
if p_valor < alfa :

  # El p-valor es menor que alfa : rechazamos la hipótesis de partida
  # -----------------------------------------------------------------
  
  print('p_valor=%.3f < alfa=%.3f' % (p_valor,alfa))
  print('Hay suficiente evidencia para rechazar la hipótesis nula: la moneda NO está equilibrada')

else :

  # El p-valor es mayor que alfa : no rechazamos la hipótesis de partida
  # -----------------------------------------------------------------

  print('p_valor=%.3f >= alfa=%.3f' % (p_valor,alfa))
  print('NO hay suficiente evidencia para rechazar la hipótesis nula')  


# * Repetimos el experimento relajando el nivel de significación del test.
# * Es decir que estaremos dispuestos a aceptar resultados aún más improbables.
# 
#   * Hipótesis nula: la moneda está equilibrada, no está manipulada.
#   * Test: probabilidad de obtener al menos un determinado número de caras
#   * Nivel de significación:  \alpha$ = 0.01$ (1%)

# In[ ]:


# Elegimos un nivel de significación del 5%
# Se trata de una opción de uso extendido
# --------------------------------------------
alfa   = 0.01

# Calculamos la probabilidad de obtener el resultado observado (p-valor)
# -----------------------------------------------------------------------
p_valor = probabilidad_caras(lanzamientos=100, numero_de_caras=63)

# Comparamos el p-valor con el nivel de significación del test
# --------------------------------------------------------------
if p_valor < alfa :

  # El p-valor es menor que alfa : rechazamos la hipótesis de partida
  # -----------------------------------------------------------------  

  print('p_valor=%.3f < alfa=%.3f' % (p_valor,alfa))
  print('Hay suficiente evidencia para rechazar la hipótesis nula: la moneda NO está equilibrada')

else :

  # El p-valor es mayor que alfa : no rechazamos la hipótesis de partida
  # -----------------------------------------------------------------

  print('p_valor=%.3f >= alfa=%.3f' % (p_valor,alfa))
  print('NO hay suficiente evidencia para rechazar la hipótesis nula')  


# ### **5. Interpretación**
# ---

# *    Obtener al menos 58 caras en 100 lanzamientos es compatible con una moneda equilbrada, a un nivel de significación del **5%**
# 
# *    Obtener al menos 59 caras en 100 lanzamientos **acumula suficiente evidencia** contra la idea de moneda esté equilibrada, a un nivel de significación del **5%**
# 
# *    Obtener al menos 62 caras en 100 lanzamientos es compatible con una moneda equilbrada, a un nivel de significación del **1%**
# 
# *    Obtener al menos 63 caras en 100 lanzamientos **acumula suficiente evidencia** contra la idea de moneda esté equilibrada, a un nivel de significación del **1%**
# 
