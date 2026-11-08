from modulos import api_cliente, limpiador_datos, analizador, exportador

def main():
    print("=== PROYECTO INTEGRADOR ===\n")

    print("1. Consultando API...")
    api_cliente.main()

    print("\n2. Limpiando datos...")
    limpiador_datos.main()

    print("\n3. Analizando datos...")
    analizador.main()

    print("\n4. Exportando a Excel...")
    exportador.main()

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()