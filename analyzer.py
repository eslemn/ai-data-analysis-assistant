def analyze_data(df):
    print("\nDataset Info:")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nStatistical Summary:")
    summary = df.describe()

    print(summary)

    return summary
