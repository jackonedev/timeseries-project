import pandas as pd
import re


def return_match_id(data: pd.DataFrame, col_name: str, patrones: dict) -> dict:
    match_id = {}
    all_indexes = []
    for llave in patrones.keys():
        if llave == "otros":
            continue
        regex = re.compile(patrones[llave])
        regex_search = data[col_name].apply(lambda x: regex.search(str(x)))
        match_id[llave] = regex_search.dropna().apply(lambda x: x.group(0)).index
        all_indexes += list(match_id[llave])
    match_id["otros"] = data.index.drop(all_indexes)

    return match_id


def category_apply(
    data: pd.DataFrame, indice_categorias: dict[str, str]
) -> pd.DataFrame:
    def counter(start=1):
        while True:
            yield start
            start += 1

    def set_label():
        x = counter()
        label = "category_" + str(next(x))
        while True:
            if (pd.DataFrame([label]).isin(data.columns)).values:
                label = "category_" + str(next(x))
            elif next(x) == 100:
                break
            else:
                return label

    label = set_label()
    data.loc[:, label] = 0
    for elemento in indice_categorias:
        data.loc[indice_categorias[elemento], label] = elemento
    return data


def merge_category(
    data: pd.DataFrame, feature: pd.DataFrame, shared_label: str, feature_label: str
) -> pd.DataFrame:
    """Ejmplo de implementacion

    merge_category(data, feature_categoria, 'Id', 'category_2')
    """

    def make_merge(
        data=data,
        feature=feature,
        shared_label=shared_label,
        feature_label=feature_label,
    ):
        return pd.merge(
            left=data, right=feature[feature_label], how="outer", on=shared_label
        )

    def make_merge_reseting_index(
        data=data,
        feature=feature,
        shared_label=shared_label,
        feature_label=feature_label,
    ):
        index_label: str = data.reset_index(drop=False).columns[0]
        return pd.merge(
            left=data.reset_index(drop=False),
            right=feature[feature_label],
            how="outer",
            on=shared_label,
        ).set_index(index_label)

    if not isinstance(data.index, pd.core.indexes.datetimes.DatetimeIndex):
        return make_merge()
    return make_merge_reseting_index()
