import pandas as pd
df = pd.read_csv( 'winequality-red.csv')
grouped = df.groupby('quality')
mean_values = grouped.mean()
print(mean_values)