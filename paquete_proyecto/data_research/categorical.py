from typing import Callable
import pandas as pd


class TimeSerieBuilder:
    """Ayuda sobre la clase TimeSerieBuilder

    Parámetros del método constructivo:
        - dataset: pd.DataFrame cuyas columnas serán tratadas como categóricas
        - target: pd.Series cuyos valores deben ser numéricos y de la misma longitud que "dataset"

    Atributos de clase:
        - self.datasets: list[pd.DataFrame] cada elemento de la lista es un dataset con una variable categórica
        - self.target: pd.Series idéntico al método constructivo

    Métodos de clase:
        - transform(): modifica el atributo self.datasets, cada dataset es el resultante de aplicar "(pd.get_dummies * target).groupby(index).sum()"
        - acumulate(): modifica el atributo self.datasets, cada dataset es el resultado de aplicar "dataset.apply(lambda x: x.cumsum())"
    """

    def __init__(self, dataset: pd.DataFrame, target: pd.Series) -> None:
        self.datasets = self.prepare(dataset)
        self.target = target
        self.accumulated = []

    @staticmethod
    def prepare(dataset: pd.DataFrame) -> list[pd.DataFrame]:
        if dataset.isna().all().all():
            dataset = dataset.dropna()
        return [dataset[label].to_frame() for label in dataset.columns]

    def transform(self, func: Callable) -> None:
        dataset = iter(self.datasets)
        for i, data in enumerate(dataset):
            mask = ~(
                (data.values == 0) | (data.values == "00") | (data.values == "NaL")
            )
            dummys = pd.get_dummies(data.loc[mask].astype(str))

            self.datasets[i] = pd.DataFrame(
                dummys.values * self.target.to_frame().loc[mask].values,
                columns=dummys.columns,
                index=dummys.index,
            )
            self.datasets[i] = self.datasets[i].apply(func)

    def accumulate(self) -> None:
        for data in self.datasets:
            self.accumulated.append(data.apply(lambda x: x.cumsum()))
