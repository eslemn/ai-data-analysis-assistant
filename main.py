import pandas as pd

print("Dataset loading...")

df = pd.read_csv("data.csv")

print("\nDataset Summary")
print("-----------------")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nMissing Values:")
missing = df.isnull().sum()
print(missing)

print("\nStatistical Summary:")
print(df.describe())

print("\nAutomatic Comments:")
for column in missing.index:
    if missing[column] > 0:
        print(f"- Column '{column}' has missing values.")

print("\nAnalysis completed.")
