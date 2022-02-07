# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import numpy as np
from shapelets import init_session, Shapelets
from shapelets.dsl.data_app import DataApp, Image, LineChart
from shapelets.model import Collection, Sequence
from shapelets.model.view_match import View
import time
import pandas as pd
import json
from matplotlib import pyplot as plt
import scipy.stats as stats
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import changefinder
import pyscamp as scamp
import builtins

# Function that computes the top k anomalies given a sequence, its matrix profile and the window size of the anomalies
def topk(seq: Sequence, profile: np.array, k: int, window_size: int):
    starts = seq.axis.starts
    every = seq.axis.every
    result = list()
    distances = profile
    for x in range(k):
        anomaly_idx = np.array(distances).argmax()
        start = int(anomaly_idx)
        end = start + window_size
        view = View(seq, starts + (start * every), starts + (end * every))
        result.append(view)
        distances[builtins.max(0, start - window_size):builtins.min(end + window_size, len(distances))] = -np.inf
    return result

# Init session
client = init_session("admin","admin")

# Instantiate a new data app
app = DataApp(name="03_industrial_machine_anomaly_detection",
description="In this dataapp, we predict machine failures using historical anomaly data.")

# Create a markdown object
md = app.markdown("""
  # Predictive maintenance using anomaly detection

  ## Introduction

  For this use case, we will use data from the public """
"""[Numenta Anomaly Benchmark (NAB)](https://github.com/numenta/NAB). This benchmark, designed for the comparison """
"""of anomaly detection algorithms, contains 58 hand-labeled data files corresponding to different real-world """
"""scenarios where anomaly detection is relevant. For this use case, temperature sensor data from an internal """
"""component of a large, expensive, industrial machine will be used. The objective will be to find a model that """
"""can be used in order to try to detect the annotated anomalies.""")
app.place(md)

# Load the data into a dataframe
df = pd.read_csv('../Data/nab/realKnownCause/machine_temperature_system_failure.csv')

df['timestamp'] = pd.to_datetime(df['timestamp'],format="%Y-%m-%d %H:%M:%S")

with open('../Data/nab/labels/combined_windows.json') as f:
  anomaly_points = json.load(f)['realKnownCause/machine_temperature_system_failure.csv']

df['anomaly'] = 0
for start, end in anomaly_points:
    df.loc[((df['timestamp'] >= start) & (df['timestamp'] <= end)), 'anomaly'] = 1

df['year'] = df['timestamp'].apply(lambda x : x.year)
df['month'] = df['timestamp'].apply(lambda x : x.month)
df['week'] = df['timestamp'].apply(lambda x : x.week)
df['day'] = df['timestamp'].apply(lambda x : x.day)
df['hour'] = df['timestamp'].apply(lambda x : x.hour)
df['minute'] = df['timestamp'].apply(lambda x : x.minute)
df.index = df['timestamp']

md2 = app.markdown("""
## Exploratory data analysis (EDA)

Let's start exploring the data by plotting the raw temperature values.""")
app.place(md2)

fig8a = plt.figure(figsize=(10,4))
plt.plot(df['value'])
plt.title('Raw temperatures')
img8a = Image(fig8a)
app.place(img8a)

md3 = app.markdown("""
We can see that the data has been captured during a period of three months, from December 2013 to February 2014. """
"""We can also see how raw temperature values are a bit noisy. We can smooth them out by plotting the daily average """
"""instead.""")
app.place(md3)

fig8 = plt.figure(figsize=(10,4))
plt.plot(df['value'].resample('D').mean())
plt.title('Daily temperatures')
img8 = Image(fig8)
app.place(img8)

md4 = app.markdown("""
In order to check the consistency of the data, we can arrange it in weeks and years and plot the count of data """
"""points.""")
app.place(md4)

# Bar plots
fig1, ax1 = plt.subplots(figsize=(10,4))
df.loc[(df['week']==1) & (df['month']==12),'year']+=1 # Fix visualization for first week of 2014
df.groupby(['year','week'])['value'].count().unstack().plot.bar(ax=ax1)
plt.title('Year/Week Count')
img1 = Image(fig1)
app.place(img1)

md5 = app.markdown("""
The plot looks fine, with data starting to be captured during the 49th week of 2013 and finishing before the """
"""end of the 8th week of 2014. During the rest of the weeks we can see that the number of data points remains """
"""constant: 2000 per week corresponding to one data point every 5 minutes. In fact, the original data has some """
"""duplicated data points, which have been detected and removed thanks to this visualization in order to obtain the """
"""final data we will be using. Now let's check the evolution of the min, max and mean temperatures for each week.""")
app.place(md5)

