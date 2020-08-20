import pandas as pd


def change_dataframe_nans_to_none(df):
    df = df.where(pd.notnull(df), None)
    return df
