# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="13_horizontal_flow_panel",
    description="13_horizontal_flow_panel"
)

# Create an horizontal_flow_panel
hf = app.horizontal_flow_panel("My horizontal flow panel")

# Create two labels
left = app.label("Left label")
right = app.label("Right label")

# Place labels into the horizontal_flow_panel
hf.place(left, width=6)
hf.place(right, width=6)

# Place horizontal_flow_panel into the Dataapp
app.place(hf)

# Register the Dataapp
client.register_data_app(app)