fig2, ax2 = plt.subplots(figsize=(10,4))
data_mean=df.groupby(['year','week']).agg({'value': 'mean'})['value']
data_max=df.groupby(['year','week']).agg({'value': 'max'})['value']
data_min=df.groupby(['year','week']).agg({'value': 'min'})['value']
labels = ['Week '+str(week)+' '+str(year) for year,week in data_mean.index]
plt.plot(labels,data_mean.values)
plt.plot(labels,data_max.values)
plt.plot(labels,data_min.values)
plt.xticks(rotation=90)
plt.title('Year/Week Mean Temperature')
plt.legend(['Mean','Max','Min'])
img2 = Image(fig2)
app.place(img2)

md6 = app.markdown("""
The average temperature ranges between 80 and 100 degrees Celsius, with the maximum temperature oscillating around """
"""100 degrees. The minimum temperatures have the largest oscillations, between 0 and 80 Celsius degrees. Let's """
"""plot some temperature distribution graphs to understand how temperatures are distributed over the different """
"""periods.""")
app.place(md6)

fig5 = plt.figure(figsize=(10,4))
density = df['value'].plot.kde().get_lines()[0].get_xydata()
plt.fill(density[:,0],density[:,1],alpha=0.3)
plt.grid()
plt.title('Temperature distribution')
img5 = Image(fig5)
app.place(img5)

fig6 = plt.figure(figsize=(10,4))
density_2013 = df.loc[df['year']==2013,'value'].plot.kde().get_lines()[0].get_xydata()
density_2014 = df.loc[df['year']==2014,'value'].plot.kde().get_lines()[1].get_xydata()
plt.fill(density_2013[:,0],density_2013[:,1],alpha=0.3)
plt.fill(density_2014[:,0],density_2014[:,1],alpha=0.3)
plt.grid()
plt.legend(['2013','2014'])
plt.title('Temperature distribution by year')
img6 = Image(fig6)
app.place(img6)

fig7 = plt.figure(figsize=(10,4))
density_12 = df.loc[df['month']==12,'value'].plot.kde().get_lines()[0].get_xydata()
density_1 = df.loc[df['month']==1,'value'].plot.kde().get_lines()[1].get_xydata()
density_2 = df.loc[df['month']==2,'value'].plot.kde().get_lines()[2].get_xydata()
plt.fill(density_12[:,0],density_12[:,1],alpha=0.3)
plt.fill(density_1[:,0],density_1[:,1],alpha=0.3)
plt.fill(density_2[:,0],density_2[:,1],alpha=0.3)
plt.grid()
plt.legend(['12','1','2'])
plt.title('Temperature distribution by month')
img7 = Image(fig7)
app.place(img7)

md7 = app.markdown("""
These charts allow us to understand what are the typical temperature ranges in general and also in each period."""
"""They can be extremely useful to quickly identify the most abnormal periods, in this case, December 2013. """
"""It's time to check the annotated anomalies, shown in blue.""")
app.place(md7)

fig9 = plt.figure(figsize=(10,4))
plt.plot(df['value'],'k')
plt.plot(df.loc[df['anomaly']==1,'value'],'.b')
plt.title('Normal/Abnormal temperatures labelled')
img9 = Image(fig9)
app.place(img9)

md9 = app.markdown("""
We can see that there are four abnormal periods. We do not have information about the first """
"""anomaly. According to the authors of the dataset, the second anomaly was a planned shutdown. The last anomaly """
"""is a catastrophic system failure. The third anomaly, a subtle but observable change in the behavior, indicated """
"""the actual onset of the problem that led to the eventual system failure.

## Model comparison and selection

In this section we will try to find a model that can help us predict abnormal points. The problem will thus """
"""be posed as a classification problem that takes a data point and classifies it as either normal or abnormal. For """
"""this, we will analyze seven methods/models for anomaly detection:
- Hotelling's T^2
- One-class SVM
- iForest algorithm
- Local outlier factor
- Changefinder algorithm
- Standard deviation filter
- Matrix profile

We will compare the performance of these methods using four metrics:
- Missed alarm rate, that describes the amount of false negatives with respect to all abnormal data points.
- False alarm rate, that describes the amount of false positives with respect to all regular data points.
- Recall, a common metric that measures the amount of true positives (anomalies) predicted with respect to all positives.
- Execution time, which describes the speed of each algorithm.
""")
app.place(md9)

