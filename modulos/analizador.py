
import json
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATOS = RUTA_PROYECTO / "datos"

def quicksort(productos):
    if len(productos) <= 1:
        return productos

    pivote = productos[len(productos) // 2]["cantidad"]

    menores = [
        p for p in productos
        if p["cantidad"] < pivote
    ]

    iguales = [
        p for p in productos
        if p["cantidad"] == pivote
    ]

    mayores = [
        p for p in productos
        if p["cantidad"] > pivote
    ]

    return quicksort(menores) + iguales + quicksort(mayores)


def main():
    with open(RUTA_DATOS / "datos_limpios.json", "r", encoding="utf-8") as f:
        productos = json.load(f)

    # Preparar productos con cantidad en gramos
    productos_gramos = [
        p for p in productos
        if p["cantidad"] is not None and p["unidad"] == "g"
    ]

    productos_ordenados = quicksort(productos_gramos)

    
    cantidades = [p["cantidad"] for p in productos_ordenados]

    total = len(cantidades)
    if total == 0:
        print("No hay productos disponibles para el analisis.")
        return

    promedio = sum(cantidades) / total

    if total % 2 == 0:
        mediana = (
            cantidades[total // 2 - 1] +
            cantidades[total // 2]
        ) / 2
    else:
        mediana = cantidades[total // 2]

    minimo = cantidades[0]
    maximo = cantidades[-1]
    rango = maximo - minimo

    varianza = sum(
        (cantidad - promedio) ** 2
        for cantidad in cantidades
    ) / total

    desviacion = varianza ** 0.5

    # Estadísticas generales
    total_productos = len(productos)
    sin_cantidad = sum(1 for p in productos if p["cantidad"] is None)
    marcas = {p["marca"] for p in productos}

    print("=== ANALISIS DE PRODUCTOS ===")
    print(f"Total de productos: {total_productos}")
    print(f"Marcas diferentes: {len(marcas)}")
    print(f"Productos sin cantidad: {sin_cantidad}")
    print(f"Productos con cantidad en gramos: {len(productos_gramos)}")

    print("\n=== ESTADISTICAS DE CANTIDADES ===")
    print(f"Promedio: {promedio:.2f} g")
    print(f"Mediana: {mediana:.2f} g")
    print(f"Minimo: {minimo} g")
    print(f"Maximo: {maximo} g")
    print(f"Rango: {rango:.2f} g")
    print(f"Desviacion estandar: {desviacion:.2f} g")

    print("\n=== PRODUCTOS ORDENADOS POR CANTIDAD ===")
    for p in productos_ordenados[:10]:
        print(f'{p["nombre"]} - {p["cantidad"]} {p["unidad"]}')


if __name__ == "__main__":
    main()
