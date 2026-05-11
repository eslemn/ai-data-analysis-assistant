from abc import ABC, abstractmethod
import numpy as np
from config import Config


class HealthStrategy(ABC):
    @abstractmethod
    def calculate_health_score(self, df):
        pass


class RuleBasedHealthStrategy(HealthStrategy):
    def calculate_health_score(self, df):
        print("\nCalculating vehicle health scores using rule-based strategy...")

        config = Config()
        df["health_score"] = 100

        if "speed" in df.columns:
            df.loc[df["speed"] > config.speed_threshold, "health_score"] -= 10

        if "engine_temp" in df.columns:
            df.loc[df["engine_temp"] > config.engine_temp_threshold, "health_score"] -= 20

        if "fuel_consumption" in df.columns:
            df.loc[df["fuel_consumption"] > config.fuel_threshold, "health_score"] -= 10

        if "mileage" in df.columns:
            df.loc[df["mileage"] > config.mileage_threshold, "health_score"] -= 10

        if "battery_voltage" in df.columns:
            df.loc[df["battery_voltage"] < config.battery_voltage_threshold, "health_score"] -= 15

        if "brake_wear" in df.columns:
            df.loc[df["brake_wear"] > config.brake_wear_threshold, "health_score"] -= 20

        if "vibration" in df.columns:
            df.loc[df["vibration"] > config.vibration_threshold, "health_score"] -= 15

        if "oil_quality" in df.columns:
            df.loc[df["oil_quality"] < config.oil_quality_threshold, "health_score"] -= 10

        if "tire_pressure" in df.columns:
            df.loc[df["tire_pressure"] < config.tire_pressure_threshold, "health_score"] -= 10

        df["health_score"] = df["health_score"].clip(lower=0)

        conditions = [
            (df["health_score"] >= 80),
            (df["health_score"] >= 50) & (df["health_score"] < 80),
            (df["health_score"] < 50)
        ]
        choices = ["Normal", "Warning", "Critical"]
        df["status"] = np.select(conditions, choices, default="Unknown")

        return df


class HealthContext:
    def __init__(self, strategy: HealthStrategy):
        self._strategy = strategy

    def calculate_health_score(self, df):
        return self._strategy.calculate_health_score(df)