# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

from shapelets import init_session
from shapelets.dsl.data_app import DataApp, Sequence
from shapelets.dsl import dsl_op
import numpy as np
import pandas as pd
import datetime

def modify_sequence(input: Sequence)->Sequence:
    original_series = input.values.to_numpy()
    new_series = original_series * 2
    output = ShapeletsSequence(input.axis,[kv.Array.from_numpy(new_series, khiva_type=kv.array.dtype.f64)],
                               "Name",NUMERIC,input.axis_info,input.column_info,"")
    return output

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

client.register_custom_function(modify_sequence)

# Create a dataApp
app = DataApp(
    name="08_modify_sequence",
    description="This Dataapp creates a sequences from a pandas dataframe column and modifies it through a custom function"
)

# Create a sample Dataframe with random integer values
rng = pd.date_range(start = '2020-01-01', end = datetime.datetime.now(), freq='1d', tz = 'UTC')
column_name = 'random_series'
df = pd.DataFrame(index=rng, columns=[column_name])
df[column_name] = np.random.randint(0,100,df.shape[0])

# Create sequence from a dataframe column
seq = client.create_sequence(dataframe=df[column_name].to_frame(), name=column_name, collection=None)

mod_seq = dsl_op.modify_sequence(seq)

button = app.button(text='Compute sequence')
button.on_click(mod_seq)
app.place(button)

# Plot the sequence
line_chart = app.line_chart(sequence=seq)
app.place(line_chart)

line_chart2 = app.line_chart(sequence=mod_seq)
app.place(line_chart2)

# Register the Dataapp
client.register_data_app(app)
