import pandas as pd
df = pd.read_csv( 'winequality-red.csv')
filtered_df = df[df['quality'] >= 6]
print(filtered_df.sort_values('quality', ascending=False))