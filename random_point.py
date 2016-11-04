from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models.widgets import Button
from bokeh.io import curdoc

import numpy as np

p = figure()

def generate():
	p.circle(*zip(np.random.random(size=2)))

generate_button = Button(label='Generate')
generate_button.on_click(generate)

l = layout([[p],[generate_button]])

generate()

curdoc().add_root(l)
curdoc().title = 'Random point in unit square'