# Hotelling's T2
hotelling_df = pd.DataFrame()
hotelling_df['value'] = df['value']
start_time = time.time()
mean = hotelling_df['value'].mean()
std = hotelling_df['value'].std()
hotelling_df['anomaly_score'] = [((x - mean)/std) ** 2 for x in hotelling_df['value']]
hotelling_df['anomaly_threshold'] = stats.chi2.ppf(q=0.95, df=1)
hotelling_df['anomaly']  = hotelling_df.apply(lambda x : 1 if x['anomaly_score'] > x['anomaly_threshold'] else 0,
                                              axis=1)
hotelling_time = time.time() - start_time

# One-class SVM
ocsvm_model = OneClassSVM(nu=0.2, gamma=0.001, kernel='rbf')
start_time = time.time()
ocsvm_ret = ocsvm_model.fit_predict(df['value'].values.reshape(-1, 1))
ocsvm_df = pd.DataFrame()
ocsvm_df['value'] = df['value']
ocsvm_df['anomaly']  = [1 if i==-1 else 0 for i in ocsvm_ret]
ocsvm_time= time.time() - start_time

# iForest
iforest_model = IsolationForest(n_estimators=300, contamination=0.1, max_samples=700)
start_time = time.time()
iforest_ret = iforest_model.fit_predict(df['value'].values.reshape(-1, 1))
iforest_df = pd.DataFrame()
iforest_df['value'] = df['value']
iforest_df['anomaly'] = [1 if i==-1 else 0 for i in iforest_ret]
iforest_time = time.time() - start_time

# Local Outlier Factor
lof_model = LocalOutlierFactor(n_neighbors=600, contamination=0.05)
start_time = time.time()
lof_ret = lof_model.fit_predict(df['value'].values.reshape(-1, 1))
lof_df = pd.DataFrame()
lof_df['value'] = df['value']
lof_df['anomaly'] = [1 if i==-1 else 0 for i in lof_ret]
lof_time = time.time() - start_time

# ChangeFinder
cf_model = changefinder.ChangeFinder(r=0.002, order=1, smooth=300)
start_time = time.time()
ch_df = pd.DataFrame()
ch_df['value'] = df['value']
ch_df['anomaly_score'] = [cf_model.update(i) for i in ch_df['value']]
ch_score_q1 = stats.scoreatpercentile(ch_df['anomaly_score'], 25)
ch_score_q3 = stats.scoreatpercentile(ch_df['anomaly_score'], 75)
ch_df['anomaly_threshold'] = ch_score_q3 + (ch_score_q3 - ch_score_q1) * 2
ch_df['anomaly']  = ch_df.apply(lambda x : 1 if x['anomaly_score'] > x['anomaly_threshold'] else 0, axis=1)
ch_time = time.time() - start_time

# Standard deviation
start_time = time.time()
sigma_df = pd.DataFrame()
sigma_df['value'] = df['value']
mean = sigma_df['value'].mean()
std = sigma_df['value'].std()
sigma_df['anomaly_threshold_3r'] = mean + 2*std
sigma_df['anomaly_threshold_3l'] = mean - 2*std
sigma_df['anomaly'] = sigma_df.apply(lambda x : 1 if (x['value'] > x['anomaly_threshold_3r']) or
                                                     (x['value'] < x['anomaly_threshold_3l']) else 0,
                                     axis=1)
sigma_time = time.time() - start_time

# Matrix profile
window_size=650
start_time = time.time()
mp = scamp.selfjoin(df['value'].values,window_size)
seq = client.create_sequence(dataframe=df['value'].to_frame(), name='value', collection=None)
views = topk(seq,mp[0],4,window_size)
mp_df = pd.DataFrame(0, columns=['anomaly'], index=df.index)
for view in views:
    mp_df[pd.to_datetime(view.begin, unit='ms'):pd.to_datetime(view.end,unit='ms')] = 1
mp_time = time.time() - start_time

# Compute metrics
hotelling_conf_matrix = confusion_matrix(df['anomaly'], hotelling_df['anomaly'])
hotelling_FAR=hotelling_conf_matrix[0][1]/(hotelling_conf_matrix[0][1]+hotelling_conf_matrix[0][0])
hotelling_MAR=hotelling_conf_matrix[1][0]/(hotelling_conf_matrix[1][1]+hotelling_conf_matrix[1][0])
hotelling_recall = recall_score(df['anomaly'], hotelling_df['anomaly'])

