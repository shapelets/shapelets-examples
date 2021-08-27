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
import requests
import pandas as pd
import numpy as np

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

def computeAvg(input1:NDArray, input2:NDArray)->NDArray:
    return NDArray((input1.values+input2.values)/2.0)

def downloadHistoricalDataComputeRollingPearson(ticker1:str, ticker2:str, history_size:str, price_type:str, window_size: int)->typing.Tuple[str,str,Sequence,Sequence,Sequence]:
    # Download maximum historical daily Data available
    import yfinance as yf

    df = yf.download(ticker1+ ' ' + ticker2, period=history_size)

    # Use differences with price Data
    if price_type!='Volume':
        df=df.diff()

    # Get companies' names
    name1 = yf.Ticker(ticker1).info['shortName']
    name2 = yf.Ticker(ticker2).info['shortName']

    # Clear dates with no Data available
    df.dropna(inplace=True)

    #Compute rolling Pearson coefficient
    df['rolling_pearson'] = df[price_type][ticker1].rolling(window=window_size, center=True).corr(df[price_type][ticker2])

    # Clear dates with no Pearson coefficient available
    df.dropna(inplace=True)

    # Fill gaps
    idx = pd.date_range(df.index[0].date(),df.index[-1].date())
    df = df.reindex(idx, fill_value=np.nan).fillna(method='ffill')

    # Convert to Sequence
    p1 = kv.Array.from_numpy(df[price_type][ticker1].to_numpy(), khiva_type=kv.array.dtype.f64)
    p1_column_info_entry = ColumnProtoEntry(sourceName=price_type + ' '+ ticker2, columnProtoEntryDataType=DT_NUMERICAL)
    p1_column_info = ColumnProto(columnDimensions=UNIDIMENSIONAL, columnProtoEntries=[p1_column_info_entry])
    p2 = kv.Array.from_numpy(df[price_type][ticker2].to_numpy(), khiva_type=kv.array.dtype.f64)
    p2_column_info_entry = ColumnProtoEntry(sourceName=price_type + ' '+ ticker1, columnProtoEntryDataType=DT_NUMERICAL)
    p2_column_info = ColumnProto(columnDimensions=UNIDIMENSIONAL, columnProtoEntries=[p2_column_info_entry])
    rp = kv.Array.from_numpy(df['rolling_pearson'].to_numpy(), khiva_type=kv.array.dtype.f64)
    rp_column_info_entry = ColumnProtoEntry(sourceName=f"rolling_pearson", columnProtoEntryDataType=DT_NUMERICAL)
    rp_column_info = ColumnProto(columnDimensions=UNIDIMENSIONAL, columnProtoEntries=[rp_column_info_entry])
    sequence_axis = kv.Array.from_numpy(df.index.astype('uint64').to_numpy(), khiva_type=kv.array.dtype.u64)
    starts0 = int(df.index[0].timestamp()*1000)
    starts1 = int(df.index[1].timestamp()*1000)
    every = (starts1-starts0)
    sequence_axis_info = AxisProto(axisName="axis",
                                   densityType=DENSE_REGULAR,
                                   axisType=ORDINAL_AXIS,
                                   starts=starts0,
                                   every=every)
    seq_p1 = ShapeletsSequence(sequence_axis,[p1],p1_column_info_entry.sourceName,
                               NUMERIC,sequence_axis_info,p1_column_info,"")
    seq_p2 = ShapeletsSequence(sequence_axis,[p2],p2_column_info_entry.sourceName,
                               NUMERIC,sequence_axis_info,p2_column_info,"")
    seq_rp = ShapeletsSequence(sequence_axis,[rp],rp_column_info_entry.sourceName,
                               NUMERIC,sequence_axis_info,rp_column_info,"")

    return name1, name2, seq_p1, seq_p2, seq_rp

client = init_session("admin","admin")
app = DataApp(name="01_anomaly_search_in_stocks_correlation",
description="In this app, historical Data from two stocks are downloaded from Yahoo finance and their rolling "
            "pearson correlation coefficient is computed. We then search for anomalies in their correlation.")

# Register custom function
client.register_custom_function(topk)
client.register_custom_function(computeAvg)
client.register_custom_function(downloadHistoricalDataComputeRollingPearson)

