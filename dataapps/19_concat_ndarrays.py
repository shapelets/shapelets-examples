# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from typing import Tuple
from shapelets import init_session
from shapelets.dsl.data_app import DataApp, NDArray
from shapelets.dsl import dsl_op
import numpy as np

def concat_ndarrays(ndarray1: NDArray, ndarray2: NDArray) -> Tuple[NDArray, NDArray]:
  newarray = np.hstack([ndarray1.values, ndarray2.values])
  return NDArray(np.arange(newarray.size), name="X_Axis"), NDArray(newarray, name="Y_axis")

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(concat_ndarrays)

# Create a dataApp
app = DataApp(
  name="19_concat_ndarrays",
  description="This Dataapp concat two ndarrays"
)

app.place(app.markdown("""
  # This Dataapp concat two ndarrays
"""))

y_axis1 = np.array([1,2,3,4,5])
y_axis2 = np.array([6,7,8,9,10])

button = app.button(text="Concat ndarrays")

y_axis1_ndarray = client.create_nd_array(y_axis1)
y_axis2_ndarray = client.create_nd_array(y_axis2)

x_axis_result, y_axis_result = dsl_op.concat_ndarrays(y_axis1_ndarray, y_axis2_ndarray)

button.on_click([x_axis_result, y_axis_result])

app.place(button)

line_chart = app.line_chart(x_axis=x_axis_result, y_axis=y_axis_result)

app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
