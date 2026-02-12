def calculate_health_score(df):
    print("\nCalculating vehicle health scores...")

    df["health_score"] = 100

    # hız riski
    df.loc[df["speed"] > 110, "health_score"] -= 15

    # motor sıcaklığı riski
    df.loc[df["engine_temp"] > 100, "health_score"] -= 20

    # yakıt tüketimi riski
    df.loc[df["fuel_consumption"] > 9, "health_score"] -= 15

    # kilometre riski
    df.loc[df["mileage"] > 40000, "health_score"] -= 10

    return df
