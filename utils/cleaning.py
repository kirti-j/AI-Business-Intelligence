import pandas as pd


def convert_date_columns(df):
        for col in df.columns:
            try:
                if "date" in col.lower():
                    df[col]=pd.to_datetime(df[col],errors="coerce")
            except Exception:
                pass
        return df

def clean_data(df):
    df=df.copy()
    #Missing values
    missing_before=df.isnull().sum().sum()

    original_rows=len(df)
    original_columns=len(df.columns)

    

    #Filling numeric columns
    numeric_cols=df.select_dtypes(include=['number']).columns

    for col in numeric_cols:
         median_value = df[col].median()
         df[col] = df[col].fillna(median_value)

         

    #Filling categorical columns
    categorical_cols=df.select_dtypes(include=['object']).columns

    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")

    #Date conversion
    df = convert_date_columns(df)


    missing_after=df.isnull().sum().sum()

    #Removing duplicates
    before_rows=len(df)
    df.drop_duplicates(inplace=True)
    after_rows=len(df)
    duplicates_removed=before_rows-after_rows

    

    #Return results
    return (df,missing_before,missing_after,duplicates_removed)