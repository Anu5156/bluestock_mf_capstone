import pandas as pd
bench = pd.read_csv("data/raw/10_benchmark_indices.csv")
print("Columns:", list(bench.columns))
print("Shape:", bench.shape)
print(bench.head(10))
for col in bench.columns:
    if bench[col].dtype == "object":
        print(f"{col} unique:", bench[col].unique()[:10])
