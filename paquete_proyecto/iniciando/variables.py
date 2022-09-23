import pandas as pd

# PAQUETE 2


def ajustar_tipos(data):
    for i, label in enumerate(list(data.columns)):
        if label == "Empleado":
            data[label] = data[label].astype(int)
        elif label == "CodigoFamilia":
            data[label] = data[label].astype(int)
        elif label == "Cantidad":
            data[label] = data[label].astype(int)
        elif label == "Ventas":
            data[label] = data[label].astype(float)
        elif label == "Area":
            data[label] = data[label].astype(int)

    return data
