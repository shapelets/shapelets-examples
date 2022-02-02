# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

# Shapelets
from shapelets import init_session
from shapelets.dsl.data_app import DataApp

# Pandas and numpy
import pandas as pd
import numpy as np

# Plotting tools
import seaborn as sns
import matplotlib.pyplot as plt

# Fit models
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# Scoring functions
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, confusion_matrix

# Initialize a session and create the DataApp
client = init_session("admin","admin")
app = DataApp(name="01_bank_customer_churn_prediction",
description="In this dataapp, a study of churn in bank customers is performed.")

# Read the data
df = pd.read_csv('../Data/bank_customer_churn.csv')

# Add markdown text
md = app.markdown("""
  # Using Shapelets to prevent bank customer churn

  ## 1. Introduction
In this study, we aim to accomplish the following tasks:

- Identify and visualize factors contributing to customer churn
- Build a prediction model that will perform the following:

a) Classify whether a customer is going to churn or not\n
b) Obtain churn probability as part of the previous classification, to make it easier for customer service to target 
low-hanging fruits in their efforts to prevent churn\n

## 2. Data set review
In this section we seek to explore the structure of our data, in order to understand the input space the data set
and to prepare the sets for exploratory and prediction tasks.

The dataset contains data from 10000 customers with 20 features and a label indicating churn named "exited". 
Let's review these features further to identify what attributes will be necessary and what data manipulation needs to be
 carried out before exploratory analysis and prediction modelling. The following features are available:\n
**Customer identification information** (2 features)\n
customer_id - Customer id\n
branch_code - Branch Code for customer account\n
**Demographic information about customers** (7 features)\n
surname - Surname of customer\n
gender - Gender of customer\n
age - Age of customer\n
dependents_no - Number of dependents\n
occupation - Occupation of the customer\n
city - City of customer (anonymized)\n
country - Country of customer \n
**Customer Bank Relationship** (8 features)\n
salary - Estimated customer salary\n
net_worth_level - Net worth of customer (3:Low 2:Medium 1:High)\n
tenure - Years with the bank\n
credit_score - Credit score\n
num_products - Number of products\n
has_cr_card - Indicates whether the client has a credit card\n
is_active - Indicates whether the client is active\n
days_since_last_transaction - No of Days Since Last Credit in Last 1 year\n
**Transactional Information** (3 features)\n
current_balance - Balance as of today\n
current_month_credit - Total Credit Amount current month\n
current_month_debit - Total Debit Amount current month\n
**Label**\n
exited - Whether the customer actually churned (1/0)\n

Let's take a look at the number of missing values and also the unique values for each feature.""")
app.place(md)

# Check columns with missing values
missing_values_categories = df.columns.to_numpy(dtype='str')
missing_values_count = df.isnull().sum().values

# Plot the missing values
fig_missing = plt.figure(figsize=(12,4))
plt.title('Missing values')
plt.bar(missing_values_categories,missing_values_count)
plt.xticks(missing_values_categories, rotation='vertical')
img_missing = app.image(fig_missing)
app.place(img_missing)

# Add markdown text
md1 = app.markdown("""
We can quickly identify some features that should be treated carefully as there is missing data. These include: gender, 
number of dependents, occupation, city and the number of days since last transaction. Some of these may relate to the 
way this data has been acquired or is being stored and could provide valuable feedback to the managers of this database.
We can also check the number of unique entries for each feature, to learn more about the type of features.
""")
app.place(md1)

# Check unique count for each variable
unique_values_categories = df.columns.to_numpy(dtype='str')
unique_values_count = df.nunique().values

# Create bar chart with unique values
fig_unique = plt.figure(figsize=(12,4))
plt.title('Unique values')
plt.bar(unique_values_categories,unique_values_count)
plt.xticks(unique_values_categories, rotation='vertical')
img_unique = app.image(fig_unique)
app.place(img_unique)

# Create markdown text
md2 = app.markdown("""
The data corresponds to a snapshot at some point in time (e.g. the balance is for a given date). This leads to several 
questions:
- On which date was this dataset generated and how relevant is this date?
- Would it be possible to obtain balances over a period of time as opposed to a single date?
- What does being an active member mean and are there different degrees to it? 
- Could it be better to provide transaction count both in terms of credits and debits to the account instead?
A break down to the products bought into by a customer could provide more information topping listing of product count.
 In this use case example, we proceed to model without context even though typically having context and better 
 understanding of the data extraction process would give better insight and possibly lead to better and contextual 
 results of the modelling process.

## 3. Exploratory data analysis (EDA)""")
app.place(md2)

