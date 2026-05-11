from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


class MaintenanceNotifier(Observer):
    def update(self, message):
        print(f"[Maintenance Team Alert] {message}")


class DashboardNotifier(Observer):
    def update(self, message):
        print(f"[Dashboard Update] {message}")


class VehicleMonitor:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)

    def check_critical_vehicles(self, df):
        critical_df = df[df["status"] == "Critical"]

        if not critical_df.empty:
            for _, row in critical_df.iterrows():
                message = f"Vehicle {row['vehicle_id']} is CRITICAL with score {row['health_score']}"
                self.notify(message)