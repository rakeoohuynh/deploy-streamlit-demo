import pandas as pd

def data_source(file_name):
    df=pd.read_csv('don_hang.csv')
    df['ngay_dat']= pd.to_datetime(df['ngay_dat'],format ='mixed')
    df['thanh_tien']=df['so_luong']* df['don_gia']
    return df