ocsvm_conf_matrix = confusion_matrix(df['anomaly'], ocsvm_df['anomaly'])
ocsvm_FAR=ocsvm_conf_matrix[0][1]/(ocsvm_conf_matrix[0][1]+ocsvm_conf_matrix[0][0])
ocsvm_MAR=ocsvm_conf_matrix[1][0]/(ocsvm_conf_matrix[1][1]+ocsvm_conf_matrix[1][0])
ocsvm_recall = recall_score(df['anomaly'], ocsvm_df['anomaly'])


iforest_conf_matrix = confusion_matrix(df['anomaly'], iforest_df['anomaly'])
iforest_FAR=iforest_conf_matrix[0][1]/(iforest_conf_matrix[0][1]+iforest_conf_matrix[0][0])
iforest_MAR=iforest_conf_matrix[1][0]/(iforest_conf_matrix[1][1]+iforest_conf_matrix[1][0])
iforest_recall = recall_score(df['anomaly'], iforest_df['anomaly'])

lof_conf_matrix = confusion_matrix(df['anomaly'], lof_df['anomaly'])
lof_FAR=lof_conf_matrix[0][1]/(lof_conf_matrix[0][1]+lof_conf_matrix[0][0])
lof_MAR=lof_conf_matrix[1][0]/(lof_conf_matrix[1][1]+lof_conf_matrix[1][0])
lof_recall = recall_score(df['anomaly'], lof_df['anomaly'])

ch_conf_matrix = confusion_matrix(df['anomaly'], ch_df['anomaly'])
ch_FAR=ch_conf_matrix[0][1]/(ch_conf_matrix[0][1]+ch_conf_matrix[0][0])
ch_MAR=ch_conf_matrix[1][0]/(ch_conf_matrix[1][1]+ch_conf_matrix[1][0])
ch_recall = recall_score(df['anomaly'], ch_df['anomaly'])


sigma_conf_matrix = confusion_matrix(df['anomaly'], sigma_df['anomaly'])
sigma_FAR=sigma_conf_matrix[0][1]/(sigma_conf_matrix[0][1]+sigma_conf_matrix[0][0])
sigma_MAR=sigma_conf_matrix[1][0]/(sigma_conf_matrix[1][1]+sigma_conf_matrix[1][0])
sigma_recall = recall_score(df['anomaly'], sigma_df['anomaly'])

mp_conf_matrix = confusion_matrix(df['anomaly'], mp_df['anomaly'])
mp_FAR=mp_conf_matrix[0][1]/(mp_conf_matrix[0][1]+mp_conf_matrix[0][0])
mp_MAR=mp_conf_matrix[1][0]/(mp_conf_matrix[1][1]+mp_conf_matrix[1][0])
mp_recall = recall_score(df['anomaly'], mp_df['anomaly'])

fig22 = plt.figure(figsize=(10,4))
scores = [hotelling_MAR,ocsvm_MAR,iforest_MAR,lof_MAR,ch_MAR,sigma_MAR,mp_MAR]
names = ['hotelling','ocsvm','iforest','lof','ch','sigma','matrix profile']
plt.title('Missed alarm rate for all methods tested')
plt.bar(names,height=scores)
img22 = Image(fig22)
app.place(img22)

fig21 = plt.figure(figsize=(10,4))
scores = [hotelling_FAR,ocsvm_FAR,iforest_FAR,lof_FAR,ch_FAR,sigma_FAR,mp_FAR]
names = ['hotelling','ocsvm','iforest','lof','ch','sigma','matrix profile']
plt.title('False alarm rate score for all methods tested')
plt.bar(names,height=scores)
img21 = Image(fig21)
app.place(img21)

md10 = app.markdown("""
Depending on the cost of a missed alarm and the cost of verifying an alarm, some models may be more interesting """
"""than others. As in many classification problems, a tradeoff has to be found between a large number of """
"""false alarms or missed issues. In this context of anomaly detection, in which not detecting an anomaly can """
"""cause the shutdown of the machine or the industrial process, recall (detected anomalies over total """
"""number of anomalies) is in general another good metric to choose.""")
app.place(md10)

fig18 = plt.figure(figsize=(10,4))
scores = [hotelling_recall,ocsvm_recall,iforest_recall,lof_recall,ch_recall,sigma_recall,mp_recall]
names = ['hotelling','ocsvm','iforest','lof','ch','sigma','matrix profile']
plt.title('Recall for all methods tested')
plt.bar(names,height=scores)
img18 = Image(fig18)
app.place(img18)

