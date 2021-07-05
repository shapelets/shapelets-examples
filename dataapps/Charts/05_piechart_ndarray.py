# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from typing import Tuple

import numpy as np
from shapelets import init_session
from shapelets.dsl import dsl_op
from shapelets.dsl.data_app import DataApp
from shapelets.model import NDArray


def concat_ndarrays(ndarray1: NDArray, ndarray2: NDArray) -> Tuple[NDArray, NDArray]:
    newarray = np.hstack([ndarray1.values, ndarray2.values])
    return NDArray(np.arange(newarray.size), name="Categories"), NDArray(newarray, name="Data")


# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(concat_ndarrays)

# Create a dataApp
app = DataApp(
    name="05_piechart_ndarray",
    description="05_piechart_ndarray"
)

app.place(app.markdown("""
  # This Dataapp concat two ndarrays
"""))

data1 = np.array([1, 2, 3, 4, 5])
data2 = np.array([6, 7, 8, 9, 10])

button = app.button(text="Concat ndarrays")

data1_ndarray = client.create_nd_array(data1)
data2_ndarray = client.create_nd_array(data2)

categories_result, data_result = dsl_op.concat_ndarrays(data1_ndarray, data2_ndarray)

button.on_click([categories_result, data_result])

app.place(button)

app.place(app.markdown("""
    # PieChart with categories and data from execution result
"""))

pie_chart = app.pie_chart(categories=categories_result, data=data_result)
app.place(pie_chart)

local_ndarray = client.create_nd_array(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), name="Local ndarray")

app.place(app.markdown("""
    # PieChart with categories set in place and data from execution result
"""))

pie_chart_mix = app.pie_chart(categories=local_ndarray, data=data_result)
app.place(pie_chart_mix)

app.place(app.markdown("""
    # PieChart with only data from execution result
"""))

pie_chart_without_categories = app.pie_chart(data=data_result)
app.place(pie_chart_without_categories)

app.place(app.markdown("""
    # PieChart with only data from local
"""))

pie_chart_data_local = app.pie_chart(data=local_ndarray)
app.place(pie_chart_data_local)

app.place(app.markdown("""
    # PieChart with categories and data from local
"""))

pie_chart_categories_data_local = app.pie_chart(categories=local_ndarray, data=local_ndarray)
app.place(pie_chart_categories_data_local)

# Register the Dataapp
client.register_data_app(app)
