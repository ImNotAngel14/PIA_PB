import json
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATOS = RUTA_PROYECTO / "datos"


def quicksort(productos):
    if len(productos) <= 1:
        return productos

    pivote = productos[len(productos) // 2]["cantidad"]
    menores = [p for p in productos if p["cantidad"] < pivote]
    iguales = [p for p in productos if p["cantidad"] == pivote]
    mayores = [p for p in productos if p["cantidad"] > pivote]

    return quicksort(menores) + iguales + quicksort(mayores)


def cargar_productos():
    with open(RUTA_DATOS / "datos_limpios.json", "r", encoding="utf-8") as f:
        return json.load(f)


def calcular_estadisticas(productos):
    productos_gramos = [
        p for p in productos
        if p["cantidad"] is not None and p["unidad"] == "g"
    ]
    ordenados = quicksort(productos_gramos)
    cantidades = [p["cantidad"] for p in ordenados]
    total = len(cantidades)

    if total == 0:
        return None

    promedio = sum(cantidades) / total
    if total % 2 == 0:
        mediana = (cantidades[total // 2 - 1] + cantidades[total // 2]) / 2
    else:
        mediana = cantidades[total // 2]

    varianza = sum((c - promedio) ** 2 for c in cantidades) / total

    return {
        "total_productos": len(productos),
        "marcas_diferentes": len({p["marca"] for p in productos}),
        "sin_cantidad": sum(1 for p in productos if p["cantidad"] is None),
        "con_gramos": total,
        "promedio": promedio,
        "mediana": mediana,
        "minimo": cantidades[0],
        "maximo": cantidades[-1],
        "rango": cantidades[-1] - cantidades[0],
        "desviacion": varianza ** 0.5,
        "ordenados": ordenados,
    }


def main():
    stats = calcular_estadisticas(cargar_productos())

    if stats is None:
        print("No hay productos disponibles para el analisis.")
        return None

    print("=== ANALISIS DE PRODUCTOS ===")
    print(f"Total de productos: {stats['total_productos']}")
    print(f"Marcas diferentes: {stats['marcas_diferentes']}")
    print(f"Productos sin cantidad: {stats['sin_cantidad']}")
    print(f"Productos con cantidad en gramos: {stats['con_gramos']}")

    print("\n=== ESTADISTICAS DE CANTIDADES ===")
    print(f"Promedio: {stats['promedio']:.2f} g")
    print(f"Mediana: {stats['mediana']:.2f} g")
    print(f"Minimo: {stats['minimo']} g")
    print(f"Maximo: {stats['maximo']} g")
    print(f"Rango: {stats['rango']:.2f} g")
    print(f"Desviacion estandar: {stats['desviacion']:.2f} g")

    print("\n=== PRODUCTOS ORDENADOS POR CANTIDAD ===")
    for p in stats["ordenados"][:10]:
        print(f'{p["nombre"]} - {p["cantidad"]} {p["unidad"]}')

    return stats


if __name__ == "__main__":
    main()