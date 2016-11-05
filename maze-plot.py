from bokeh.plotting import figure, output_file
from bokeh.layouts import gridplot, layout, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, Div, Slider
from bokeh.io import curdoc

import maze
from itertools import tee

# From https://docs.python.org/3/library/itertools.html#recipes
def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

x_slider = Slider(title='Number of nodes on the X axis', value=5, start=3, end=31, step=1)
y_slider = Slider(title='Number of nodes on the Y axis', value=5, start=3, end=x_slider.end, step=1)

size = 640
main = figure(width=size, plot_height=size, title=None)
node_source = ColumnDataSource(data=dict(x=[], y=[]))
vertex_source = ColumnDataSource(data=dict(x=[], y=[]))

rect_size = 0.5
main.rect(x='x', y='y', width=rect_size, height=rect_size, source=node_source, color='black')
main.rect(x='x', y='y', width=rect_size, height=rect_size, source=vertex_source, color='black')

class MyContainer(object):
    pass

container = MyContainer()

def generate():
    mean = lambda x,y: (x+y)/2
    segments = maze.Node.createMaze(container.nodes)
    xs, ys = zip(*[(mean(s.x,e.x), mean(s.y,e.y)) for seg in segments for s,e in pairwise(seg)])
    vertex_source.data = dict(x=xs, y=ys)

generate_button = Button(label='Generate')
generate_button.on_click(generate)

controls = [x_slider, y_slider]

def update():
    container.nodes = maze.Node2D.createGrid(y_slider.value, x_slider.value)
    xs, ys = zip(*[(n.x, n.y) for n in container.nodes])
    node_source.data = dict(x=xs, y=ys)
    
    generate()

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'
controls.append(generate_button)
inputs = widgetbox(*controls, sizing_mode=sizing_mode)

update()
l = layout([[inputs, gridplot([[main]])]], sizing_mode=sizing_mode)

curdoc().add_root(l)
curdoc().title = 'Maze'
