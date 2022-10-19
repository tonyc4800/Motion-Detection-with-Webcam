from motion_detector import df 
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

# Add new columns to the dataframe which is the datetime values converted into strings
# These will be provided to the HoverTool for use in the tooltips
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

# Creates bokeh datasoucre
cds = ColumnDataSource(df)

# Creates bokeh figure that will display the data
f = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode = 'scale_both', title = "Motion Graph")
f.yaxis.minor_tick_line_color = None
f.yaxis.ticker.desired_num_ticks = 1

# Adds hover functionality to graph
hover = HoverTool(tooltips = [("Start", "@Start_string"), ("End", "@End_string")])
f.add_tools(hover)

# Adds quadrilaterals to the graph to represent the data
f.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "green", source = cds)

output_file("Graph.html")
show(f)