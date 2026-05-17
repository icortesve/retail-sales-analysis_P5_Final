import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

def analisis_correlacion(df):
    """Genera un mapa de calor para identificar relaciones multivariables."""
    # Crear canvas
    plt.figure(figsize=(10, 8))

    # Para la matriz, se seleccionan solo las variables numéricas con mayúsculas correctas
    corr = df[['Age', 'Total Amount']].corr()
    
    sns.heatmap(corr, annot=True, cmap='vlag', vmin=-1, vmax=1, fmt=".2f", linewidths=0.5)
    plt.title('Mapa de Calor: Correlaciones de Variables', fontsize=15, pad=20)
    plt.show()

def graficar_analisis_comparativo_y_tendencia(df):
    """
    Crea un lienzo unificado de subplots para comparar variables clave y tendencia.
    Las leyendas mapean dinámicamente el promedio utilizando parches de Matplotlib.
    """
    # Datos temporales
    df_temp = df.copy()
    df_temp['Date'] = pd.to_datetime(df_temp['Date']) # Formato fecha
    resumen_temporal = df_temp.resample('ME', on='Date')['Total Amount'].sum() # Agrupa ventas al fin del mes
    
    # Cáluclo promedios para leyendas
    promedios_genero = df.groupby('Gender')['Total Amount'].mean()
    promedios_cat = df.groupby('Product Category')['Total Amount'].mean()
    
    # Canvas y subplots
    fig = plt.figure(figsize=(16, 12)) # Lienzo
    grid = plt.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.2) # Lienzo dividido
    
    # Asignar cada gráfico a una posición en el lienzo
    ax0 = fig.add_subplot(grid[0, 0]) # Fila 1, Columna 1: Géneros
    ax1 = fig.add_subplot(grid[0, 1]) # Fila 1, Columna 2: Categorías
    ax2 = fig.add_subplot(grid[1, :])  # Fila 2, Tendencia Temporal
    
    # Subplot 1
    # Comparación por Género
    # Ventas acumuladas por género
    sns.barplot(data=df, x='Gender', y='Total Amount', ax=ax0, palette='viridis', hue='Gender', estimator=sum, legend=False)
    
    # Leyenda manual con los mismos colores --> Parche
    colores_g = [patch.get_facecolor() for patch in ax0.patches][:len(promedios_genero)]
    custom_handles_g = [mpatches.Patch(color=colores_g[i], label=f"{gen} (Prom: ${promedios_genero[gen]:,.2f})") for i, gen in enumerate(promedios_genero.index)]
    
    # Diseño, etiquetas y leyenda
    ax0.legend(handles=custom_handles_g, title='Métrica por Género', loc='upper right', fontsize=10)
    ax0.set_title('A. Ventas Totales por Género', fontsize=12, fontweight='bold', pad=10)
    ax0.set_xlabel('Género')
    ax0.set_ylabel('Monto Total ($)')
    ax0.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Subplot 2
    # Comparación por Categoría
    # Ventas acumuladas por Categoría
    sns.barplot(data=df, x='Product Category', y='Total Amount', ax=ax1, palette='magma', hue='Product Category', estimator=sum, legend=False)
    
    # Leyenda manual con los mismos colores --> Parche
    colores_c = [patch.get_facecolor() for patch in ax1.patches][:len(promedios_cat)]
    custom_handles_c = [mpatches.Patch(color=colores_c[i], label=f"{cat} (Prom: ${promedios_cat[cat]:,.2f})") for i, cat in enumerate(promedios_cat.index)]

    # Diseño, etiquetas y leyenda
    ax1.legend(handles=custom_handles_c, title='Métrica por Categoría', loc='upper right', fontsize=10)
    ax1.set_title('B. Ventas Totales por Categoría de Producto', fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel('Categoría')
    ax1.set_ylabel('Monto Total ($)')
    ax1.grid(axis='y', linestyle='--', alpha=0.8)
    
    # Subplot 3: Tendencia Temporal
    ax2.plot(resumen_temporal.index, resumen_temporal.values, marker='s', color='#E63946', linewidth=2, label='Ventas Mensuales Acumuladas')
    
    # Monto máximo y fecha
    max_val = resumen_temporal.max()
    max_date = resumen_temporal.idxmax()
    
    # Cartel con texto
    ax2.annotate(f'Máximo Histórico\n${max_val:,.2f}',
                 xy=(max_date, max_val), # coordenadas exactas en el máx
                 xytext=(max_date + pd.Timedelta(days=20), max_val * 0.95), # coordenadas del cuadro, desplazado
                 arrowprops=dict(arrowstyle="->", color="#4A5568", linewidth=1.5, connectionstyle="arc3,rad=-0.1"), # Flecha
                 fontsize=11, fontweight='bold', color='darkred', 
                 bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)) # Contenedor de texto

    # Diseño, etiquetas y leyenda
    ax2.set_title('C. Tendencia Temporal de Ventas con Identificación de Hitos', fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel('Fecha de Registro')
    ax2.set_ylabel('Monto Total Acumulado ($)')
    ax2.grid(True, which='both', linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left', frameon=True)
    
    # Título general
    plt.suptitle('Comparación de Ventas por Género y Categoría, y Evolución Temporal', fontsize=16, fontweight='bold', y=0.96)
    plt.show()