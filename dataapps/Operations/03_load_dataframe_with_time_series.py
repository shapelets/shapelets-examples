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
    already_loaded = [
        sequence.name for sequence in client.get_collection_sequences(collection)]
    loaded = 0
    begin = time.time()
    all_begin = time.time()
    for column in df.columns:
        if column not in already_loaded:
            begin = time.time()
            client.create_sequence(dataframe=df.loc[:, column].to_frame(), name=column, collection=collection)#, starts=np.datetime64(0,'Y'), every=1)
            loaded += 1
    print(f"Loaded[{loaded}]:\t{column}\t{time.time() - begin}")
    print(f"Total elapsed: {time.time() - all_begin}​​​​​​​")


def get_collection(client: Shapelets,
collection_name: str,
collection_description: str = "No description available"
) -> Collection:
    collections = client.get_collections()
    if collection_name not in [collection.name for collection in collections]:
        client.create_collection(name=collection_name,
description=collection_description)
    collections = client.get_collections()
    return next(col for col in collections if col.name == collection_name)

# Start shapelets process and init session as admin
client = init_session("admin", "admin")

# Create a dataApp
app = DataApp(
    name="03_load_dataframe_with_time_series",
    description="This Dataapp loads a dataframe containing time series"
)

app.place(app.markdown("""
  # This Dataapp loads a dataframe containing time series
"""))

#Create a sample Dataframe with random integer values
rng = pd.date_range(start = '2020-01-01', end = datetime.datetime.now(), freq='1d', tz = 'UTC')
df = pd.DataFrame(index=rng, columns=['random_series']) 
df['random_series'] = np.random.randint(0,100,df.shape[0])

#Create an empty collection
collection = get_collection(client, collection_name = "Dataframe collection",
                             collection_description="This is a collection including a Dataframe with a random time series")

#Upload the dataframe into the collection
upload_sequences(client, df, collection)

#Get the first column in the dataframe as a sequence
column = 0 
seq = client.get_collection_sequences(collection)[column]

#Create a line chart
line_chart = app.line_chart(title=seq.name, sequence=seq)
# Place line_chart into the Dataapp
app.place(line_chart)

# Register the Dataapp
client.register_data_app(app)
