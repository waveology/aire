# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 06:33:05 2023

@author: Ernesto
"""

import lee_datos
import matplotlib.pyplot as plt
from scipy import stats



yearlist = ('2019','2020','2021','2022')
codigo_magnitud = 8
codigo_estacion=28092005


df = []
for year in yearlist :
    
    d, magnitud, unidades,estacion = lee_datos.comunidad(
             'datos/comunidad/%s.csv' % year,
              codigo_magnitud=codigo_magnitud, 
              codigo_estacion=codigo_estacion) 
    df.append(d)

# Series temporales
# ----------------------
fig,ax = plt.subplots()
for i in range(len(yearlist)) :    
    df[i].plot(x='fecha',y='valor',
          marker='o',ms=3,lw=0,grid=True,
          label=yearlist[i],title='valor',ax=ax)
ax.legend()
ax.set_title('%s     -     %s  (%s)' % (estacion,magnitud,unidades))



fig,ax = plt.subplots()
for i in range(len(yearlist)) :    
    df[i].hist(column='valor',bins=20,ax=ax,range=(0,100),
               alpha=0.5,label=year)
ax.legend()
ax.set_title('%s     -     %s  (%s)' % (estacion,magnitud,unidades))


fig,ax = plt.subplots(2,2)
fax = ax.ravel()
for i in range(len(yearlist)) :    
    df[i].hist(column='valor',bins=30,ax=fax[i],
                label=yearlist[i],range=(0,100),
                density=False,log=False,edgecolor='black')
    fax[i].legend()
    fax[i].set_title(None)
fig.suptitle('%s     -     %s  (%s)' % (estacion,magnitud,unidades))


print('Año1  Año2 media_año1 media_año2 mediana_año1 mediana_año2 p-valor')
print("------------------------------------------------------------------")
for i in range(len(yearlist)) :
    for j in range(len(yearlist)) :    
        
        if i >= j : continue
        
        st,pvalue = stats.mannwhitneyu(df[i]['valor'],df[j]['valor'])
        
        mean1   = df[i]['valor'].mean()
        mean2   = df[j]['valor'].mean()
        median1 = df[i]['valor'].median()
        median2 = df[j]['valor'].median()
        
        print('%s %s %.4f %.4f %.4f %.4f %.5f' 
              % (yearlist[i],yearlist[j],mean1,mean2,median1,median2,pvalue))






