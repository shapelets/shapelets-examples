# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from typing import Tuple

import numpy as np
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.model import NDArray
from shapelets.dsl import dsl_op


def computed_linechart(name: str) -> Tuple[str, NDArray]:
    return f"Name: {name}", NDArray(np.array([10, 21, 34, 12, 14, -1, 15, 28, -5, 39]), name="Y Axis")

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(computed_linechart)

# Create a dataApp
app = DataApp(
    name="07_linechart_computed",
    description="07_linechart_computed"
)

name, y_axis_nd = dsl_op.computed_linechart('Example name')

button = app.button(text="Execute")
button.on_click([name, y_axis_nd])

app.place(button)


# Create a line_chart rendering ndarrays and computed title
line_chart = app.line_chart(title=name, y_axis=y_axis_nd)
# Place line_chart into the Dataapp
app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
