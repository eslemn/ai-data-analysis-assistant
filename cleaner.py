def clean_data(df):
    print("\nCleaning data...")

    print("\nHandling missing values...")

    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        df[col] = df[col].fillna(df[col].mean())

    return df