md11 = app.markdown("""One-class SVM and iForest show high recall, but their false alarm rate is also quite high. """
"""Both Hotelling's T^2 and the standard deviation model show a good tradeoff, with similar results between """
"""both of them. Let's compare the speed of these algorithms.""")
app.place(md11)

# Plot execution times
fig22= plt.figure(figsize=(10,4))
scores = [hotelling_time,ocsvm_time,iforest_time,lof_time,ch_time,sigma_time,mp_time]
names = ['hotelling','ocsvm','iforest','lof','ch','sigma','matrix profile']
plt.title('Execution time in seconds for all methods tested')
plt.bar(names,height=scores)
img22 = Image(fig22)
app.place(img22)

md12 = app.markdown("""
Both algorithms also show similar execution times. Although Hotelling's T^2 seems to perform slightly better, we"""
""" will choose the standard deviation method due to its simplicity, as it only has one parameter. Let's try to """
""" run a parameter search on this model to try to further improve it. In this case, we will minimize the sum of """
""" the missed alarm rate and the false alarm rate.""")
app.place(md12)

# Sigma model optimization
sigma_df = pd.DataFrame()
sigma_df['value'] = df['value']
mean = sigma_df['value'].mean()
std = sigma_df['value'].std()
param_list = []
space = np.arange(0.5,2.0,0.01)
for k in space:
    sigma_df['anomaly_threshold_3r'] = mean + k*std
    sigma_df['anomaly_threshold_3l'] = mean - k*std
    sigma_df['anomaly'] = sigma_df.apply(lambda x : 1 if (x['value'] > x['anomaly_threshold_3r']) or
                                                         (x['value'] < x['anomaly_threshold_3l']) else 0, axis=1)
    sigma_conf_matrix = confusion_matrix(df['anomaly'], sigma_df['anomaly'])
    sigma_FAR = sigma_conf_matrix[0][1] / (sigma_conf_matrix[0][1] + sigma_conf_matrix[0][0])
    sigma_MAR = sigma_conf_matrix[1][0] / (sigma_conf_matrix[1][1] + sigma_conf_matrix[1][0])
    param_list.append(sigma_FAR+sigma_MAR)

opt_thr = space[param_list.index(min(param_list))]

fig24 = plt.figure(figsize=(10,4))
plt.plot(space,param_list)
plt.title('Recall for different thresholds')
plt.axvline(x=opt_thr,color='r')
img24 = Image(fig24)
app.place(img24)

md13 = app.markdown("""
Once the model parameter has been optimized, we can check its performance. Since we do not have a test sequence, """
""" we will evaluate it in the original sequence for simplicity, although a hold out set should be used in a real """
""" application to avoid overfitting.""")
app.place(md13)

# Get optimized model
sigma_df['anomaly_threshold_3r'] = mean + opt_thr * std
sigma_df['anomaly_threshold_3l'] = mean - opt_thr * std
sigma_df['anomaly'] = sigma_df.apply(
    lambda x: 1 if (x['value'] > x['anomaly_threshold_3r']) or (x['value'] < x['anomaly_threshold_3l']) else 0, axis=1)

fig25 = plt.figure(figsize=(10,4))
plt.plot(df['value'],'k')
plt.plot(sigma_df.loc[(df['anomaly']==1) & (sigma_df['anomaly']==1),'value'],'.g')
plt.plot(sigma_df.loc[(df['anomaly']==1) & (sigma_df['anomaly']==0),'value'],'.r')
plt.plot(sigma_df.loc[(df['anomaly']==0) & (sigma_df['anomaly']==1),'value'],'.y')
plt.title('Anomalies detected with an optimized variance-based method')
img25 = Image(fig25)
app.place(img25)

md14 = app.markdown("""
The previous figure shows the detected anomalies in green, the false negatives in red and the false alarms in """
"""yellow. While the number of missed alarms is quite high (there is an alarm every time the temperature drops """
"""below 65 or above 100 degrees Celsius), all missed alarms are always preceded by detected anomalies, indicating """
"""that the system could be safely used for predictive maintenance.

## Conclusion

In this data app, we have shown how anomaly detection can be used in order to prevent machine failures. We have """ 
"""explored a dataset with labelled anomalies, compared various models using relevant metrics and optimized on the """
"""best models, achieving a missed alarm rate of 39% and a false alarm rate of 6%.""")
app.place(md14)

# Register the DataApp
client.register_data_app(app)
