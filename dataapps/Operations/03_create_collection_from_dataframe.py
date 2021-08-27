# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets import Shapelets
from shapelets.model import Collection
import pandas as pd
import numpy as np
import time
import datetime

def upload_sequences(client: Shapelets, df: pd.DataFrame, collection: Collection):
    already_loaded = [sequence.name for sequence in client.get_collection_sequences(collection)]
    loaded = 0
    begin = time.time()
    all_begin = time.time()
    for column in df.columns:
        if column not in already_loaded:
            begin = time.time()
            client.create_sequence(dataframe=df.loc[:, column].to_frame(), name=column, collection=collection)
            loaded += 1
    print(f"Loaded[{loaded}]:\t{column}\t{time.time() - begin}")
    print(f"Total elapsed: {time.time() - all_begin}")


def get_collection(client: Shapelets, collection_name: str, collection_description: str = "No description available") -> Collection:
    collections = client.get_collections()
    if collection_name not in [collection.name for collection in collections]:
        client.create_collection(name=collection_name,description=collection_description)
    collections = client.get_collections()
    return next(col for col in collections if col.name == collection_name)

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(name="03_create_collection_from_dataframe",
              description="This Dataapp creates a collection from a dataframe, uploads it, "
                          "retrieves one of its columns as a sequence and plots it")

app.place(app.markdown("""
  # This Dataapp creates a collection from a dataframe, uploads it, 
  retrieves one of its columns as a sequence and plots it
""".replace("\n","")))

# Create a sample dataframe with a datetime index
rng = pd.date_range(start = '2020-01-01', end = datetime.datetime.now(), freq='1d', tz = 'UTC')
df = pd.DataFrame(index=rng, columns=['random_series'])

# Add two columns with random integer values, from 0 to 10 and from 0 to 100
df['random_series_10'] = np.random.randint(0,10,df.shape[0])
df['random_series_100'] = np.random.randint(0,100,df.shape[0])

# Create an empty collection
collection = get_collection(client, collection_name = "Dataframe collection",
                             collection_description="This is a collection including a Dataframe with two random time series")

# Upload the dataframe into the collection
upload_sequences(client, df, collection)

# Get the sequences from the collection, in the same column order as they appear in the dataframe
# and holding the index information
# Sequence indices start from 1 (0 corresponds to the dataframe index)
seq_10 = client.get_collection_sequences(collection)[1]
seq_100 = client.get_collection_sequences(collection)[2]

# Create a line chart
line_chart_10 = app.line_chart(title=seq_10.name, sequence=seq_10)
line_chart_100 = app.line_chart(title=seq_100.name, sequence=seq_100)

# Place line_chart into the Dataapp
app.place(line_chart_10)
app.place(line_chart_100)

# Register the Dataapp
client.register_data_app(app)