# Plot the proportion of customers retained
labels = 'Exited', 'Retained'
sizes = [df.exited[df['exited']==1].count(), df.exited[df['exited']==0].count()]
explode = (0, 0.1)
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.title("Proportion of customers churned and retained", size = 20)
img = app.image(fig1)
app.place(img)

# Create markdown text
md3 = app.markdown('''
An immediate indicator to obtain from the dataset is that about 24% of the customers have churned. This is a static '''+
'''figure, which could and should be computed periodically to monitor how it is affected by the actions of the '''+
'''company. Let's take a look at the different features available to evaluate their influence on the customer churn.''')
app.place(md3)

# Check the churning relationship with categorical variables
fig2, axarr = plt.subplots(2, 2, figsize=(12, 12))
sns.countplot(x='country', hue='exited', data=df, ax=axarr[0][0])
sns.countplot(x='gender', hue='exited', data=df, ax=axarr[0][1])
sns.countplot(x='has_cr_card', hue='exited', data=df, ax=axarr[1][0])
sns.countplot(x='is_active', hue='exited', data=df, ax=axarr[1][1])
img2 = app.image(fig2)
app.place(img2)

# Add markdown text
md4 = app.markdown('''
From the previous charts the following can be noted:
- Majority of the data is from Portuguese customers. The proportions seem to remain constant across different '''+
'''countries.
- The proportion of female customers churning is greater than that of male customers, but overall, most churning '''+
'''customers are male.
- Interestingly, majority of the customers that churned are those with credit cards. Given that the majority of the''' +
''' customers have credit cards this could be just a coincidence.
- Non-active customers seem to churn proportionately more than active customers, which is reasonable.
- The overall proportion of inactive members is quite high suggesting that the bank may need a program implemented '''+
'''to turn this group to active customers.''')
app.place(md4)

# Check the churning relationship with continuous variables
fig3, axarr = plt.subplots(3, 2, figsize=(12, 12))
sns.boxplot(y='age',x = 'exited', hue = 'exited',data = df , ax=axarr[0][0])
sns.boxplot(y='salary',x = 'exited', hue = 'exited',data = df, ax=axarr[0][1])
sns.boxplot(y='tenure',x = 'exited', hue = 'exited',data = df, ax=axarr[1][0])
sns.boxplot(y='credit_score',x = 'exited', hue = 'exited',data = df, ax=axarr[1][1])
sns.boxplot(y='days_since_last_transaction',x = 'exited', hue = 'exited',data = df, ax=axarr[2][0])
sns.boxplot(y='current_balance',x = 'exited', hue = 'exited',data = df, ax=axarr[2][1])
img3 = app.image(fig3)
app.place(img3)

# Add markdown text
md5 = app.markdown('''
We note the following from the previous box plots:
- Age does not have a significant impact on churning.
- Customers with the highest and lowest salaries churn more.
- With regard to the tenure, churning is less common on customers that have been with the bank for several years. '''+
'''An effort in retention during the first 2-3 years could reduce churning.
- There is no significant difference in the credit score distribution between retained and churned customers.
- The same applies to the number of days since last transaction. It does not seem to have an impact on the customer '''+
'''churn.
- Balance dispersion is high and therefore its effect on the likelihood to churn cannot be concluded from the box plot.
''')
app.place(md5)

# Drop infinite values and nans
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True,how='any')

# Split into train and test data
df_train = df.sample(frac=0.8, random_state=200)
df_test = df.drop(df_train.index)

# Define continuous and categorical variables to be used in the study
continuous_vars = ['credit_score', 'age','tenure','current_balance','num_products','salary','current_month_debit',
                   'current_month_credit']
cat_vars = ['has_cr_card', 'is_active', 'country', 'gender']

# Build the dataframe holding the training data
df_train = df_train[['exited'] + continuous_vars + cat_vars]

