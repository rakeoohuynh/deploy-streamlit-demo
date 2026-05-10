import pandas as pd

def data_source(file_name):
    df = pd.read_csv('don_hang.csv', index_col=False)
    # Drop any leftover index columns saved by previous to_csv() calls
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['ngay_dat'] = pd.to_datetime(df['ngay_dat'], format='mixed')
    df['thanh_tien'] = df['so_luong'] * df['don_gia']
    return df

