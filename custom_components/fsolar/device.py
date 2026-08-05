from typing import Any


class FSolarDevice:
    def __init__(self, device_data: dict[str, Any]) -> None:
        self.id = device_data.get("id")
        self.device_sn = device_data.get("deviceSn")
        self.device_type = device_data.get("deviceType")
        self.device_model = device_data.get("deviceModel")
        self.plant_id = device_data.get("plantId")
        match device_data.get("deviceType"):
            case "BP":
                self.device_type_str = "Battery Pack"
            case "OC":
                self.device_type_str = "Inverter"
            case _:
                self.device_type_str = "Unknown"

        self.device_data = device_data

    def __repr__(self) -> str:
        return (
            f"FSolarDevice(id={self.id}, device_sn={self.device_sn}, "
            f"device_type={self.device_type_str}, device_model={self.device_model}, "
            f"plant_id={self.plant_id})"
        )

    def update(self, device_data: dict[str, Any]) -> None:
        """Updates the device's attributes with new data."""
        self.device_data = device_data

    def as_inverter(self) -> Any | None:
        """Casts this FSolarDevice to an FSolarInverter."""
        if self.device_type == "OC":
            return FSolarInverter(self.device_data)
        return None

    def as_battery_pack(self) -> Any | None:
        """Casts this FSolarDevice to an FSolarBatteryPack."""
        if self.device_type == "BP":
            return FSolarBatteryPack(self.device_data)
        return None


class FSolarInverter(FSolarDevice):
    def __init__(self, device_data: dict[str, Any]) -> None:
        super().__init__(device_data)
        self.update(device_data)

    def update(self, device_data: dict[str, Any]) -> None:
        self.pv_string_1_power = device_data.get("pvPower")
        self.pv_string_2_power = device_data.get("pv2Power")
        self.pv_total_power = device_data.get("pvTotalPower")
        self.pv_string_1_voltage = device_data.get("pvVolt")
        self.pv_string_2_voltage = device_data.get("pv2Volt")
        self.pv_string_1_current = device_data.get("pvInCurr")
        self.pv_string_2_current = device_data.get("pv2InCurr")
        self.grid_input_voltage = device_data.get("acRInVolt")
        self.grid_input_current = device_data.get("acRInCurr")
        self.grid_input_frequency = device_data.get("acRInFreq")
        self.grid_input_power = device_data.get("acRInPower")
        self.ac_output_voltage = device_data.get("acROutVolt")
        self.ac_output_current = device_data.get("acROutCurr")
        self.ac_output_power = device_data.get("acTotalOutActPower")
        self.ac_output_apparent_power = device_data.get("acTotalOutAppaPower")
        self.ct_grid_power = device_data.get("ctPower")
        self.load_power = device_data.get("totalConsumPower")
        self.meter_power = device_data.get("meterPower")
        self.load_percent = device_data.get("loadPercent")
        self.battery_power = device_data.get("emsPower")
        self.battery_soc = device_data.get("emsSoc")
        self.battery_voltage = device_data.get("emsVoltage")
        self.battery_current = device_data.get("emsCurrent")
        self.battery_total_capacity = device_data.get("totalEmsCapacity")
        self.inverter_temp_max = device_data.get("tempMax")
        self.inverter_device_temp_max = device_data.get("devTempMax")
        self.pv_energy_total = device_data.get("ePvTotal")
        self.battery_energy_charged_total = device_data.get("eBatCharTotal")
        self.battery_energy_discharged_total = device_data.get("eBatDisCharTotal")
        self.grid_feed_energy_total = device_data.get("eGridFeedTotal")
        self.load_energy_total = device_data.get("eLoadTotal")
        self.grid_import_energy_total = device_data.get("eTotal")
        self.inverter_wifi_signal = device_data.get("wifiSignal")

    def __repr__(self) -> str:
        return (
            f"FSolarInverter(inner={super().__repr__()}, pv_string_1_power={self.pv_string_1_power}, "
            f"pv_string_2_power={self.pv_string_2_power}, ac_output_power={self.ac_output_power}, "
            f"grid_input_power={self.grid_input_power}, load_power={self.load_power}, "
            f"battery_power={self.battery_power}, battery_soc={self.battery_soc}, "
            f"battery_voltage={self.battery_voltage}, battery_current={self.battery_current}, "
            f"battery_total_capacity={self.battery_total_capacity}, inverter_temp_max={self.inverter_temp_max}, "
            f"inverter_device_temp_max={self.inverter_device_temp_max}, pv_energy_total={self.pv_energy_total}, "
            f"battery_energy_charged_total={self.battery_energy_charged_total}, "
            f"battery_energy_discharged_total={self.battery_energy_discharged_total}, grid_feed_energy_total={self.grid_feed_energy_total}, "
            f"load_energy_total={self.load_energy_total}, grid_import_energy_total={self.grid_import_energy_total}, inverter_wifi_signal={self.inverter_wifi_signal})"
        )


