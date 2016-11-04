from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button
from bokeh.io import curdoc

import numpy as np

source = ColumnDataSource(data=dict(x=[], y=[]))

p = figure()
p.circle(x='x', y='y', source=source)

def generate():
	values = [[v] for v in np.random.random(size=2)]
	source.data = dict(x=values[0], y=values[1])

generate_button = Button(label='Generate')
generate_button.on_click(generate)

l = layout([[p],[generate_button]])

generate()

curdoc().add_root(l)
curdoc().title = 'Random point in unit square'
