# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

"""Use this file to create example dataApps"""
from shapelets import init_session
import pandas as pd
from shapelets.dsl import DataApp, dsl_op
from shapelets.model import Dataframe


def computed_dataframe(df: Dataframe) -> Dataframe:
    return df

client = init_session("admin", "admin")

client.register_custom_function(computed_dataframe)

df = pd.read_csv('../Data/mitdb102.csv', header=None, index_col=0, names=['MLII', 'V1'], skiprows=200000, nrows=20000)
df.index = pd.to_datetime(df.index, unit='s')

df_result = client.create_dataframe(df, name="Example dataframe", description="Example description")

app = DataApp(name="13_table", description="13_table")

table = app.table(df_result)
app.place(table)

button = app.button(text="Click to compute a dataframe")
computed_df = dsl_op.computed_dataframe(df_result)
button.on_click([computed_df])
app.place(button)

table2 = app.table(computed_df)
app.place(table2)

client.register_data_app(app)