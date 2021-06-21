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
    name="11_piechart_ndarray",
    description="11_piechart_ndarray"
)

# Create numpy arrays
categories = numpy.array(["A", "B", "C", "D", "E", "F", "G", "H"])
data = numpy.array([10, 21, 34, 23, 45, 12, 78, 31])

# Persist ndarrays
categories_nd = client.create_nd_array(categories, name="Categories")
data_nd = client.create_nd_array(data, name="Data")

# Create a pie_chart rendering ndarrays
pie_chart = app.pie_chart(title="Random example", categories=categories_nd, data=data_nd)
# Place pie_chart into the Dataapp
app.place(pie_chart)

# Register the Dataapp
client.register_data_app(app)
