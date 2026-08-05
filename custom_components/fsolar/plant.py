from typing import Any


class FSolarPlant:
    """Represents a plant in the FSolar system."""

    def __init__(self, plant_data: dict[str, Any]) -> None:
        self.id = plant_data.get("id")
        self.plant_name = plant_data.get("plantName")
        self.plant_type = plant_data.get("plantType")
        match plant_data.get("plantType"):
            case "HO":
                self.plant_type_str = "Home"
            case _:
                self.plant_type_str = "Unknown"
        self.total_installed_capacity = plant_data.get("totalInstalledCapacity")

        self.update(plant_data)

    def __repr__(self) -> str:
        return (
            f"FSolarPlant(id={self.id}, plant_name={self.plant_name}, "
            f"plant_type={self.plant_type_str}, total_installed_capacity={self.total_installed_capacity}, "
            f"current_power={self.current_power}{self.current_power_unit}, "
            f"today_energy={self.today_energy}{self.today_energy_unit}, "
            f"total_energy={self.total_energy}{self.total_energy_unit})"
        )

    def update(self, plant_data: dict[str, Any]) -> None:
        """Updates the plant's attributes with new data."""
        self.current_power = plant_data.get("currentPower")
        self.current_power_unit = plant_data.get("currentPowerUnit")
        self.today_energy = plant_data.get("todayEnergy")
        self.today_energy_unit = plant_data.get("todayEnergyUnit")
        self.total_energy = plant_data.get("totalEnergy")
        self.total_energy_unit = plant_data.get("totalEnergyUnit")
