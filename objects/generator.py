from __future__ import annotations
from dataclasses import dataclass

@dataclass
class TEG:
    thermocouple: Thermocouple
    heat_source_resistance: float
    heat_sink_resistance: float
    internal_contact_resistance: float
    load_resistance: float

    @property
    def electrical_resistance(self):
        return self.thermocouple.electrical_resistance + self.internal_contact_resistance

    @property
    def total_electrical_resistance(self):
        return self.electrical_resistance + self.load_resistance
    
    def temp_delta(self, source_temp: float, sink_temp: float):
        return (source_temp - sink_temp) / (
            1
            + self.heat_source_resistance * self.thermocouple.thermal_conductance
            + self.heat_sink_resistance * self.thermocouple.thermal_conductance
            + (
                self.thermocouple.seebeck_coefficent*self.thermocouple.seebeck_coefficent
                * (
                    self.heat_sink_resistance * source_temp
                    + self.heat_source_resistance * sink_temp
                )
                / self.total_electrical_resistance
            )
        )
    
    def output_power(self, source_temp: float, sink_temp: float):
        return (
            self.thermocouple.seebeck_coefficent*self.thermocouple.seebeck_coefficent
            * self.temp_delta(source_temp=source_temp, sink_temp=sink_temp) ** 2
            * self.load_resistance
        ) / (self.total_electrical_resistance**2)

    def max_power_load_resistance(self, source_temp: float, sink_temp: float):
        return self.electrical_resistance + (
            self.thermocouple.seebeck_coefficent*self.thermocouple.seebeck_coefficent
            * (
                self.heat_sink_resistance * source_temp
                + self.heat_source_resistance * sink_temp
            )
        ) / (
            1
            + self.heat_sink_resistance * self.thermocouple.thermal_conductance
            + self.heat_source_resistance * self.thermocouple.thermal_conductance
        )
    
    def set_load_resistance(self, source_temp: float, sink_temp: float) -> None:
        self.load_resistance = self.max_power_load_resistance(source_temp=source_temp, sink_temp=sink_temp)
        return self.load_resistance
    
    def voltage(self, hot_temp: float, cold_temp: float):
        return (
            0.5
            * (hot_temp**2 - cold_temp**2)
            * self.thermocouple.seebeck_coefficent
        )
    
    def current(self, hot_temp: float, cold_temp: float):
        return self.voltage(hot_temp=hot_temp, cold_temp=cold_temp) / (
            self.load_resistance * self.electrical_restance
        )


@dataclass
class Thermocouple:
    thermal_conductance: float
    electrical_resistance: float
    seebeck_coefficent: float