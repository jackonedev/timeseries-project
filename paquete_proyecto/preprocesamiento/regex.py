import pandas as pd
import re

def return_match_id(data: pd.DataFrame, col_name: str, patrones: dict) -> dict:
    match_id = {}
    all_indexes = []
    for llave in patrones.keys():
        if llave == 'otros':
            continue
        regex = re.compile(patrones[llave])
        regex_search = data[col_name].apply(lambda x: regex.search(str(x)))
        match_id[llave] = regex_search.dropna().apply(lambda x: x.group(0)).index
        all_indexes += list(match_id[llave])
    match_id['otros'] = data.index.drop(all_indexes)
    
    return match_id


def category_apply(data: pd.DataFrame, indice_categorias: dict) -> pd.DataFrame:
    def counter(start=1):
        while True:
            yield start
            start += 1

    def set_label():
        x = counter()
        label = 'category_' + str(next(x))
        while True:
            if (pd.DataFrame([label]).isin(data.columns)).values:
                label = 'category_' + str(next(x))
            elif next(x) == 100:
                break
            else:
                return label

    label = set_label()
    data.loc[:, label] = 0
    for elemento in indice_categorias:
        data.loc[indice_categorias[elemento], label] = elemento
    return data