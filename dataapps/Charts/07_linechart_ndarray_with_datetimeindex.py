# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
import numpy
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
import pandas as pd
import numpy as np
import datetime


# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="07_linechart_ndarray_with_datetimeindex",
    description="07_linechart_ndarray_with_datetimeindex"
)

index = pd.date_range(start = '2020-01-01', end = datetime.datetime.now(), freq='1d', tz = 'UTC').to_numpy()
data = np.random.randint(0,100,len(index))

# Persist ndarrays
x_axis_nd = client.create_nd_array(index, name="X Axis")
y_axis_nd = client.create_nd_array(data, name="Y Axis")

# Create a line_chart rendering ndarrays
line_chart = app.line_chart(title="Random linechart", y_axis=y_axis_nd) #This works
#line_chart = app.line_chart(title="Random linechart", x_axis=x_axis_nd, y_axis=y_axis_nd) #This does not work
# Place line_chart into the Dataapp
app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
