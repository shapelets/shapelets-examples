# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
import random

from shapelets import init_session
from shapelets.dsl import DataApp
import shapelets.dsl.dsl_op as dsl_op


def custom_random(a: int, b: int) -> int:
    import random
    return random.randint(a, b)


# This example works under 0.3.15 and above
# Login into shapelets-solo
client = init_session("admin", "admin")
# Register custom function
client.register_custom_function(custom_random)
# Creating DataApp
app = DataApp(name="10_timer", description="Example of using timer")

# Creating a timer
timer = app.timer(title="Execute random number every 5 seconds, 4 times", every=5, times=4)
value = dsl_op.custom_random(0, 100)
timer.run([value])

# Creating a label with the executed value
label = app.label(value)

# Placing widgets into the DataApp
app.place(timer)
app.place(label)

client.register_data_app(app)
