# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
import matplotlib.pyplot as plt
import numpy as np

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="10_matplotlib_chart",
    description="10_matplotlib_chart"
)

fig = plt.figure()
x = np.linspace(2, 3, 10)
y = np.sin(x ** 2) + np.cos(x)
plt.plot(x, y, label='Line 1')
plt.plot(x, y - 0.6, label='Line 2')
plt.legend()
fig.suptitle("""Function Example\n\n""", fontweight="bold")

img = app.image(fig)
app.place(img)

# Register the Dataapp
client.register_data_app(app)