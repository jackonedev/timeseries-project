import pandas as pd  # for develop
import pandas  # for annotations
from sklearn.model_selection import TimeSeriesSplit
from paquete_proyecto.herramientas.type_adjust import type_adjust


def complete_dates(data: pandas.DataFrame, fillna='0.0') -> pandas.DataFrame:
    """Completa las fechas faltantes entre un máximo y un mínimo establecido

    Entry:
    data: DataFrame con cuyo index contiene el datetime a completar
    Return:
    DataFrame con indice expandido y NaNs en todas las filas completadas

    """
    def date_range(data: pandas.DataFrame) -> pandas.DatetimeIndex:
        """data must have DatetimeIndex in index"""
        start_date = data.index.min()
        end_date = data.index.max()
        return pd.date_range(start=start_date, end=end_date)
    def build_default_sample(
        index: pandas.DatetimeIndex, index_name: str
    ) -> pandas.DataFrame:
        date_range = index
        muestra = pd.DataFrame(
            [0.0 for i in range(len(date_range))], index=date_range, columns=["default"]
        )
        muestra.index.name = index_name
        return muestra


    dates = date_range(data)
    muestra = build_default_sample(dates, data.index.name)
    result = pd.merge(
        data.reset_index(), muestra.reset_index(), on=data.index.name, how="right"
    )
    result.set_index(data.index.name, inplace=True)
    result.fillna(value=fillna, inplace=True)
    return type_adjust(result.drop(columns="default"))


def timeseries_cv(
    data: pandas.DataFrame, n_splits: int, max_train_size: int, test_size: int
) -> list[pandas.DataFrame]:
    """Dado un DataFrame con Datetime en index, ingresar los parámetros de cortes dados por Scikit-Learn:

    https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

    Existe un parámetro "gap" que no está siendo implementado en esta función.
    """

    splitter = TimeSeriesSplit(
        n_splits=n_splits, max_train_size=max_train_size, test_size=test_size
    )
    date_range = pd.date_range(start=data.index.min(), end=data.index.max())
    train = []
    test = []  # only purpouse is to extract last element
    for train_index, test_index in splitter.split(date_range):
        concat_index, predict_index = date_range[train_index], date_range[test_index]
        train.append(data.loc[concat_index])
        test.append(data.loc[predict_index])
    # Append last element from test into train list
    train.append(test[-1])
    return train



