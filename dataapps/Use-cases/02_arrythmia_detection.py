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
import pandas as pd

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
    loaded = 0
    begin = time.time()
    all_begin = time.time()
    for column in df.columns:
            # We upload it always no matter if it has already been uploaded
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

client = init_session("admin","admin")
app = DataApp(name="02_arrythmia_detection",
description="In this app, Data from the MIT-BIH Arrhythmia Database (mitdb) are analyzed looking for premature ventricular contractions (PVC).")

# Register custom function
client.register_custom_function(topk)

df = pd.read_csv('../Data/mitdb102.csv', header=None, index_col=0, names=['MLII', 'V1'], skiprows=200000, nrows=100000)
df.index = pd.to_datetime(df.index, unit='s')

collection = get_collection(client, collection_name = "Arrythmia dataframe collection",
                             collection_description="This is a collection including ECG Data from the MIT-BIH Arrythmia Database")

# Upload the dataframe into the collection
upload_sequences(client, df, collection)

# Get the first column in the dataframe as a sequence
seq0 = client.get_collection_sequences(collection)[0]
seq1 = client.get_collection_sequences(collection)[1]

# Create a markdown
md = app.markdown("""
  # Anomaly detection for Premature Ventricular Contraction Detection in ECG data

  ## Introduction

Premature ventricular contractions (PVCs) are a relatively common type of abnormal heartbeat (arrhythmia). The electrical events of the heart detected by the electrocardiogram (ECG) allow a PVC to be easily distinguished from a normal heart beat. Although a PVC can be a sign of decreased oxygenation to the heart muscle, often PVCs are benign and may even be found in healthy hearts.

  ## What causes PVCs?
There are certain things that can help to reinforce a premature signal in the ventricles. These include: advancing age, reduced blood flow to your heart (such as coronary artery disease), scarring after a heart attack, etc.

Many heart conditions raise the risk for PVCs, including: high blood pressure, heart attack, heart failure, coronary heart disease, etc.

They often happen in people without any heart disease. However, PVCs are somewhat more common in people with some kind of heart disease.

This use case has been first published by the research team of [Professor Eamonn Keogh](https://www.cs.ucr.edu/~eamonn/).

Here you can see how fast anomalies can be detected in large time series using an algorithm called Matrix Profile. In the following charts two ECG signals sampled every 3 ms and with a duration of 6 minutes, which corresponds to 120000 samples. One can navigate and zoom into the data very quickly and also efficiently search for the most k anomalous chunks (windows) of any given size. Try it out!
  """)
app.place(md)

# Add a horizontal flow planel
hpanel = app.horizontal_flow_panel("Select input arguments: ")
app.place(hpanel)

# Add controllers (number and slider) to the horizontal flow panel
window_size = app.number(name="Window size: ", default_value=250, value_type=int)
hpanel.place(window_size, width=6)

k = app.slider(name="K value", title="Desired number of anomalies: ", min_value=1, max_value=20, step=1,
                default_value=1, value_type=int)
hpanel.place(k, width=6)

# Compute the matrix profile and get the top k values in this profile
mp = dsl.matrix_profile_self_join(seq0, window_size)
views, max = dsl.topk(seq0, mp, k, window_size)

# Create and place a button to run the anomaly detection algorithm
button = app.button("Execute anomaly-detection", text="Execute anomaly-detection")
button.on_click([views])
app.place(button)

# Create a temporal context
tc = app.temporal_context("Temporal context")

# Plot the sequences
line_chart1 = app.line_chart(title='MLII', sequence=seq0, views=views, temporal_context=tc)
app.place(line_chart1)

line_chart2 = app.line_chart(title='V1', sequence=seq1, views=views, temporal_context=tc)
app.place(line_chart2)

# Register the DataApp
client.register_data_app(app)