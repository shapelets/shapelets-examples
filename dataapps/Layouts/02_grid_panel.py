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
    name="14_grid_panel",
    description="14_grid_panel"
)

# Create an grid_panel
gp = app.grid_panel(title="My grid panel", num_rows=2, num_cols=2)

# Create four labels
top_left = app.label("Top Left label")
top_right = app.label("Top Right label")
bottom_left = app.label("Bottom Left label")
bottom_right = app.label("Bottom Right label")

# Place labels into the grid_panel
gp.place(top_left, row=0, col=0)
gp.place(top_right, row=0, col=1)
gp.place(bottom_left, row=1, col=0)
gp.place(bottom_right, row=1, col=1)

# Place grid_panel into the Dataapp
app.place(gp)

# Register the Dataapp
client.register_data_app(app)
