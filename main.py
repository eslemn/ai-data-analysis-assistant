import pandas as pd
from cleaner import clean_data
from analyzer import analyze_data
from health import calculate_health_score
from llm_report import generate_llm_report


def main():
    print("Dataset loading...")

    # CSV yükle
    df = pd.read_csv("data.csv")

    print("\nFirst rows:")
    print(df.head())

    # Veri temizleme
    print("\nCleaning data...")
    df = clean_data(df)

    # Analiz
    print("\nRunning analysis...")
    analysis_summary = analyze_data(df)

    print("\nAnalysis Summary:")
    print(analysis_summary)

    # Araç sağlık skoru
    df = calculate_health_score(df)

    print("\nVehicle Health Scores:")
    print(df[["vehicle_id", "health_score"]])

    # LLM raporu
    print("\nGenerating AI report...")
    report = generate_llm_report(analysis_summary)

    print("\n===== AI VEHICLE REPORT =====")
    print(report)

    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()
