import pandas as pd

def run_basic_eda(filepath: str):
    df = pd.read_csv(filepath)
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "describe": df.describe().to_dict()
    }
