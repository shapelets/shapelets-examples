# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from typing import List

from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.dsl import dsl_op
import random
import numpy as np

def random_hist() -> List[float]:
    import random
    return random.sample(range(10000), k=60)

def random_int() -> int:
    import random
    return random.randint(2, 40)

def random_bool() -> bool:
    import random
    return random.choice([True, False])

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(random_hist, force=True, persist_results=False)
client.register_custom_function(random_int, force=True, persist_results=False)
client.register_custom_function(random_bool, force=True, persist_results=False)

# Create a dataApp
app = DataApp(
    name="09_histogram",
    description="09_histogram"
)

app.place(app.markdown("# Basic histogram"))
app.place(app.histogram([12,21,34,12,34,3,6,14,12,12,14,34]))

app.place(app.markdown("# Basic histogram with 4 bins"))
app.place(app.histogram([12,21,34,12,34,3,6,14,12,12,14,34], 4))

app.place(app.markdown("# Basic histogram with 4 bins and cumulative"))
app.place(app.histogram([12,21,34,12,34,3,6,14,12,12,14,34], 4, True))

app.place(app.markdown("# Computed histogram. It renders after execution"))
button = app.button(text="Execute histogram")
hist = dsl_op.random_hist()
bins = dsl_op.random_int()
cumulative = dsl_op.random_bool()
button.on_click([hist, bins, cumulative])
app.place(button)
app.place(app.histogram(hist, bins, cumulative))

app.place(app.markdown("# Basic histogram with ndarray"))
ndarray = client.create_nd_array(np.array(random.sample(range(10000), k=60)), "NDarray")
app.place(app.histogram(ndarray))
# Register the Dataapp
client.register_data_app(app)


