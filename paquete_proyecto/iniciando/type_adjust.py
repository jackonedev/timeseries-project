import pandas as pd
import pandas

def type_adjust(data):
    """type_adjust()

    Keyword arguments:
    data: pandas.DataFrame -- Selecciona cada una de las columnas, y las evalua para elegir el mejor datatype:

        1ro: str -> float
            función 1: prueba cambio directo float(x)
            funcion 2: intenta eliminando el "." y cambiando la "," por "."
        2do: float -> int
            función 3: si para cada fila x // int(x) == 0 entonces int(x)
        3: str -> datetime
            función 4: para las columnas object restantes pd.to_datetime()

    Return: pandas.DataFrame -- Con las columnas modificadas
    """
    index = get_index_name(data)
    data.reset_index(drop=False, inplace=True)
    data = convert_object_to_datetime(data)
    data = convert_object_to_float(data)
    data = convert_object_to_float_2(data)
    data = convert_float_to_int(data)
    return data.set_index(index, drop=True)


def get_index_name(data):
    if isinstance(data.index.name, type(None)):
        return 'index'
    else:
        return data.index.name


## FROM STRING TO ANOTHER TYPE
def check_object_type(data: pandas.DataFrame) -> list[str]:
    cols_mask = (data.dtypes== 'object').values
    return data.loc[:, cols_mask].columns.values


def convert_object_to_datetime(data: pandas.DataFrame) -> pandas.DataFrame:
    cols = check_object_type(data)
    for label in cols:
        try:
            data[label] = pd.to_datetime(data[label], infer_datetime_format=True)
        except:
            pass
    return data


def convert_object_to_float(data: pandas.DataFrame) -> pandas.DataFrame:
    cols = check_object_type(data)
    for label in cols:
        try:
            data[label] = data[label].astype(float)
        except:
            pass
    return data


def convert_object_to_float_2(data: pandas.DataFrame) -> pandas.DataFrame:
    cols = check_object_type(data)
    for label in cols:
        try:
            data[label] = data[label].apply(lambda x: x.replace('.', '').replace(',', '.'))
            data[label] = data.astype(float)
        except:
            pass
    return data


## FROM FLOAT TO INT
def check_float_type(data: pandas.DataFrame) -> list[str]:
    cols_mask = (data.dtypes== 'float').values
    return data.loc[:, cols_mask].columns.values

def convert_float_to_int(data):
    cols = check_float_type(data)
    for label in cols:
        if (data[label] % data[label].astype(int)).sum() == 0.0:
            data[label] = data[label].astype(int)
    return data




# if __name__ == '__main__':
#     string = '1.350,05'
#     print (string.replace('.', '').replace(',', '.'))