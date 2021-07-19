# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
from shapelets import init_session
from shapelets.dsl.data_app import DataApp
from shapelets.model import Sequence
from shapelets.dsl import dsl_op as dsl
from shapelets.model.view_match import View
from shapelets.model.ndarray import NDArray
import typing
import io
import pandas as pd
import requests
from bs4 import BeautifulSoup

def createSequences(csv_content:str)->str: #->typing.Tuple[Sequence, Sequence]
    df = pd.read_csv(csv_content, header=None, skiprows=[0, 1], index_col=0, names=['MLII', 'V1'])

    #Convert to Sequences
    s1 = kv.Array.from_numpy(df['MLII'].to_numpy(), khiva_type=kv.array.dtype.f64)
    s1_column_info_entry = ColumnProtoEntry(sourceName='MLII', columnProtoEntryDataType=DT_NUMERICAL)
    s1_column_info = ColumnProto(columnDimensions=UNIDIMENSIONAL, columnProtoEntries=[s1_column_info_entry])
    s2 = kv.Array.from_numpy(df['V1'].to_numpy(), khiva_type=kv.array.dtype.f64)
    s2_column_info_entry = ColumnProtoEntry(sourceName='V1', columnProtoEntryDataType=DT_NUMERICAL)
    s2_column_info = ColumnProto(columnDimensions=UNIDIMENSIONAL, columnProtoEntries=[s2_column_info_entry])
    sequence_axis = kv.Array.from_numpy(df.index.astype('uint64').to_numpy(), khiva_type=kv.array.dtype.u64)
    starts0 = int(df.index[0].timestamp()*1000)
    starts1 = int(df.index[1].timestamp()*1000)
    every = (starts1-starts0)
    sequence_axis_info = AxisProto(axisName="axis",
                                   densityType=DENSE_REGULAR,
                                   axisType=ORDINAL_AXIS,
                                   starts=starts0,
                                   every=every)
    seq1 = ShapeletsSequence(sequence_axis,[s1],s1_column_info_entry.sourceName,
                               NUMERIC,sequence_axis_info,s1_column_info,"")
    seq2 = ShapeletsSequence(sequence_axis,[s2],s2_column_info_entry.sourceName,
                               NUMERIC,sequence_axis_info,s2_column_info,"")

    return seq1, seq2

client = init_session("admin","admin")
app = DataApp(name="02_arrythmia_detection",
description="In this app, data from the MIT-BIH Arrhythmia Database (mitdb) are retrieved.")

html_doc = requests.get('https://archive.physionet.org/cgi-bin/atm/ATM?tool=samples_to_csv&database=mitdb&rbase=102')
soup = BeautifulSoup(html_doc.content, 'html.parser')
section = soup.find(id='page').find_all('pre')
csv_content = io.StringIO(section[1].text)

# Register custom function
client.register_custom_function(createSequences)

seq1, seq2 = createSequences(csv_content)

# Create temporal context
tc = app.temporal_context("Temporal context")

# Show companies' names and plot price data
line_chart1 = app.line_chart(title='MLII', sequence=seq1, temporal_context=tc)
app.place(line_chart1)

line_chart2 = app.line_chart(title='V1', sequence=seq2, temporal_context=tc)
app.place(line_chart2)

# Register DataApp
client.register_data_app(app)