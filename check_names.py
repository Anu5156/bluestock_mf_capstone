import pandas as pd
bench = pd.read_csv("data/raw/10_benchmark_indices.csv")
print("All index names:", bench["index_name"].unique())
