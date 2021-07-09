# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl import DataApp
import shapelets.dsl.dsl_op as dsl_op


def custom_print(text: str) -> str:
    return text

def custom_print_integer(integer: int) -> int:
    return integer


# This example work under 0.3.8 and above
# Login into shapelets-solo
client = init_session("admin", "admin")
# Register a custom functions
client.register_custom_function(custom_print)
client.register_custom_function(custom_print_integer)

# Creating DataApp
app = DataApp(name="09_selector", description="09_selector")

# Selector with string values and default value
selector = app.selector(["hello", "world", "example"], value="hello")
app.place(selector)

# Create execution graph
result = dsl_op.custom_print(selector)
# Create button
button = app.button(text="Click to print")
# On click execute function
button.on_click([result])
# Print result into label
label = app.label(result)

# Place widgets
app.place(button)
app.place(label)

# Selector with number values
selector2 = app.selector([1, 2, 3])
app.place(selector2)

# Create execution graph
result2 = dsl_op.custom_print_integer(selector2)
# Create button
button2 = app.button(text="Click to print")
# On click execute function
button2.on_click([result2])
# Print result into label
label2 = app.label(result2)

# Place widgets
app.place(button2)
app.place(label2)

# Selector with dict values, index_by, label_by and value_by property
selector3 = app.selector([{"id": 1, "hello": "world", "foo": "bar"}, {"id": 2, "hello": "moon", "foo": "baz"}],
                         index_by="id", label_by="hello",
                         value_by="foo")
app.place(selector3)

# Create execution graph
result3 = dsl_op.custom_print(selector3)
# Create button
button3 = app.button(text="Click to print")
# On click execute function
button3.on_click([result3])
# Print result into label
label3 = app.label(result3)

# Place widgets
app.place(button3)
app.place(label3)

client.register_data_app(app)
