from pprint import pprint
import pandas as pd
from paquete_proyecto.iniciando.bases import importar_databases
from paquete_proyecto.iniciando.variables import ajustar_tipos

# PROGRAMA PRINCIPAL


def main():
    ventas, ventas_2 = importar_databases()
    ventas, ventas_2 = ajustar_tipos(ventas), ajustar_tipos(ventas_2)
    pprint(ventas)


if __name__ == "__main__":
    main()
