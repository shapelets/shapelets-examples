# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.dsl import dsl_op


def custom_print_text(text: str) -> str:
    return text


# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(custom_print_text)

# Create a dataApp
app = DataApp(
    name="12_text",
    description="This DataApp shows how to use text input"
)

# Create a text input
text = app.text()
# Place text input into the Dataapp
app.place(text)

# Create a text with title
text1 = app.text("This the text title")
# Place text with title into the Dataapp
app.place(text1)

# Create a text input with default value
text2 = app.text("This is a text with default text", text="Hello world")
# Place text input with default text into the Dataapp
app.place(text2)

# Create text input
text3 = app.text("This text input is an entry parameter")

# Use value as entry of an algorithm
result = dsl_op.custom_print_text(text3)
# Create a button
button = app.button(text="Click here")
# Execution custom_print_text on click
button.on_click([result])

# Place text input and button
app.place(text3)
app.place(button)
# Place a text input with the execution result as text parameter
app.place(app.text(title="Result will be placed here", text=result))

# Register the Dataapp
client.register_data_app(app)
