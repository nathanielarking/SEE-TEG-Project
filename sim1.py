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

data = pd.DataFrame()
data["Temp Delta"] = range(0, 100, 5)

sink_temp = 0
data["Optimal Load Resistance"] = [generator.set_load_resistance(source_temp=st, sink_temp=sink_temp) for st in data["Temp Delta"]]

fig = go.Figure()

# Add Solar Panel Temperature vs Time
fig.add_trace(go.Scatter(x=data["Temp Delta"], y=data["Optimal Load Resistance"], mode='lines', name='Output Power'))

# Update layout
fig.update_layout(
    title_text="TEG Optimal Load Resistance vs Temperature Delta",
    xaxis_title="Temperature Delta (°C)",
    yaxis_title="Optimal load resistance (Ohm)",
)

config = {
  'toImageButtonOptions': {
    'format': 'png', # one of png, svg, jpeg, webp
    'filename': 'optimal_load_resistance.png',
    'scale': 3 # Multiply title/legend/axis/canvas sizes by this factor
  }
}


fig.show(config=config)

