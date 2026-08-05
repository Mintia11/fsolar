"""Sensor platform for FelicitySolar integration."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FSolarDataUpdateCoordinator


@dataclass(frozen=True, kwargs_only=True)
class FSolarSensorDescription(SensorEntityDescription):
    """Class describing FSolar sensor entities."""

    value_fn: Callable[[object], object]


INVERTER_SENSORS: tuple[FSolarSensorDescription, ...] = (
    # Solar PV
    FSolarSensorDescription(
        key="pv_string_1_power",
        name="PV String 1 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.pv_string_1_power,
    ),
    FSolarSensorDescription(
        key="pv_string_2_power",
        name="PV String 2 Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.pv_string_2_power,
    ),
    FSolarSensorDescription(
        key="pv_total_power",
        name="PV Total Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.pv_total_power,
    ),
    FSolarSensorDescription(
        key="pv_string_1_voltage",
        name="PV String 1 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.pv_string_1_voltage,
    ),
    FSolarSensorDescription(
        key="pv_string_2_voltage",
        name="PV String 2 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.pv_string_2_voltage,
    ),
    FSolarSensorDescription(
        key="pv_string_1_current",
        name="PV String 1 Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.pv_string_1_current,
    ),
    FSolarSensorDescription(
        key="pv_string_2_current",
        name="PV String 2 Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.pv_string_2_current,
    ),
    # AC / Grid
    FSolarSensorDescription(
        key="grid_input_voltage",
        name="Grid Input Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.grid_input_voltage,
    ),
    FSolarSensorDescription(
        key="grid_input_current",
        name="Grid Input Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.grid_input_current,
    ),
    FSolarSensorDescription(
        key="grid_input_frequency",
        name="Grid Input Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.grid_input_frequency,
    ),
    FSolarSensorDescription(
        key="grid_input_power",
        name="Grid Input Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.grid_input_power,
    ),
    FSolarSensorDescription(
        key="ac_output_voltage",
        name="AC Output Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.ac_output_voltage,
    ),
    FSolarSensorDescription(
        key="ac_output_current",
        name="AC Output Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.ac_output_current,
    ),
    FSolarSensorDescription(
        key="ac_output_power",
        name="AC Output Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.ac_output_power,
    ),
    FSolarSensorDescription(
        key="ac_output_apparent_power",
        name="AC Output Apparent Power",
        native_unit_of_measurement="VA",
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.ac_output_apparent_power,
    ),
    FSolarSensorDescription(
        key="ct_grid_power",
        name="CT Grid Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.ct_grid_power,
    ),
    FSolarSensorDescription(
        key="load_power",
        name="Load Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.load_power,
    ),
    FSolarSensorDescription(
        key="meter_power",
        name="Meter Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.meter_power,
    ),
    FSolarSensorDescription(
        key="load_percent",
        name="Load Percentage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.load_percent,
    ),
    # Battery EMS
    FSolarSensorDescription(
        key="battery_power",
        name="EMS Battery Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_power,
    ),
    FSolarSensorDescription(
        key="battery_soc",
        name="EMS Battery SoC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_soc,
    ),
    FSolarSensorDescription(
        key="battery_voltage",
        name="EMS Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_voltage,
    ),
    FSolarSensorDescription(
        key="battery_current",
        name="EMS Battery Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_current,
    ),
    FSolarSensorDescription(
        key="battery_total_capacity",
        name="EMS Battery Capacity",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        value_fn=lambda dev: dev.battery_total_capacity,
    ),
    # Temperatures & Diagnostics
    FSolarSensorDescription(
        key="inverter_temp_max",
        name="Inverter Max Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.inverter_temp_max,
    ),
    FSolarSensorDescription(
        key="inverter_device_temp_max",
        name="Inverter Device Max Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.inverter_device_temp_max,
    ),
    FSolarSensorDescription(
        key="inverter_wifi_signal",
        name="Inverter Wi-Fi Signal",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.inverter_wifi_signal,
    ),
    # Totals (Energy)
    FSolarSensorDescription(
        key="pv_energy_total",
        name="PV Total Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda dev: dev.pv_energy_total,
    ),
    FSolarSensorDescription(
        key="battery_energy_charged_total",
        name="Battery Charged Total Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda dev: dev.battery_energy_charged_total,
    ),
    FSolarSensorDescription(
        key="battery_energy_discharged_total",
        name="Battery Discharged Total Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda dev: dev.battery_energy_discharged_total,
    ),
    FSolarSensorDescription(
        key="grid_feed_energy_total",
        name="Grid Export Total Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda dev: dev.grid_feed_energy_total,
    ),
    FSolarSensorDescription(
        key="load_energy_total",
        name="Load Total Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda dev: dev.load_energy_total,
    ),
    FSolarSensorDescription(
        key="grid_import_energy_total",
        name="Grid Import Total Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda dev: dev.grid_import_energy_total,
    ),
)


BATTERY_SENSORS: tuple[FSolarSensorDescription, ...] = (
    FSolarSensorDescription(
        key="battery_soc",
        name="Battery SoC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_soc,
    ),
    FSolarSensorDescription(
        key="battery_soh",
        name="Battery SoH",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_soh,
    ),
    FSolarSensorDescription(
        key="battery_voltage",
        name="Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_voltage,
    ),
    FSolarSensorDescription(
        key="battery_current",
        name="Battery Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_current,
    ),
    FSolarSensorDescription(
        key="battery_power",
        name="Battery Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_power,
    ),
    FSolarSensorDescription(
        key="battery_capacity",
        name="Battery Capacity",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        value_fn=lambda dev: dev.battery_capacity,
    ),
    FSolarSensorDescription(
        key="battery_rated_energy",
        name="Battery Rated Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        value_fn=lambda dev: dev.battery_rated_energy,
    ),
    FSolarSensorDescription(
        key="battery_remaining_energy",
        name="Battery Remaining Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY_STORAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_remaining_energy,
    ),
    FSolarSensorDescription(
        key="battery_charging_state",
        name="Charging State",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_charging_state,
    ),
    FSolarSensorDescription(
        key="battery_bms_state",
        name="BMS State",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_bms_state,
    ),
    FSolarSensorDescription(
        key="battery_cell_voltage_max",
        name="Max Cell Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_cell_voltage_max,
    ),
    FSolarSensorDescription(
        key="battery_cell_voltage_min",
        name="Min Cell Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_cell_voltage_min,
    ),
    FSolarSensorDescription(
        key="battery_cell_voltage_max_id",
        name="Max Voltage Cell ID",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_cell_voltage_max_id,
    ),
    FSolarSensorDescription(
        key="battery_cell_voltage_min_id",
        name="Min Voltage Cell ID",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_cell_voltage_min_id,
    ),
    FSolarSensorDescription(
        key="battery_temp_max",
        name="Max Battery Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_temp_max,
    ),
    FSolarSensorDescription(
        key="battery_temp_min",
        name="Min Battery Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda dev: dev.battery_temp_min,
    ),
    FSolarSensorDescription(
        key="battery_charge_voltage_limit",
        name="Charge Voltage Limit",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_charge_voltage_limit,
    ),
    FSolarSensorDescription(
        key="battery_discharge_voltage_limit",
        name="Discharge Voltage Limit",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_discharge_voltage_limit,
    ),
    FSolarSensorDescription(
        key="battery_charge_current_limit",
        name="Charge Current Limit",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_charge_current_limit,
    ),
    FSolarSensorDescription(
        key="battery_discharge_current_limit",
        name="Discharge Current Limit",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_discharge_current_limit,
    ),
    FSolarSensorDescription(
        key="battery_heating_status",
        name="Heating Status",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_heating_status,
    ),
    FSolarSensorDescription(
        key="battery_status",
        name="Battery Status",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_status,
    ),
    FSolarSensorDescription(
        key="battery_warning_count",
        name="Warning Count",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_warning_count,
    ),
    FSolarSensorDescription(
        key="battery_wifi_signal",
        name="Battery Wi-Fi Signal",
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda dev: dev.battery_wifi_signal,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FSolar sensors from a config entry."""
    coordinator: FSolarDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[FSolarSensorEntity] = []

    for device in coordinator.data.get("devices", {}).values():
        if hasattr(device, "pv_total_power"):
            for desc in INVERTER_SENSORS:
                entities.append(FSolarSensorEntity(coordinator, device, desc))
        elif hasattr(device, "battery_soh"):
            for desc in BATTERY_SENSORS:
                entities.append(FSolarSensorEntity(coordinator, device, desc))

    async_add_entities(entities)


class FSolarSensorEntity(CoordinatorEntity[FSolarDataUpdateCoordinator], SensorEntity):
    """Representation of an FSolar sensor."""

    entity_description: FSolarSensorDescription

    def __init__(
        self,
        coordinator: FSolarDataUpdateCoordinator,
        device: object,
        description: FSolarSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_sn = device.device_sn
        self._attr_unique_id = f"{self._device_sn}_{description.key}"
        self._attr_name = (
            f"{getattr(device, 'device_model', 'FSolar')} {description.name}"
        )

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_sn)},
            name=f"{getattr(device, 'device_type_str', 'Device')} ({self._device_sn})",
            manufacturer="FelicitySolar",
            model=getattr(device, "device_model", None),
        )

    @property
    def native_value(self) -> object:
        """Return state of sensor."""
        device = self.coordinator.data["devices"].get(self._device_sn)
        if device is None:
            return None
        return self.entity_description.value_fn(device)
