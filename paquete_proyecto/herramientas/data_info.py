import pandas as pd


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
