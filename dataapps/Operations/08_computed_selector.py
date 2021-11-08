# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from typing import List

from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.dsl import dsl_op


def get_list_of_ints(options: List[int]) -> List[int]:
    return options


def get_list_of_strings(options: List[str]) -> List[str]:
    return options


def get_int(i: int) -> int:
    return i


def get_str(s: str) -> str:
    return s


# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="08_computed_selector_options",
    description="08_computed_selector_options"
)

# Get a list of ints and store the result
client.register_custom_function(get_list_of_ints)
output_ints = dsl_op.get_list_of_ints([1, 2, 3])

# Create and place selector that accepts a list of ints
selector_ints = app.selector(output_ints)
app.place(selector_ints)

# Get a list of strings and store the result
client.register_custom_function(get_list_of_strings)
output_strings = dsl_op.get_list_of_strings(["hello", "world", "example"])

# Get a title and store the result
client.register_custom_function(get_str)
title = dsl_op.get_str('Computed title')

# Create a selector that accepts a list of computable strings and a computed title
selector_strings = app.selector(options=output_strings, title=title)
app.place(selector_strings)

# You can also compute the initial value
client.register_custom_function(get_int)
selected = dsl_op.get_int(3)

selector_dicts = app.selector(options=output_ints, value=selected)
app.place(selector_dicts)

# Create button to get computed parameters
button = app.button(text="Compute options")
app.place(button)
button.on_click([output_strings, output_ints, selected, title])

# Register the Dataapp
client.register_data_app(app)
