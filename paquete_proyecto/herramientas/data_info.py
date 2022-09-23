import pandas as pd

# EXTRACTOS DE OTROS TRABAJOS


def data_info(data, name="data", order_by=None):
    """Funcion que devuelve informacion de un DataFrame en formato tipo DataFrame
    order_by: None por default- acepta: "type"
    """
    df = pd.DataFrame(pd.Series(data.columns))
    df.columns = ["columna"]
    df.columns.name = f"info de {name}"
    # df.index.name = 'index'
    df["type"] = data.dtypes.values
    df["count"] = data.count().values
    # df["count_pct"] = round(data.notna().astype(int).sum() / data.shape[0] * 100, 2).astype(str) + " %"
    df["NaN"] = data.isna().sum().values
    df["NaN_pct"] = round(df["NaN"] / data.shape[0] * 100, 2).astype(str) + " %"
    df["unique"] = [len(data[elemento].value_counts()) for elemento in data.columns]
    df["unique_pct"] = round(df["unique"] * 100 / len(data), 2).astype(str) + " %"

    if order_by == "type":
        df = df.sort_values(by=["type", "unique"])
        df = df.reset_index(drop=True)
    return df


# def check_underscore(df):
#     cols = list(df.columns)
#     for i, elemento in enumerate(cols):
#         cols[i] = cols[i].replace(" ", "_")
#     df.columns = cols
#     return df


def str_to_float(serie):
    eliminar_punto = lambda x: x.replace(".", "")
    reemplazar_coma = lambda x: x.replace(",", ".")
    result = list(serie.values)
    result = list(map(eliminar_punto, result))
    result = list(map(reemplazar_coma, result))
    result = pd.Series(data=result, index=serie.index)
    return result


# def check_type_str(dataset):  # for load_dataset
#     cols_mask = (dataset.dtypes == "object").values
#     cols_obj = dataset.loc[:, cols_mask].columns.values
#     posibles_dt = []
#     if len(cols_obj) == 0:
#         return print('No hay columnas tipo "object"')
#     for i, elemento in enumerate(cols_obj):
#         try:
#             pd.to_datetime(dataset[elemento], infer_datetime_format=True)
#             posibles_dt.append(elemento)
#         except:
#             pass
#     return select_type_dt(dataset, posibles_dt)


# def select_type_dt(dataset, cols_dt):  # used above in check_type_str and check_type_dt
#     indice = list(dataset.loc[:, cols_dt].columns)
#     if len(indice) == 1:
#         return indice[0]
#     for i in range(len(indice)):
#         indice[i] = str(i + 1) + ") {}".format(indice[i])
#     print(">> SELECCION DE SERIE DE TIEMPO:")
#     for i in range(len(indice)):
#         print(indice[i])
#     op = input(">> ")
#     try:
#         op = int(op) - 1  # para empezar a contar desde cero
#         indice = list(dataset.loc[:, cols_dt].columns)[op]
#         return indice
#     except:
#         print("\nERROR: La opcion ingresada no corresponde\n")
#         return


# def check_type_dt(dataset):  # for VectorBuilding.__init__
#     if isinstance(dataset.index, pd.core.indexes.datetimes.DatetimeIndex):
#         print(f"\nSerie de tiempo: {dataset.index.name}\n")
#         return dataset
#     else:
#         cols_dt = (dataset.dtypes == "<M8[ns]").values
#         if cols_dt.sum() == 0:
#             indice = check_type_str(dataset)
#             print(f"\nSerie de tiempo: {indice}\n")
#             dataset[indice] = pd.to_datetime(
#                 dataset[indice], infer_datetime_format=True
#             )
#             return dataset.set_index(indice)
#         elif cols_dt.sum() == 1:
#             indice = list(dataset.loc[:, cols_dt].columns)[0]
#             print(f"\nSerie de tiempo: {indice}\n")
#             return dataset.set_index(indice)
#         else:
#             indice = select_type_dt(dataset, cols_dt)
#             print(f"\nSerie de tiempo: {indice}\n")
#             return dataset.set_index(indice)


# def load_dataset(file_name, freq: str = None, dropnan=False, fillnan=False):
#     try:
#         df = pd.read_csv(file_name)
#     except:
#         df = pd.read_csv(file_name, sep=";")
#     df = check_underscore(df)
#     df = check_type_dt(df)
#     if freq != None:
#         df = df.asfreq(freq=freq)
#     if dropnan:
#         print("Cantidad de NaNs en: \n" + df.isna().sum().to_string())
#         if df.isna().sum().sum() > 0:
#             df = df.dropna()
#             print("NaNs eliminados\n")
#     if fillnan:
#         print("Cantidad de NaNs en: \n" + df.isna().sum().to_string())
#         df.fillna(method="bfill", inplace=True)
#         print('NaNs imputados: método "backfill"')
#     return df
