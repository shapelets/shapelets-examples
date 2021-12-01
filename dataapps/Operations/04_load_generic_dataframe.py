# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import pandas as pd

from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(name="04_load_generic_dataframe", description="This Dataapp loads data from a generic dataframe")

app.place(app.markdown("""
  # This Dataapp loads data from a generic dataframe
"""))

# Create a sample Dataframe with names and ages
Name = ['tom', 'krish', 'nick', 'juli']
Age = [25, 30, 26, 22]
df = pd.DataFrame(list(zip(Name, Age)), columns=['Name', 'Age'])

# Create NDArrays
data1_ndarray = client.create_nd_array(df['Name'].to_numpy(dtype='str'))
data2_ndarray = client.create_nd_array(df['Age'].to_numpy())

# Create bar chart
bar_chart = app.bar_chart(categories=data1_ndarray, data=data2_ndarray)
app.place(bar_chart)

# Register the Dataapp
client.register_data_app(app)
