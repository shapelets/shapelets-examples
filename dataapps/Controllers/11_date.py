# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import time

from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.dsl import dsl_op


def custom_print_date(date: float) -> float:
    return date


# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(custom_print_date)

# Create a dataApp
app = DataApp(
    name="11_date",
    description="This DataApp shows how to use date input"
)

# Create a date
date = app.date()
# Place date into the Dataapp
app.place(date)

# Create a date with title
date1 = app.date("This is a date with title")
# Place date with title into the Dataapp
app.place(date1)

# Create a date with default date
date2 = app.date("This is a date with default date", date=time.time())
# Place date with default date into the Dataapp
app.place(date2)

# Create a date with min date
date3 = app.date("This is a date with min date", min_date=time.time())
# Place date with min date into the Dataapp
app.place(date3)

# Create a date with max date
date4 = app.date("This is a date with max date", max_date=time.time())
# Place date with max date into the Dataapp
app.place(date4)

# Create date input
date5 = app.date("This date input is an entry parameter")

# Use value as entry of an algorithm
result = dsl_op.custom_print_date(date5)
# Create a button
button = app.button(text="Click here")
# Execution custom_print_date on click
button.on_click([result])

# Place date input and button
app.place(date5)
app.place(button)
# Place a date input with the execution result as date and min_date entry
app.place(app.date(title="Result will be placed here", date=result, min_date=result))

# Register the Dataapp
client.register_data_app(app)
