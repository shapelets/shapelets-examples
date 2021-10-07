# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.dsl import dsl_op


def computeSquare(x: int) -> str:
    return 'The result is ' + str(x ** 2)


# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(computeSquare)

# Create a dataApp
app = DataApp(
    name="05_use_custom_function",
    description="05_use_custom_function"
)

# Create a slider
slider = app.slider(title="Select a value", min_value=0, max_value=10, step=1, default_value=5)
app.place(slider)

# Place slider into the Dataapp
button = app.button(text="Compute square of value")
app.place(button)

# Compute the square and store the result in output
output = dsl_op.computeSquare(slider)

# Display the result in a label
label = app.label(output)
app.place(label)

# Compute output when the button is clicked
button.on_click([output])

# Register the Dataapp
client.register_data_app(app)
