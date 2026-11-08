"""
Módulo: graficas.py
Descripción: Genera gráficas a partir de los datos analizados.

Autor: Kenia Janett Arcivar Vazquez
Matrícula: 0000000
Rol: Programador
Materia: Programación Básica
Fecha: 07/11/2026
"""
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

from modulos.analizador import cargar_productos, calcular_estadisticas

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_GRAFICAS = RUTA_PROYECTO / "graficas"

def grafica_barras(productos):
    # PRIMERA GRAFICA: LAS 10 MARCAS CON MAS PRODUCTOS
    conteo_marcas = Counter()

    for producto in productos:  # SE RECORREN LOS PRODUCTOS UNO POR UNO
        marca = producto["marca"]  # SE OBTIENE LA MARCA DE CADA PRODUCTO
        conteo_marcas[marca] += 1  # SE SUMA 1 AL CONTADOR DE ESA MARCA

    marcas = conteo_marcas.most_common(10)  # LAS 10 MARCAS MAS COMUNES

    nombres_marcas = [marca for marca, cantidad in marcas]  # NOMBRES DE LAS MARCAS
    cantidades = [cantidad for marca, cantidad in marcas]  # CUANTOS PRODUCTOS TIENE CADA UNA

    print("\nMarcas más comunes:", nombres_marcas)
    print("Cantidades:", cantidades)

    plt.figure(figsize=(10, 6))  # TAMAÑO DE LA GRAFICA
    plt.bar(nombres_marcas, cantidades, color="yellow")  # CREA LAS BARRAS

    plt.title("Las 10 marcas con más productos")
    plt.xlabel("Marcas")  # EJE HORIZONTAL
    plt.ylabel("Cantidad de productos")  # EJE VERTICAL

    plt.xticks(rotation=45)  # SE INCLINAN LOS NOMBRES PARA QUE NO SE EMPALMEN
    plt.tight_layout()  # SE ACOMODAN LOS ELEMENTOS

    plt.savefig(RUTA_GRAFICAS / "grafica_barras.png", dpi=300)  # SE GUARDA EN PNG
    plt.show()


def grafica_lineas(stats):
    # SEGUNDA GRAFICA: DISTRIBUCION DE PRODUCTOS POR GRAMOS
    # stats["ordenados"] YA TRAE SOLO LOS PRODUCTOS EN GRAMOS Y ORDENADOS POR EL ANALIZADOR
    cantidades = [p["cantidad"] for p in stats["ordenados"]]

    print("\nProductos con cantidad en gramos:", len(cantidades))

    conteo_gramos = Counter()

    for cantidad in cantidades:
        intervalo = int(cantidad // 50) * 50  # INTERVALOS DE 50 EN 50
        conteo_gramos[intervalo] += 1

    # COMO ESTA ORDENADO, EL ULTIMO ES EL MAXIMO: SE CREAN TODOS LOS INTERVALOS DE 0 HASTA AHI
    maximo = int(cantidades[-1] // 50) * 50
    intervalos = range(0, maximo + 50, 50)

    nombres_intervalos = [f"{inicio}-{inicio + 49} g" for inicio in intervalos]
    cantidades_intervalos = [conteo_gramos.get(inicio, 0) for inicio in intervalos]  # 0 SI ESTA VACIO

    print(nombres_intervalos)
    print(cantidades_intervalos)

    plt.figure(figsize=(12, 6))
    plt.plot(nombres_intervalos, cantidades_intervalos, marker="s", color="green")

    plt.title("Distribución de productos según su contenido en gramos")
    plt.xlabel("Rango de gramos")
    plt.ylabel("Cantidad de productos")

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(RUTA_GRAFICAS / "grafica_lineas.png", dpi=300)
    plt.show()


def main(stats=None):
    RUTA_GRAFICAS.mkdir(exist_ok=True)

    productos = cargar_productos()
    print("Cantidad de productos:", len(productos))

    # SI main.py YA CORRIO EL ANALIZADOR, SE REUTILIZAN SUS RESULTADOS
    if stats is None:
        stats = calcular_estadisticas(productos)

    grafica_barras(productos)  # LAS BARRAS CUENTAN TODOS LOS PRODUCTOS, NO SOLO LOS DE GRAMOS

    if stats is None:
        print("No hay productos en gramos para la gráfica de líneas.")
    else:
        grafica_lineas(stats)


if __name__ == "__main__":
    main()