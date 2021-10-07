# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import numpy as np
from typing import Tuple

from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.dsl import dsl_op
from shapelets.model import NDArray


def computed_linechart(name: str) -> Tuple[str, NDArray]:
    return name, NDArray(np.random.randint(-100, 102, 10), name="Y Axis")


# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Register custom function
client.register_custom_function(computed_linechart)

# Create a dataApp
app = DataApp(
    name="08_multi_linechart",
    description="08_multi_linechart"
)

# Create numpy arrays
x_axis = np.array([10, 20, 30, 40, 50, 55, 60, 75, 80, 95])
y_axis = np.array([10, 21, 34, 12, 14, -1, 15, 28, -5, 39])
y_axis2 = np.array([43, 21, 23, -10, 2, 15, 38, 30, -30, 12])
y_axis3 = np.array([13, 22, 15, -5, 2, 5, 18, 25, -20, 12])

# Persist ndarrays
x_axis_nd = client.create_nd_array(x_axis, name="X Axis")
y_axis_nd = client.create_nd_array(y_axis, name="Y Axis")
y_axis_nd2 = client.create_nd_array(y_axis2, name="Y Axis 2")
y_axis_nd3 = client.create_nd_array(y_axis3, name="Y Axis 3")

# Create a line_chart rendering ndarrays
line_chart = app.line_chart(title="Random multi linechart")
line_chart.plot(y_axis_nd, label="Line 1")
line_chart.plot(y_axis_nd2, label="Line 2")
line_chart.plot(y_axis_nd3, label="Line 3")

# Execute algorithm which returns name and a random ndarray of integers
name, array = dsl_op.computed_linechart("Computed linechart")

button = app.button(text="Click here to get a computed linechart")
button.on_click([name, array])

# Plot computed ndarray and name
line_chart.plot(array, label=name)

# Place widgets
app.place(button)
app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
