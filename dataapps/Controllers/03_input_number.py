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
    name="03_input_number",
    description="03_input_number"
)

# Create input number
number = app.number(name="Input number")
# Create input number with default value
number2 = app.number(name="Input number with default value", default_value=10)
# Create input with value type
number3 = app.number(name="Input number with value type", value_type=float)

# Place widgets into the Dataapp
app.place(number)
app.place(number2)
app.place(number3)

# Register the Dataapp
client.register_data_app(app)
