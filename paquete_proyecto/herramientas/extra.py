import pandas as pd


def str_to_float(serie):
    eliminar_punto = lambda x: x.replace(".", "")
    reemplazar_coma = lambda x: x.replace(",", ".")
    result = list(serie.values)
    result = list(map(eliminar_punto, result))
    result = list(map(reemplazar_coma, result))
    result = pd.Series(data=result, index=serie.index)
    return result


def check_underscore(df):
    cols = list(df.columns)
    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")
    df.columns = cols
    return df
