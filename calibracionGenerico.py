#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 11:38:29 2025

@author: sergiobarrioszamora
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from statistics import stdev
from statistics import mean

ruta = "/"

datos_opc = pd.read_csv(ruta + 'Archivo1', delimiter = ',') #Añadir nombre del primer archivo de datos
datos_opc2 = pd.read_csv(ruta + 'Archivo2', delimiter = ',') #Añadir nombre del segundo archivo de datos
datos_PM10 = pd.read_csv(ruta + 'Congresos_PM10.txt', delimiter = '\t')

fecha_añadir = "2025-04-03"  
datos_opc['TIEMPO']=pd.to_datetime(fecha_añadir + " " + datos_opc["TIEMPO"],  # Combina fecha + hora
    format="%Y-%m-%d %H:%M:%S")
fecha_añadir = "2025-04-04"  
datos_opc2['TIEMPO']=pd.to_datetime(fecha_añadir + " " + datos_opc2["TIEMPO"],  # Combina fecha + hora
    format="%Y-%m-%d %H:%M:%S")

datos_PM10['date']=pd.to_datetime(datos_PM10['date'], format = "%d/%m/%Y %H:%M")
datos_opc = pd.concat([datos_opc, datos_opc2])

datos_opc.RESISTENCIA[datos_opc.RESISTENCIA < 0] == np.nan

datos_PM10 = datos_PM10.set_index('date')
datos_opc = datos_opc.set_index('TIEMPO')

datos_opc_10m=datos_opc.resample('10T').mean()

datos_opc_H =  datos_opc.resample('2H').mean()
datos_PM10_H = datos_PM10.resample('2H').mean()

# calibracion para 10m
# datos_PM10_H = datos_PM10 
# datos_opc_H = datos_opc_10m

plt.figure()
plt.plot(datos_PM10_H.index, datos_PM10_H.PM10)
plt.figure()
plt.plot(datos_opc_H.index, datos_opc_H.RESISTENCIA,'.')

r_pearson = np.corrcoef(datos_PM10_H.PM10, datos_opc_H.RESISTENCIA)


def func(x, a, b):
     return a*x + b
 
    
popt, pcov = curve_fit(func, datos_opc_H.RESISTENCIA, datos_PM10_H.PM10)

y_pred = func(datos_opc_H.RESISTENCIA, *popt)
r = datos_PM10_H.PM10 - y_pred
chisq = sum((r / datos_PM10_H.PM10) ** 2)
mediax = mean(datos_opc_H.RESISTENCIA)
mediay = mean(datos_PM10_H.PM10)

mediaxy = mean(datos_opc_H.RESISTENCIA*datos_PM10_H.PM10)
sigmax = stdev(datos_opc_H.RESISTENCIA)
sigmay = stdev(datos_PM10_H.PM10)
coef_Pearson = len(datos_opc_H.RESISTENCIA)*(mediaxy-mediax*mediay)/((len(datos_opc_H.RESISTENCIA)-1)*sigmax*sigmay)



fig=plt.figure(figsize=[18,12])
ax=fig.gca()
plt.plot(datos_opc_H.RESISTENCIA, datos_PM10_H.PM10, 'b.', label='Puntos', markersize=19)
plt.plot(datos_opc_H.RESISTENCIA, y_pred, 'r-', label='Regresión',linewidth=4.0)

plt.xlabel('Resistencia',fontsize=25)
plt.ylabel('PM10 ($\mu$g·m$^{-3}$)',fontsize=25)
plt.legend(loc='best',fontsize=25)

# Este comando permite modificar el grosor de los ejes:
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(4)

# Con estas líneas podemos dar formato a los "ticks" de los ejes:
plt.tick_params(axis="x", labelsize=25, labelrotation=0, labelcolor="black")
plt.tick_params(axis="y", labelsize=25, labelrotation=0, labelcolor="black")

# Aquí dibuja el gráfico que hemos definido.
plt.show()