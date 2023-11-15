import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo CSV a pandas
df = pd.read_csv('C:/Users/Luis/Desktop/proyecto parte 2/crecimiento_instagram.csv')

# Calcular el crecimiento neto (Seguidores - Dejaron_de_seguir)
df['Crecimiento_Neto'] = df['Seguidores'] - df['Dejaron_de_seguir']

#Seguidores nuevos a lo largo del tiempo
plt.figure(figsize=(12, 6))
plt.plot(df['Fecha'], df['Seguidores'], label='Seguidores', marker='o', linestyle='-', color='blue')
plt.xlabel('Fecha')
plt.ylabel('Seguidores')
plt.title('Crecimiento de Seguidores en Instagram')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

#Crecimiento Neto a lo largo del tiempo
plt.figure(figsize=(12, 6))
plt.plot(df['Fecha'], df['Crecimiento_Neto'], label='Crecimiento Neto', marker='o', linestyle='-', color='green')
plt.xlabel('Fecha')
plt.ylabel('Crecimiento Neto')
plt.title('Crecimiento Neto en Instagram')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

#Personas que Dejaron de Seguir a lo largo del tiempo
plt.figure(figsize=(12, 6))
plt.plot(df['Fecha'], df['Dejaron_de_seguir'], label='Dejaron de Seguir', marker='o', linestyle='-', color='red')
plt.xlabel('Fecha')
plt.ylabel('Dejaron de Seguir')
plt.title('Personas que Dejaron de Seguir en Instagram')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Mostrar las gráficas
plt.tight_layout()
plt.show()
