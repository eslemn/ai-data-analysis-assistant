import pandas as pd
from cleaner import clean_data
from analyzer import analyze_data
from health import  RuleBasedHealthStrategy, HealthContext
from recommendation import generate_recommendations
from report_factory import ReportFactory
from observer import VehicleMonitor, MaintenanceNotifier, DashboardNotifier
from prediction import predict_failures


def main():
    print("Dataset loading...")

    # CSV yükle
    df = pd.read_csv("data.csv")

    print("\nMissing values BEFORE cleaning:")
    print(df.isnull().sum())

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

    # Strategy Pattern
    strategy = RuleBasedHealthStrategy()  #health score hesaplama türü seçimi
    health_context = HealthContext(strategy)    #seçilen stratejiyi kullanan context sınıfı
    df = health_context.calculate_health_score(df)

    df = predict_failures(df)
    # Recommendation
    df = generate_recommendations(df)   #araçların sensör verilerine göre bakım önerileri eklenmesi

    print("\nVehicle Health Results:")
    print(df[["vehicle_id", "health_score", "status","failure_risk_score","risk_level","predicted_fault", "maintenance_recommendation"]])

    # Observer Pattern
    monitor = VehicleMonitor()   #araçları kontrol eden ana yapı
    monitor.attach(MaintenanceNotifier())    #bakım ekibine haber verecek yapı   attach ile gözlemcileri bağlıyosun kritik durum olursa
    monitor.attach(DashboardNotifier())     #ekrana dashboarda bilgi verecek yapı  attach ile gözlemcileri bağlıyosun kritik durum olursa
    monitor.check_critical_vehicles(df)     #dataframe içindeki kritik durumdaki araçları kontrol eder ve gözlemcilere haber verir

    # Factory Method Pattern
    report_generator = ReportFactory.create_report_generator("llm")
    report = report_generator.generate(analysis_summary, df)

    print("\n===== AI VEHICLE REPORT =====")
    print(report)

    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()