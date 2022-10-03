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
