from modulos import api_cliente, limpiador_datos


def main():
    print("=== PROYECTO INTEGRADOR ===\n")

    print("1. Consultando API...")
    api_cliente.main()

    print("\n2. Limpiando datos...")
    limpiador_datos.main()

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()