# One hot encode the categorical variables
lst = ['country', 'gender', 'has_cr_card', 'is_active']
remove = list()
for i in lst:
    if (df_train[i].dtype == str or df_train[i].dtype == object):
        for j in df_train[i].unique():
            df_train[i+'_'+j] = np.where(df_train[i] == j,1,-1)
        remove.append(i)
df_train = df_train.drop(remove, axis=1)

# Perform MinMax scaling of the continuous variables
minVec = df_train[continuous_vars].min().copy()
maxVec = df_train[continuous_vars].max().copy()
df_train[continuous_vars] = (df_train[continuous_vars]-minVec)/(maxVec-minVec)

# Add markdown text
md16 = app.markdown('''# 4. Model fitting, model selection and classification results
We will split our dataset into training and test sets (80% - 20% of the data) and train three classification models:
 - Logistic regression
 - Support Vector Machine (SVM) with a Radial Basis Function (RBF) kernel
 - Random forest
The ROC curves corresponding to the training an test results of these three models are shown next. The performance '''+
'''of a random model is added for reference.''')
app.place(md16)

# Fit primal logistic regression
log_primal = LogisticRegression()
log_primal.fit(df_train.loc[:, df_train.columns != 'exited'],df_train.exited)

# Fit SVM with RBF Kernel
SVM_RBF = SVC(kernel='rbf', probability=True)
SVM_RBF.fit(df_train.loc[:, df_train.columns != 'exited'],df_train.exited)

# Fit Random Forest classifier
RF = RandomForestClassifier(max_depth=8)
RF.fit(df_train.loc[:, df_train.columns != 'exited'],df_train.exited)

# Compute scores
def get_auc_scores(y_actual, method, method2):
    auc_score = roc_auc_score(y_actual, method)
    fpr_df, tpr_df, _ = roc_curve(y_actual, method2)
    return (auc_score, fpr_df, tpr_df)

# Define X and y
y = df_train.exited
X = df_train.loc[:, df_train.columns != 'exited']

# Get AUC Scores
auc_log_primal, fpr_log_primal, tpr_log_primal = get_auc_scores(y, log_primal.predict(X),
                                                                log_primal.predict_proba(X)[:,1])
auc_SVM_RBF, fpr_SVM_RBF, tpr_SVM_RBF = get_auc_scores(y, SVM_RBF.predict(X),SVM_RBF.predict_proba(X)[:,1])
auc_RF, fpr_RF, tpr_RF = get_auc_scores(y, RF.predict(X),RF.predict_proba(X)[:,1])

# Plot ROC curve for training data
fig6 = plt.figure(figsize = (6,3), linewidth= 1)
plt.plot(fpr_log_primal, tpr_log_primal, label = 'log primal Score: ' + str(round(auc_log_primal, 5)))
plt.plot(fpr_SVM_RBF, tpr_SVM_RBF, label = 'SVM RBF Score: ' + str(round(auc_SVM_RBF, 5)))
plt.plot(fpr_RF, tpr_RF, label = 'RF score: ' + str(round(auc_RF, 5)))
plt.plot([0,1], [0,1], 'k--', label = 'Random: 0.5')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC Curve (training data)')
plt.legend(loc='best')
img6 = app.image(fig6)
app.place(img6)


# Create dataframe for test
df_test = df_test[['exited'] + continuous_vars + cat_vars]

# One hot encode the categorical variables
lst = ["country", "gender"]
remove = list()
for i in lst:
    for j in df_test[i].unique():
        df_test[i+'_'+j] = np.where(df_test[i] == j,1,-1)
    remove.append(i)
df_test = df_test.drop(remove, axis=1)

# Ensure that all one hot encoded variables that appear in the train data appear in the subsequent data
L = list(set(df_train.columns) - set(df_test.columns))
for l in L:
    df_test[str(l)] = -1

# MinMax scaling continuous variables based on min and max from the train data
df_test[continuous_vars] = (df_test[continuous_vars]-minVec)/(maxVec-minVec)
# Ensure that variables are ordered in the same way as was ordered in the train set
df_test = df_test[df_train.columns]

# Compute AUCs for test data
auc_log_primal_test, fpr_log_primal_test, tpr_log_primal_test = get_auc_scores(
    df_test.exited,log_primal.predict(df_test.loc[:, df_test.columns != 'exited']),
                                                       log_primal.predict_proba(
                                                           df_test.loc[:, df_test.columns != 'exited'])[:,1])
