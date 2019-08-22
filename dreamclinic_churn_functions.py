import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix


def clean_df(df):
    """
    Takes in a Pandas Dataframe from Dreamclinic
    and cleans it for aggregation.
    """
    # remove rows where HrsWorked = 0
    # because they are just used by the front desk staff somehow
    df = df[df['HrsWorked'] != 0]
    # fill NaN values in 'Service_Category with 'Massage'
    df['Service_Category'] = df['Service_Category'].fillna(value='Massage')
    # remove white space from Therapist names
    df['Therapist'] = df['Therapist'].str.strip()
    # make all therapist names lowercase to avoid typos in data entry
    df['Therapist'] = df['Therapist'].str.lower() 
    # find and replace nicknames with domain knowledge
    df = df.replace('abby thomson', 'abigail thomson')
    # Drop Address_City and Addres_State Columns from Dataframe
    df.drop(['Address_City', 'Address_State', 'Invoice_Category'],
                                               axis=1, 
                                               inplace=True)
    # Drop rows without a clientID
    df = df.dropna()
    return df


def groupby_time(df, offset_alias='M'):
    """
    Groupby time period: 
    'offset aliases' is just a format code.
    """
    months = df.TransactionDate.dt.to_period(offset_alias)
    g = df.groupby(months)
    return g


def unique_client_agg(groupby_obj):
    """
    Takes in the groupby obj from groupby_time()
    and aggregates it for unique clients.
    """
    # Count unique clients by month and drop/rename columns to reflect
    # new aggredated DateFrame.
    client_count_df = groupby_obj.nunique()
    return client_count_df


def sum_client_agg(groupby_obj):
    """
    Takes in the groupby obj from groupby
    and aggregates it for all clients.
    """
    # Count unique clients by month and drop/rename columns to reflect
    # new aggredated DateFrame.
    total_count_df = groupby_obj.count()
    return total_count_df


def clean_agg_df(client_count_df):
    """Cleans aggregaged df from unique_client_agg and total_client_agg."""
    client_count_df = client_count_df.drop('TransactionDate', axis=1)
    client_count_df['month'] = client_count_df.index
    client_count_df.reset_index(inplace=True)
    client_count_df["client_count"] = client_count_df['clientID']
    client_count_df.drop('clientID', axis=1, inplace=True)
    client_count_df['month'] = client_count_df['month'].astype('str')
    client_count_df.rename(columns={"clientID": "unique_client_count",
                                    "Therapist": "therapists_employed",
                                    "Zipcode": "zipcodes_reached"},
                                    inplace=True)
    client_count_df.drop(["HrsWorked"], axis=1, inplace=True)
    return client_count_df


def line_plot(df, 
                title, 
                x_label, 
                y_label, 
                x_column='TransactionDate',
                y_column='services_performed'):
    """Creates a line plot with clean aggregated dataframe"""
    x = df[x_column]
    y = df[y_column]
    fig, ax = plt.subplots(figsize=(30, 7))
    plt.title(title, fontsize=30)
    sns.lineplot(x=x,
                y=y,
                ax=ax)
    plt.xlabel(x_label, fontsize=25)
    plt.ylabel(y_label, fontsize=25)
    return plt.show()


def session_count_graph(session_count, min_sessions, max_sessions):
    fig, ax = plt.subplots()
    ax.hist(session_count,
            bins=max_sessions,
            range=(min_sessions,
            max_sessions + 1))
    plt.ylabel('# of clients')
    plt.xlabel('# of sessions they get over their lifetime as a client')
    plt.title('Amount of clients that get X number of Session')
    plt.xticks(ticks=(range(min_sessions, (max_sessions + 1))))
    return plt.show


def temporal_split(df,
                    start_year=2019,
                    start_month=6,
                    start_day=1,
                    end_year=2019,
                    end_month=8,
                    end_day=1):
    """
    Starts with client_df, 
    returns DataFrame of clients labeled churn or not.
    """
    #cuts the data temporally 
    # to the last 2 months so that we can label the data for modeling
    start = df['Date'].searchsorted(dt.datetime(start_year,
                                                start_month,
                                                start_day))
    end = df['Date'].searchsorted(dt.datetime(end_year,
                                                end_month,
                                                end_day))
    #DataFrame used as labeling data
    not_churn_df = df.iloc[start:end]
    not_churn_df['churn'] = False
    labeling_df = pd.DataFrame(not_churn_df['clientID'].unique())
    labeling_df['churn'] = False
    labeling_df = labeling_df.rename({0 : 'clientID'},axis=1)
    churn_df = df.merge(labeling_df,
                               how='left',
                               on='clientID')
    churn_df['churn'] = churn_df['churn'].fillna(value=True)
    return churn_df


def session_count(df):
    """Take in client_df and outputs a session count df and session count groupby
    object."""
    session_count = df.groupby('clientID').nunique()['TransactionDate']
    session_count_df = pd.DataFrame([session_count]).T
    session_count_df['#_of_sessions_had'] = session_count_df.replace()
    session_count_df = session_count_df.drop('TransactionDate', axis=1)
    return session_count_df, session_count



def temporal_split_test(churn_df,
                        start_year=2018, 
                        start_month=12, 
                        start_day=1, 
                        end_year=2019, 
                        end_month=5, 
                        end_day=31):
    """Needs churn_df, outputs temporal test_df for train_test_split"""
    start = churn_df['Date'].searchsorted(dt.datetime(start_year,
                                                        start_month,
                                                        start_day))
    end = churn_df['Date'].searchsorted(dt.datetime(end_year,
                                                        end_month,
                                                        end_day))
    test_df = churn_df.iloc[start:end]
    return test_df


def temporal_split_train(churn_df, 
                         end_year=2018, 
                         end_month=11, 
                         end_day=30):
    #Temporal train split
    end = churn_df['Date'].searchsorted(dt.datetime(end_year, 
                                                    end_month, 
                                                    end_day))
    train_df = churn_df.iloc[:end]
    return train_df


def aggregate(df, unique_col='clientID'):
    """
    Aggregates the train and test Dataframes 
    with the features for modeling.
    """
    count_train_df = df.groupby('clientID').nunique()
    # counts how many times everything happens
    summed_df = df.groupby(unique_col).sum()
    # Total session count
    summed_df['total_sessions'] = count_train_df['Date']
    # Average session length calc
    summed_df['average_session_length'] = summed_df['HrsWorked']/summed_df['total_sessions']
    # turns zipcodes into bool
    return summed_df


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
#     classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax