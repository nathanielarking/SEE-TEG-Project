import pandas as pd
import plotly.graph_objects as go

from objects.generator import TEG, Thermocouple

generator = TEG(
    thermocouple=Thermocouple(
        thermal_conductance=2.907, electrical_resistance=3.4, seebeck_coefficent=0.1
    ),
    heat_source_resistance=.01,
    heat_sink_resistance=.01,
    internal_contact_resistance=.01,
    load_resistance=3,
)

data = pd.read_csv("data/ambient_temperature.csv", delimiter=",")
data["panel_temp"] = data["temp"] + 10

sink_temp = 10

source_temp = data["panel_temp"]
data["output_power"] = [generator.output_power(source_temp=st, sink_temp=sink_temp) for st in source_temp]

fig = go.Figure()

# Add Solar Panel Temperature vs Time
fig.add_trace(go.Scatter(x=data["time"], y=data["panel_temp"], mode='lines', name='Solar Panel Temperature'))

# Add TEG Output Power vs Time
fig.add_trace(go.Scatter(x=data["time"], y=data["output_power"], mode='lines', name='TEG Output Power', yaxis='y2'))

# Update layout
fig.update_layout(
    title_text="Solar Panel Temperature and TEG Output Power",
    xaxis_title="Time (Hour)",
    yaxis_title="Solar Panel Temperature (°C)",
    yaxis2=dict(
        title="TEG Output Power (W)",
        overlaying='y',
        side='right',
    ),
    showlegend=True
)

fig.show()