auc_SVM_RBF_test, fpr_SVM_RBF_test, tpr_SVM_RBF_test = get_auc_scores(
    df_test.exited, SVM_RBF.predict(df_test.loc[:, df_test.columns != 'exited']),
                                                       SVM_RBF.predict_proba(
                                                           df_test.loc[:, df_test.columns != 'exited'])[:,1])
auc_RF_test, fpr_RF_test, tpr_RF_test = get_auc_scores(df_test.exited, RF.predict(
        df_test.loc[:, df_test.columns != 'exited']),RF.predict_proba(df_test.loc[:, df_test.columns != 'exited'])[:,1])

# Plot ROC curve for test data
fig7 = plt.figure(figsize = (6,3), linewidth= 1)
plt.plot(fpr_log_primal_test, tpr_log_primal_test, label = 'log Primal score: ' + str(round(auc_log_primal_test, 5)))
plt.plot(fpr_SVM_RBF_test, tpr_SVM_RBF_test, label = 'SVM RBF score: ' + str(round(auc_SVM_RBF_test, 5)))
plt.plot(fpr_RF_test, tpr_RF_test, label = 'RF score: ' + str(round(auc_RF_test, 5)))
plt.plot([0,1], [0,1], 'k--', label = 'Random: 0.5')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC Curve (test data)')
plt.legend(loc='best')
img7 = app.image(fig7)
app.place(img7)

# Add markdown
md7 = app.markdown('''As already mentioned, the main aim is to predict the customers that will possibly churn so '''+
'''they can be put in some sort of scheme to prevent churn. In this case, recall results (correct guesses over the '''+
''' actual number of churning customers) are more important than other metrics, like the overall accuracy score '''+
'''of the model.\n Here the objective is to obtain the highest possible recall while trying to maintain a high '''+
'''precision so that the bank can focus its resources effectively towards clients highlighted by the model without '''+
'''wasting too much resources on the false positives.\n From the review of the fitted models above, the best model ''' +
'''is the random forest. One can choose different points in the ROC curve to find a tradeoff between True Positive '''+
'''Rate (TPR) or Recall, and the False Positive Rate (FPR or probability of false alarm). '''+
'''The choice of a point in the ROC curve should be based on the resources that the bank can provide to '''+
'''address the churning problem: if many resources can be allocated, the bank could allow itself to make many wrong '''+
'''guesses (left part of the curve) in order to greatly reduce the churn problem. However, if the bank is '''+
'''looking for a more conservative approach, then the number of customers addressed will be very low (left part '''+
'''of the curve) and so will be the reduction of churn. The model will also provide a probability of churn, which'''+
''' could also be used to priorite which customers to reach out to in order to minimize the resources needed.''')
app.place(md7)

# Compute and plot confusion matrix
pred_val = RF.predict(df_test.loc[:, df_test.columns != 'exited'])
cm = confusion_matrix(df_test.exited,pred_val)
fig8 = plt.figure(figsize=[8, 8])
norm_cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
sns.heatmap(norm_cm, annot=cm, fmt='g', xticklabels=['Predicted: No','Predicted: Yes'],
            yticklabels=['Actual: No','Actual: Yes'], cmap='bone')
img8 = app.image(fig8)
app.place(img8)

# Add markdown
md8 = app.markdown('''
The previous figure shows a confusion matrix for a very characteristic point in the ROC curve: the one that '''+
'''corresponds to a precision of 50% (half of the predicted churning customers actually do churn).'''+
'''With a precision of 50%, a recall of around 21% and a FPR of 7% is obtained. This recall tells us that the model '''+
'''is able to highlight 21% of all customers who churned. The FPR of 7% indicates that, out of all '''+
'''customers that the model thinks will not churn, around 7% actually did churn. \n

# 5. Conclusion
The performance of the model on previously unseen data is reasonably good even without putting much effort in '''+
''' feature selection or feature engineering. However, in as much as the model performs well, it still misses '''+
'''about half of those who end up churning. This could be improved by re-training the model with more data '''+
'''over time while in the meantime use the model to address customers with high-probablity of churning.''')
app.place(md8)

# Register DataApp
client.register_data_app(app)