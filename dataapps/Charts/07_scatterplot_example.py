# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import numpy as np

from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="07_scatterplot_example",
    description="07_scatterplot_ndarray"
)

# Create numpy arrays
aroma_array = np.array([8, 2, 3, 4, 5, 5, 10, 5, 4, 7, 10, 4, 3, 4, 5, 7, 7])
taste_array = np.array([10, 2, 3, 6, 12, 5, -5, -6, 2, 6, 6, -5, -5, 3, 4, 3, 2, 10, -6])
size_array = np.array([2, 5, 3, 4, 6, 5, 2, 7, 8, 8, 7, 6, 6, 8, 4, 8, 6])
price_array = np.array([20, 21, 30, 60, 12, 50, 15, 18, 23, 16, 43, 40, 32, 23, 24, 32, 22, 10, 22])
variety_array = np.array(
    ['Robusta', 'Arabica', 'Arabica', 'Arabica', 'Robusta', 'Arabica', 'Robusta', 'Robusta', 'Robusta',
     'Arabica', 'Arabica', 'Arabica', 'Robusta', 'Arabica', 'Robusta', 'Robusta'])

# Persist ndarrays
aroma_nd = client.create_nd_array(array=aroma_array, name="aroma", description="aroma quality")
taste_nd = client.create_nd_array(array=taste_array, name="taste", description="taste quality")
size_nd = client.create_nd_array(array=size_array, name="bean size (mm)", description="bean size")
price_nd = client.create_nd_array(array=price_array, name="bean price ($)", description="bean price")
variety_nd = client.create_nd_array(array=variety_array, name="bean variety", description="bean variety")

# Use ndarrays with scatter_plot
simple_scatter_plot = app.scatter_plot(x_axis=aroma_nd, y_axis=taste_nd, title="Simple")
simple_scatter_plot_trend = app.scatter_plot(x_axis=aroma_nd, y_axis=taste_nd, title="Simple with trend line",
                                             trend_line=True)
scatter_plot = app.scatter_plot(x_axis=aroma_nd, y_axis=taste_nd, color=price_nd, title="Color")
scatter_plot_variety = app.scatter_plot(x_axis=aroma_nd, y_axis=taste_nd, categories=variety_nd,
                                        title="Categorical")
bubble = app.scatter_plot(x_axis=aroma_nd, y_axis=taste_nd, size=price_nd, title="Bubble")
bubble_variety = app.scatter_plot(x_axis=aroma_nd, y_axis=taste_nd, size=size_nd, categories=variety_nd,
                                  title="Bubble Categorical")
bubble_complex_trend_line = app.scatter_plot(x_axis=aroma_nd, y_axis=taste_nd, size=size_nd, color=price_nd,
                                             title="Bubble with color and a trend line", trend_line=True)

# Create layout
hpanel1 = app.horizontal_flow_panel()
hpanel2 = app.horizontal_flow_panel()
hpanel3 = app.horizontal_flow_panel()
hpanel4 = app.horizontal_flow_panel()

hpanel1.place(simple_scatter_plot, width=7)
hpanel1.place(bubble, width=5)

hpanel2.place(scatter_plot, width=6)
hpanel2.place(scatter_plot_variety, width=6)

hpanel3.place(bubble_variety, width=12)
hpanel4.place(bubble_complex_trend_line, width=12)

# Place layout in Data app
app.place(hpanel1)
app.place(hpanel2)
app.place(hpanel3)
app.place(hpanel4)

# Register the Dataapp
client.register_data_app(app)
