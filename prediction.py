from config import Config


def predict_failures(df):
    print("\nPredicting possible vehicle failures...")

    config = Config()

    failure_risk_scores = []
    risk_levels = []
    predicted_faults = []

    for _, row in df.iterrows():
        risk_score = 0
        vehicle_faults = []

        # Tekil riskler
        if row["engine_temp"] > config.engine_temp_threshold:
            risk_score += 20

        if row["battery_voltage"] < config.battery_voltage_threshold:
            risk_score += 15
            vehicle_faults.append("Battery system issue")

        if row["brake_wear"] > config.brake_wear_threshold:
            risk_score += 20
            vehicle_faults.append("Brake maintenance required")

        if row["vibration"] > config.vibration_threshold:
            risk_score += 15

        if row["oil_quality"] < config.oil_quality_threshold:
            risk_score += 10
            vehicle_faults.append("Oil system degradation")

        if row["tire_pressure"] < config.tire_pressure_threshold:
            risk_score += 10
            vehicle_faults.append("Tire pressure issue")

        if row["mileage"] > config.mileage_threshold:
            risk_score += 10

        # Kombinasyon riskleri
        if row["engine_temp"] > config.engine_temp_threshold and row["vibration"] > config.vibration_threshold:
            risk_score += 20
            vehicle_faults.append("Possible engine failure")

        if row["battery_voltage"] < config.battery_voltage_threshold and row["mileage"] > config.mileage_threshold:
            risk_score += 10
            vehicle_faults.append("Electrical system wear risk")

        if row["brake_wear"] > config.brake_wear_threshold and row["speed"] > config.speed_threshold:
            risk_score += 10
            vehicle_faults.append("High brake safety risk")

        # Fault yoksa
        if not vehicle_faults:
            vehicle_faults.append("No immediate fault predicted")

        # Risk level belirleme
        if risk_score >= 60:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        failure_risk_scores.append(risk_score)
        risk_levels.append(risk_level)
        predicted_faults.append(", ".join(vehicle_faults))

    df["failure_risk_score"] = failure_risk_scores
    df["risk_level"] = risk_levels
    df["predicted_fault"] = predicted_faults

    return df