# Get list of Yahoo symbols
url='https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv'
s=requests.get(url).content
symbols_df=pd.read_csv(io.StringIO(s.decode('utf-8')), header=None, names=['tickers']).sort_values(by='tickers')

# Convert df to list
list_of_symbols = symbols_df['tickers'].values.tolist()

# Set price type (Adj Close, Open, High, Low, Close or Volume)
hpanel = app.horizontal_flow_panel("Select Data to analyze and period of analysis: ")
app.place(hpanel)
price_type = app.selector([{'value':'Adj Close','label':'Δ Adj Close'},
                           {'value':'Open','label':'Δ Open'},
                           {'value':'High','label':'Δ High'},
                           {'value':'Low','label':'Δ Low'},
                           {'value':'Close','label':'Δ Close'},
                           {'value':'Volume','label':'Volume'}], index_by='value', value_by='value', label_by='label', value='Adj Close')
hpanel.place(price_type, width=6)

history_size = app.selector([{'value':'6mo','label':'6 months'},
                             {'value':'1y','label':'1 year'},
                             {'value':'2y','label':'2 years'},
                             {'value':'5y','label':'5 years'},
                             {'value':'10y','label':'10 years'},
                             {'value':'max','label':'Maximum'}], index_by='value', value_by='value', label_by='label', value='max')

hpanel.place(history_size, width=6)

# Create stock selectors
hpanel1 = app.horizontal_flow_panel("Select stock symbols from Yahoo Finance: ")
app.place(hpanel1)
ticker1 = app.selector(list_of_symbols,value=list_of_symbols[0])
hpanel1.place(ticker1, width=6)
ticker2 = app.selector(list_of_symbols,value=list_of_symbols[1])
hpanel1.place(ticker2, width=6)

# Add controllers
hpanel2 = app.horizontal_flow_panel("Select input arguments: ")
app.place(hpanel2)
window_size = app.number(name="Window size value", default_value=30, value_type=int)
hpanel2.place(window_size, width=6)

k = app.slider(name="K value", title="Desired number of anomalies: ", min_value=1, max_value=20, step=1,
                default_value=3, value_type=int)
hpanel2.place(k, width=6)

# Download historical Data and compute rolling Pearson
name1, name2, prices1, prices2, rp = dsl.downloadHistoricalDataComputeRollingPearson(ticker1,
                                                                                     ticker2,
                                                                                     history_size,
                                                                                     price_type,
                                                                                     window_size)
# Execute matrix profile algorithm
mp1 = dsl.matrix_profile_self_join(prices1, window_size)
mp2 = dsl.matrix_profile_self_join(prices2, window_size)
mp_avg = dsl.computeAvg(mp1, mp2)
mp_rp = dsl.matrix_profile_self_join(rp, window_size)
views_rp, max_rp = dsl.topk(rp, mp_rp, k, window_size)
views_avg, max_avg = dsl.topk(prices1, mp_avg, k, window_size)

button2 = app.button("Execute anomaly-detection", text="Execute anomaly-detection")
button2.on_click([name1, name2, prices1, prices2, rp, mp1, mp2, mp_avg, mp_rp, views_rp, views_avg])
app.place(button2)

# Create temporal context
tc = app.temporal_context("Temporal context")

# Show companies' names and plot price Data
label1 = app.label(name1)
app.place(label1)
line_chart1 = app.line_chart(title='Stock 1', sequence=prices1, temporal_context=tc)
app.place(line_chart1)

label2 = app.label(name2)
app.place(label2)
line_chart2 = app.line_chart(title='Stock 2', sequence=prices2, temporal_context=tc)
app.place(line_chart2)

# Create rolling Pearson plot
line_chart3 = app.line_chart(title='Avg Profile Stock 1', sequence=prices1, views=views_avg, temporal_context=tc)
app.place(line_chart3)

# Create rolling Pearson plot
line_chart4 = app.line_chart(title='Avg Profile Stock 1', sequence=prices2, views=views_avg, temporal_context=tc)
app.place(line_chart4)

# Create rolling Pearson plot
line_chart5 = app.line_chart(title='Rolling Pearson', sequence=rp, views=views_rp, temporal_context=tc)
app.place(line_chart5)

# Register DataApp
client.register_data_app(app)