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
    name="04_slider",
    description="04_slider"
)

# Create a slider
slider = app.slider(title="Select a value", min_value=0, max_value=10, step=1, default_value=5)
# Place slider into the Dataapp
app.place(slider)

# Register the Dataapp
client.register_data_app(app)
