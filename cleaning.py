import streamlit as st
import pandas as pd


@st.cache
def clean(data, columns, wanted_columns, dtypes=None):
    # checking if the number of types is equal to the columns
    if len(wanted_columns) != len(dtypes):
        return 0

    # change to dataframe
    df = pd.DataFrame(data)

    # passing column
    df.columns = columns

    # drop unnecessary columns

    for col in columns:
        if col not in wanted_columns:
            df = df.drop(col, axis=1)

    if dtypes is not None:
        # data types conversion
        columns = df.columns.values.tolist()
        for i in range(len(columns)):
            if dtypes[i] == "num":
                df[columns[i]] = df[columns[i]].apply(pd.to_numeric)
            elif dtypes[i] == "time":
                df[columns[i]] = pd.to_datetime(df[columns[i]] / 1000, unit='s')

    return df


