import pandas as pd
import plotly.graph_objects as go

from objects.generator import TEG, Thermocouple

seebecks = [*range(1, 1000)]
seebecks = [seebeck/100 for seebeck in seebecks]

generators = iter([TEG(
    thermocouple=Thermocouple(
        thermal_conductance=2.907, electrical_resistance=3.4, seebeck_coefficent=seebeck
    ),
    heat_source_resistance=.01,
    heat_sink_resistance=.01,
    internal_contact_resistance=.01,
    load_resistance=3,
) for seebeck in seebecks])





sink_temp = 0
source_temp = 40
data = pd.DataFrame()
data["Seebeck Coefficient"] = seebecks
data["Output Power"] = [generator.output_power(source_temp=source_temp, sink_temp=sink_temp) for generator in generators]

fig = go.Figure()

# Add Solar Panel Temperature vs Time
fig.add_trace(go.Scatter(x=data["Seebeck Coefficient"], y=data["Output Power"], mode='lines', name='Output Power'))

# Update layout
fig.update_layout(
    title_text="TEG Output Power vs Seebeck Coefficent at 40C Temp Delta",
    xaxis_title="Seebeck Coefficient (V/K)",
    yaxis_title="Output Power (W)",
)

config = {
  'toImageButtonOptions': {
    'format': 'png', # one of png, svg, jpeg, webp
    'filename': 'seebeck_coefficient.png',
    'scale': 3 # Multiply title/legend/axis/canvas sizes by this factor
  }
}

fig.show(config=config)

