# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets import Shapelets
from shapelets.model import Collection
import time
from shapelets.model import Sequence
from shapelets.dsl import dsl_op as dsl
from shapelets.model.view_match import View
from shapelets.model.ndarray import NDArray
import typing
import io
import pandas as pd
import requests
from bs4 import BeautifulSoup

def topk(seq: Sequence, profile: NDArray, k: int, window_size: int) -> typing.Tuple[typing.List[View], int]:
    starts = seq.axis_info.starts
    every = seq.axis_info.every

    distances = profile.values[0]
    result = list()
    for x in range(k):
        anomaly_idx = np.array(distances).argmax()
        start = anomaly_idx
        end = start + window_size
        view = View(seq.sequence_id, starts + (start * every), starts + (end * every))
        result.append(view)
        distances[(max(0, start - window_size)):(min(end + window_size, len(distances)))] = -np.inf

    return result, 0

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
    print(f"Total elapsed: {time.time() - all_begin}​​​​​​​")


def get_collection(client: Shapelets, collection_name: str, collection_description: str = "No description available") -> Collection:
    collections = client.get_collections()
    if collection_name not in [collection.name for collection in collections]:
        client.create_collection(name=collection_name,description=collection_description)
    collections = client.get_collections()
    return next(col for col in collections if col.name == collection_name)

client = init_session("admin","admin")
app = DataApp(name="02_arrythmia_detection",
description="In this app, data from the MIT-BIH Arrhythmia Database (mitdb) are retrieved.")

# Register custom function
client.register_custom_function(topk)

html_doc = requests.get('https://archive.physionet.org/cgi-bin/atm/ATM?tool=samples_to_csv&database=mitdb&rbase=102')
soup = BeautifulSoup(html_doc.content, 'html.parser')
section = soup.find(id='page').find_all('pre')
csv_content = section[1].text

df = pd.read_csv(io.StringIO(csv_content), header=None, index_col=0, names=['MLII', 'V1'], skiprows=50000, nrows=10000)
df.index = pd.to_datetime(df.index, unit='s')

collection = get_collection(client, collection_name = "Arrythmia dataframe collection",
                             collection_description="This is a collection including a ECG data")

# Upload the dataframe into the collection
upload_sequences(client, df, collection)

# Get the first column in the dataframe as a sequence
seq0 = client.get_collection_sequences(collection)[0]
seq1 = client.get_collection_sequences(collection)[1]

# Add controllers
hpanel = app.horizontal_flow_panel("Select input arguments: ")
app.place(hpanel)
window_size = app.number(name="Window size value", default_value=250, value_type=int)
hpanel.place(window_size, width=6)

#k = app.slider(name="K value", title="Desired number of anomalies: ", min_value=1, max_value=20, step=1,
#                default_value=1, value_type=int)
#hpanel.place(k, width=6)
k=app.number(value_type=int)
hpanel.place(k,width=6)

mp = dsl.matrix_profile_self_join(seq0, window_size)
views, max = dsl.topk(seq0, mp, k, window_size)

button = app.button("Execute anomaly-detection", text="Execute anomaly-detection")
button.on_click([views])
app.place(button)

# Create temporal context
tc = app.temporal_context("Temporal context")

# Show data
line_chart1 = app.line_chart(title='MLII', sequence=seq0, views=views, temporal_context=tc)
app.place(line_chart1)

line_chart2 = app.line_chart(title='V1', sequence=seq1, views=views, temporal_context=tc)
app.place(line_chart2)

# Register DataApp
client.register_data_app(app)