import pandas as pd
from paquete_proyecto.herramientas.extra import (
    str_to_float,
    check_underscore,
    ColateColumn,
)
from paquete_proyecto.herramientas.type_adjust import type_adjust


# FUNCION 2


def ajustes_finales(data):
    """
    Función para ajustar los tipos de variables al formato deseado, de forma manual.
    """
    # Cambiamos el tipo de variable de la columna
    for label in list(data.columns):
        if label == "Ventas":
            data[label] = data[label].astype(float)

    # Chequeamos que el nombre de las columnas no tenga espacios en blanco " "
    data = check_underscore(data)

    # Cambiamos el orden de las columnas
    data = ColateColumn(data).vos("Id").aca("IdCliente")

    return data


# FUNCION 1


def importar_databases():
    """Bases de datos para el proyecto:

    Return: tuple = (ventas, ventas_sin_duplicados)
    """

    # Abrimos la base de datos
    file_path = "./id_for_ideas/Ventas.csv"
    ventas = pd.read_csv(file_path, sep=";", low_memory=False)

    # Aplicamos mascara 1, y separamos con y sin duplicados
    ventas = mascara_1(ventas, "NombreCliente")
    ventas_sin_duplicados = ventas.drop_duplicates()

    # Eliminamos valores inconsistentes
    ventas = eliminar_valores_inconsistente(ventas, "Cantidad")
    ventas_sin_duplicados = eliminar_valores_inconsistente(
        ventas_sin_duplicados, "Cantidad"
    )

    # # Creamos el indice para temporal
    ventas = definir_indice_temporal(ventas, "Fecha")
    ventas_sin_duplicados = definir_indice_temporal(ventas_sin_duplicados, "Fecha")

    # Agrego la columna ID para RegEx
    ventas.reset_index(drop=False, inplace=True)
    ventas.reset_index(drop=False, inplace=True)
    ventas.set_index("Fecha", drop=True, inplace=True)
    ventas.loc[:, "Id"] = ventas["index"] + 1
    ventas.drop(columns="index", inplace=True)

    ventas_sin_duplicados.reset_index(drop=False, inplace=True)
    ventas_sin_duplicados.reset_index(drop=False, inplace=True)
    ventas_sin_duplicados.set_index("Fecha", drop=True, inplace=True)
    ventas_sin_duplicados.loc[:, "Id"] = ventas_sin_duplicados["index"] + 1
    ventas_sin_duplicados.drop(columns="index", inplace=True)

    return type_adjust(ventas), type_adjust(ventas_sin_duplicados)


def mascara_1(data, label):
    """Para quitar una clase extraña de NaN's. Todo lo que no sea un string, se elimina"""
    mascara = []
    for elemento in data[label].values:
        mascara.append(type(elemento))

    for i, elemento in enumerate(mascara):
        if elemento == str:
            mascara[i] = True
        else:
            mascara[i] = False

    return data.loc[mascara]


def eliminar_valores_inconsistente(data, label):
    data.loc[data[label] == "1,068", label] = 1
    data.loc[data[label] == "1,006", label] = 1
    return data


def sequence(start=1):
    while True:
        yield start
        start += 1


cont = sequence()


def definir_indice_temporal(data, label):
    global cont
    time_serie = pd.to_datetime(data[label], infer_datetime_format=True)
    # print(f"La longitud de la serie Nº {next(cont)} es de: {len(time_serie)}")
    data[label] = time_serie
    data.sort_values(by=label, inplace=True)
    return data.set_index(label)
