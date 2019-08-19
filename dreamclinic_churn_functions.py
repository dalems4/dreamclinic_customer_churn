import matplotlib.pyplot as plt
import seaborn as sns


def clean_df(df):
    """Takes in a Pandas Dataframe from Dreamclinic
    and cleans it for aggregation"""
    # remove rows where HrsWorked = 0
    # because they are just used by the front desk staff somehow
    df = df[df['HrsWorked'] != 0]
    # fill NaN values in 'Service_Category with 'Massage'
    df['Service_Catagory'] = df['Service_Category'].fillna(value='Massage')
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
    df = df.dropna(subset=['clientID'])
    return df


def groupby_time(df, offset_alias='M'):
    """Groupby time period: 'offset aliases'. '"""
    months = df.TransactionDate.dt.to_period(offset_alias)
    g = df.groupby(months)
    return g


def unique_client_agg(groupby_obj):
    """Takes in the groupby obj from groupby
       and aggregates it for unique clients."""
    # Count unique clients by month and drop/rename columns to reflect
    # new aggredated DateFrame.
    client_count_df = groupby_obj.nunique()
    return client_count_df


def sum_client_agg(groupby_obj):
    """Takes in the groupby obj from groupby
       and aggregates it for all clients."""
    # Count unique clients by month and drop/rename columns to reflect
    # new aggredated DateFrame.
    total_count_df = groupby_obj.count()
    return total_count_df


def clean_agg_df(client_count_df):
    """Cleans aggregaged df from unique_client_agg and total_client_agg."""
    client_count_df.drop('TransactionDate', axis=1, inplace=True)
    date_column = client_count_df['TransactionDate']
    client_count_df.reset_index(inplace=True)
    client_count_df["client_count"] = client_count_df['clientID']
    client_count_df.drop('clientID', axis=1, inplace=True)
    date_column = date_column.astype('str')
    client_count_df.rename(columns={"clientID": "unique_client_count",
                                    "Therapist": "therapists_employed",
                                    "Zipcode": "zipcodes_reached"},
                                    inplace=True)
    client_count_df.drop(["HrsWorked"], axis=1, inplace=True)
    client_count_df.drop(['Service_Category'], axis=1,  inplace=True)
    return client_count_df


def line_plot(df, title, x_label, y_label, x_column='TransactionDate',
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
