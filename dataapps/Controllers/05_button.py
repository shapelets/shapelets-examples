# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl import dsl_op
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="05_button",
    description="05_button"
)

# Create buttons
button = app.button(text="Click does nothing")
button2 = app.button(text="Click runs abs")

# On click execute abs of -10
button2.on_click(dsl_op.abs(-10))

# Place buttons into the Dataapp
app.place(button)
app.place(button2)

# Register the Dataapp
client.register_data_app(app)
