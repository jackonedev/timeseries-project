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


class ColateColumn:
    """
    La columna "colate", debe entrar atras que la columna "label". Usamos un pd.reindex()
    """

    def __init__(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Ayuda para cambiar el orden de las columnas:

        Funciona de izquierda a derecha

        ColateColumn(dataset).vos(label_1).aca(label_2)

        label_1 se cuela delante de label_2

        """

        self.dataset = dataset

    def vos(self, colate: str):
        self.colate = colate
        return self

    def aca(self, aca: str):
        # Creo un diccionario que tiene key: label- value: index
        dicto = {}
        for i, elemento in enumerate(list(self.dataset.columns)):
            dicto[elemento] = i

        if dicto[aca] < dicto[self.colate]:
            for elemento in dicto.keys():
                if (
                    dicto[elemento] > dicto[aca]
                    and dicto[elemento] < dicto[self.colate]
                ):
                    dicto[elemento] += 1

            dicto[self.colate] = dicto[aca]
            dicto[aca] += 1
            llaves = pd.Series(dicto).sort_values().index
            return self.dataset.reindex(llaves, axis=1)


def definir_indice_temporal(data):
    """Ayuda para la funcion definir_indice_temporal
    Cuando se invoca, elige la primera columna que encuentra tipo datetime como índice.
    Si no encuentra devuelve el objeto original.
    """

    def chequear_tipo(serie):
        """Aclaración sobre esta funcion:
        El formato 'datetime64[ns]' es el estandar que sale de adjust_type().

        Chequear "paquete_proyecto.herramientas.adjust_type"
        """
        for i, elemento in enumerate(serie.values):
            if elemento == "datetime64[ns]":
                return list(serie.index)[i]
        return False

    label = chequear_tipo(data.dtypes)

    if label:
        data[label] = pd.to_datetime(data[label], infer_datetime_format=True)
        data.sort_values(by=label, inplace=True)
        return data.set_index(label)
    return data


def setear_tipo(data, label, dtype):
    try:
        data[label] = data[label].astype(dtype)
    except:
        pass
    return data
