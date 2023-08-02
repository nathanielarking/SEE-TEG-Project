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
    load_resistance=1,
)

data = pd.read_csv("data/ambient_temperature.csv", delimiter=",")
data["panel_temp"] = data["temp"] + 10

sink_temp = 10

# Calculate optimal_load_resistance
data["optimal_load_resistance"] = [
    generator.set_load_resistance(source_temp=st, sink_temp=sink_temp)
    for st in data["panel_temp"]
]

fig = go.Figure()

# Add Solar Panel Temperature vs Time
fig.add_trace(go.Scatter(x=data["time"], y=data["panel_temp"], mode='lines', name='Solar Panel Temperature'))

# Add Optimal Load Resistance vs Time
fig.add_trace(go.Scatter(x=data["time"], y=data["optimal_load_resistance"], mode='lines', name='Optimal Load Resistance', yaxis='y2'))

# Update layout
fig.update_layout(
    title_text="Solar Panel Temperature and Optimal Load Resistance",
    xaxis_title="Time",
    yaxis_title="Solar Panel Temperature (°C)",

    yaxis2=dict(
        title="Optimal Load Resistance (Ω)",
        overlaying='y',
        side='right',
        range=[min(data["optimal_load_resistance"]), max(data["optimal_load_resistance"])]
    ),
    showlegend=True
)

fig.show()

print(data)
