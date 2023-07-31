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
        return (
            self.thermocouple.electrical_resistance + self.internal_contact_resistance
        )

    @property
    def total_electrical_resistance(self):
        self.electrical_resistance + self.load_resistance

    def temp_delta(self, source_temp: float, sink_temp: float):
        return (source_temp - sink_temp) / (
            1
            + self.heat_source_resistance * self.thermocouple.thermal_conductance
            + self.heat_sink_resistance * self.thermocouple.thermal_conductance
            + (
                self.thermocouple.seebeck_coefficent**2
                * (
                    self.heat_sink_resistance * source_temp
                    + self.heat_source_resistance * sink_temp
                )
                / self.total_electrical_resistance
            )
        )

    def current(self, hot_temp: float, cold_temp: float):
        return self.thermocouple.voltage(hot_temp=hot_temp, cold_temp=cold_temp) / (
            self.load_resistance * self.electrical_restance
        )

    def output_power(self, source_temp: float, sink_temp: float):
        return (
            self.thermocouple.seebeck_coefficent**2
            * self.temp_delta(source_temp=source_temp, sink_temp=sink_temp) ** 2
            * self.load_resistance
        ) / (self.total_electrical_resistance**2)

    def max_power_load_resistance(self, source_temp: float, sink_temp: float):
        return self.electrical_resistance + (
            self.thermocouple.seebeck_coefficent**2
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


@dataclass
class Thermocouple:
    n_type_semiconductor: NTypeSemiconductor
    p_type_semiconductor: PTypeSemiconductor
    load_resistance: float

    @property
    def thermal_conductance(self):
        return (
            self.n_type_semiconductor.thermal_conductance
            + self.p_type_semiconductor.thermal_conductance
        ) / 2

    @property
    def electrical_resistance(self):
        return (
            self.n_type_semiconductor.electrical_resistance
            + self.p_type_semiconductor.electrical_resistance
        )

    @property
    def seebeck_coefficent(self):
        return (
            self.p_type_semiconductor.seebeck_coefficent
            - self.n_type_semiconductor.seebeck_coefficent
        )

    def voltage(self, hot_temp: float, cold_temp: float):
        return (
            0.5
            * (hot_temp**2 - cold_temp**2)
            * (
                self.n_type_semiconductor.seebeck_coefficent
                - self.p_type_semiconductor.seebeck_coefficent
            )
        )


@dataclass
class Semiconductor:
    length: float  # Meters
    cross_sectional_area: float
    thermal_conductivity: float
    electrical_resistivity: float
    seebeck_coefficent: float
    thomson_coefficeint: float

    @property
    def thermal_conductance(self):
        return (self.thermal_conductivity * self.cross_sectional_area) / self.length

    @property
    def electrical_resistance(self):
        return (self.electrical_resistivity * self.length) / self.cross_sectional_area

class NTypeSemiconductor(Semiconductor):
    pass


class PTypeSemiconductor(Semiconductor):
    pass