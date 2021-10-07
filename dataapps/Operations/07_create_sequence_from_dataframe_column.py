# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import datetime
import numpy as np
import pandas as pd

from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="07_create_sequence_from_dataframe_column",
    description="This Dataapp creates a sequences from a pandas dataframe column and plots it"
)

app.place(app.markdown("""
  # This Dataapp creates a sequences from an NDArray and plots it
"""))

# Create a sample Dataframe with random integer values
rng = pd.date_range(start='2020-01-01', end=datetime.datetime.now(), freq='1d', tz='UTC')
column_name = 'random_series'
df = pd.DataFrame(index=rng, columns=[column_name])
df[column_name] = np.random.randint(0, 100, df.shape[0])

# Create sequence from a dataframe column
seq = client.create_sequence(dataframe=df[column_name].to_frame(), name=column_name, collection=None)

# Plot the sequence
line_chart = app.line_chart(sequence=seq)
app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