class FSolarBatteryPack(FSolarDevice):
    def __init__(self, device_data: dict[str, Any]) -> None:
        super().__init__(device_data)
        self.update(device_data)

    def update(self, device_data: dict[str, Any]) -> None:
        self.battery_soc = device_data.get("battSoc")
        self.battery_soh = device_data.get("battSoh")
        self.battery_voltage = device_data.get("battVolt")
        self.battery_current = device_data.get("battCurr")
        self.battery_power = device_data.get("bmsPower")
        self.battery_capacity = device_data.get("battCapacity")
        self.battery_rated_energy = device_data.get("ratedEnergy")
        self.battery_remaining_energy = device_data.get("remainingBatteryEnergy1")
        self.battery_charging_state = device_data.get("bmsChargingState")
        self.battery_bms_state = device_data.get("bmsState")
        self.battery_cell_voltage_max = device_data.get("maxVoltage2bms")
        self.battery_cell_voltage_min = device_data.get("minVoltage2bms")
        self.battery_cell_voltage_max_id = device_data.get("maxVoltageNum2bms")
        self.battery_cell_voltage_min_id = device_data.get("minVoltageNum2bms")
        self.battery_cell_voltages = device_data.get("bmsVoltageList", [])
        self.battery_cell_temps = [device_data.get(f"cellTemp{i}") for i in range(1, 5)]
        self.battery_temp_max = device_data.get("tempMax")
        self.battery_temp_min = device_data.get("tempMin")
        self.battery_charge_voltage_limit = device_data.get("BMSLCVolt")
        self.battery_discharge_voltage_limit = device_data.get("BMSLDVolt")
        self.battery_charge_current_limit = device_data.get("BMSLCCurr")
        self.battery_discharge_current_limit = device_data.get("BMSLDCurr")
        self.battery_heating_status = device_data.get("heatStatusStr")
        self.battery_wifi_signal = device_data.get("wifiSignal")
        self.battery_status = device_data.get("status")
        self.battery_warning_count = device_data.get("warningCount")

    def __repr__(self) -> str:
        return (
            f"FSolarBatteryPack(inner={super().__repr__()}, battery_soc={self.battery_soc}, "
            f"battery_soh={self.battery_soh}, battery_voltage={self.battery_voltage}, "
            f"battery_current={self.battery_current}, battery_power={self.battery_power}, "
            f"battery_capacity={self.battery_capacity}, battery_rated_energy={self.battery_rated_energy}, "
            f"battery_remaining_energy={self.battery_remaining_energy}, battery_charging_state={self.battery_charging_state}, "
            f"battery_bms_state={self.battery_bms_state}, battery_cell_voltage_max={self.battery_cell_voltage_max}, "
            f"battery_cell_voltage_min={self.battery_cell_voltage_min}, battery_cell_voltage_max_id={self.battery_cell_voltage_max_id}, "
            f"battery_cell_voltage_min_id={self.battery_cell_voltage_min_id}, battery_cell_voltages={self.battery_cell_voltages}, "
            f"battery_cell_temps={self.battery_cell_temps}, battery_temp_max={self.battery_temp_max}, "
            f"battery_temp_min={self.battery_temp_min}, battery_charge_voltage_limit={self.battery_charge_voltage_limit}, "
            f"battery_discharge_voltage_limit={self.battery_discharge_voltage_limit}, battery_charge_current_limit={self.battery_charge_current_limit}, "
            f"battery_discharge_current_limit={self.battery_discharge_current_limit}, battery_heating_status={self.battery_heating_status}, "
            f"battery_wifi_signal={self.battery_wifi_signal}, battery_status={self.battery_status}, "
            f"battery_warning_count={self.battery_warning_count})"
        )
