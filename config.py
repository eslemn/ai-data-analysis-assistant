class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.model_name = "gemma3:4b"
            cls._instance.speed_threshold = 110
            cls._instance.engine_temp_threshold = 100
            cls._instance.fuel_threshold = 9
            cls._instance.mileage_threshold = 40000
            cls._instance.battery_voltage_threshold = 11.8
            cls._instance.brake_wear_threshold = 70
            cls._instance.vibration_threshold = 5.0
            cls._instance.oil_quality_threshold = 60
            cls._instance.tire_pressure_threshold = 30
        return cls._instance