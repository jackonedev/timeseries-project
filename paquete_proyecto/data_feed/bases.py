import pandas as pd
from paquete_proyecto.herramientas.extra import (
    check_underscore,
    definir_indice_temporal,
    setear_tipo,
)

from paquete_proyecto.herramientas.type_adjust import type_adjust


# FUNCION 2: DE SALIDA DE ETAPA DATA FEED


def ajustes_finales(data):
    """
    Función para ajustar los tipos de variables al formato deseado, de forma manual.
    """
    # for label in list(data.columns):
    #     if label == "Ventas":
    #         data[label] = data[label].astype(float)

    # # Cambiamos el tipo de variable de la columna
    data = setear_tipo(data, "Ventas", float)

    # Chequeamos que el nombre de las columnas no tenga espacios en blanco " "
    data = check_underscore(data)

    # Definimos indice_temporal
    data = definir_indice_temporal(data)

    return data


# FUNCION 1: DE ENTRADA A ETAPA DATA FEED


def importar_databases():
    """Bases de datos para el proyecto:

    Return: tuple = (ventas, ventas_sin_duplicados)
    """

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

    # Abrimos la base de datos
    file_path = "./src/Ventas.csv"
    ventas = pd.read_csv(file_path, sep=";", low_memory=False)

    # Aplicamos mascara 1, y separamos con y sin duplicados
    ventas = mascara_1(ventas, "NombreCliente")
    ventas_sin_duplicados = ventas.drop_duplicates()

    # Eliminamos valores inconsistentes
    ventas = eliminar_valores_inconsistente(ventas, "Cantidad")
    ventas_sin_duplicados = eliminar_valores_inconsistente(
        ventas_sin_duplicados, "Cantidad"
    )

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
