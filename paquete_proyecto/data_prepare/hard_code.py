import pandas

from paquete_proyecto.herramientas.extra import ColateColumn


def hard_category_id(data: pandas.DataFrame, name: str = "Id") -> pandas.DataFrame:
    """Ayuda para entender la funcion hard_category_id

    Es un criterio de categorización rígido, impuesto por el analista.

    Es NECESARIO QUE LA FUNCION TENGA UN INDICE TIPO DATETIME
    """
    index_label = data.reset_index(drop=False).columns[0]
    first_col_label = data.reset_index(drop=False).columns[1]

    data.reset_index(drop=False, inplace=True)
    data.reset_index(drop=False, inplace=True)
    index_col = data.columns[0]
    data.set_index(index_label, drop=True, inplace=True)
    data.loc[:, name] = data[index_col] + 1
    data = data.drop(columns=index_col)

    # Cambiamos el orden de las columnas
    data = ColateColumn(data).vos(name).aca(first_col_label)
    return data


def hard_category_1(data: pandas.DataFrame, label='category1') -> pandas.DataFrame:
    """Ayuda para entender la funcion hard_category_1

    Es un criterio de categorización rígido, impuesto por el analista.
    """

    data.loc[
        (data.Familia == "SERVICIOS") | (data.Familia == "REENCAUCHE"), label
    ] = "servicio"
    data[label] = data[label].fillna("producto")
    return data
