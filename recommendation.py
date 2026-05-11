def generate_recommendations(df):
    print("\nGenerating maintenance recommendations...")

    recommendations = []

    for _, row in df.iterrows():
        vehicle_recommendations = []

        if row["engine_temp"] > 100:
            vehicle_recommendations.append("Engine inspection recommended")

        if row["fuel_consumption"] > 9:
            vehicle_recommendations.append("Fuel system check recommended")

        if row["mileage"] > 40000:
            vehicle_recommendations.append("General maintenance recommended")

        if row["speed"] > 110:
            vehicle_recommendations.append("Driving behavior should be monitored")

        if not vehicle_recommendations:
            vehicle_recommendations.append("Regular monitoring is sufficient")

        recommendations.append(", ".join(vehicle_recommendations))

    df["maintenance_recommendation"] = recommendations
    return df