import pandas as pd 


def type_corrector(df: pd.DataFrame) -> pd.DataFrame:
    df.collected_at = pd.to_datetime(df.collected_at, format='%Y-%m-%d %H:%M:%S.%f')  
    df['datetime_utc'] = pd.to_datetime(df['datetime_utc'], format='%Y-%m-%d %H:%M:%S%z')
    df['datetime_msc'] = pd.to_datetime(df['datetime_msc'], format='%Y-%m-%d %H:%M:%S%z')
    df['date'] = pd.to_datetime(df['date'])
    return df 


def stripper(df: pd.DataFrame) -> pd.DataFrame:
    df.text = df.text.str.strip().str.replace(r'\n+',  ' | ', regex=True)
    return df 


def sorter(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(['channel', 'datetime_utc']).reset_index(drop=True)
    return df 