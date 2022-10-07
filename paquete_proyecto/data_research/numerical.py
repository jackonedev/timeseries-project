import numpy as np
import pandas as pd


class TimeSerieTarget:
    def __init__(self, target: pd.Series) -> None:
        self.targets = self.prepare(target)

    @staticmethod
    def prepare(target: pd.Series) -> pd.DataFrame:
        if target.dtype == "float64":
            result = target.groupby(target.index).sum().to_frame()
            result[f"log_{target.name}"] = np.log(result)
            result[f"log_{target.name}"][result[f"log_{target.name}"] == -np.inf] = 0
            result[f"accum_{target.name}"] = result[[target.name]].cumsum()

        elif target.dtype == "int32":
            result = target.groupby(target.index).sum().to_frame()
            result[f"accum_{target.name}"] = result[[target.name]].cumsum()

        else:
            return
        return result
