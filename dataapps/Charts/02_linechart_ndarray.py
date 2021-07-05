# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
import numpy
from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="02_linechart_ndarray",
    description="02_linechart_ndarray"
)

# Create numpy arrays
x_axis = numpy.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
y_axis = numpy.array([10, 21, 34, 12, 14, -1, 15, 28, -5, 39])

# Persist ndarrays
x_axis_nd = client.create_nd_array(x_axis, name="X Axis")
y_axis_nd = client.create_nd_array(y_axis, name="Y Axis")

# Create a line_chart rendering ndarrays
line_chart = app.line_chart(title="Random linechart", x_axis=x_axis_nd, y_axis=y_axis_nd)
# Place line_chart into the Dataapp
app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
