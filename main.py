import pandas as pd
from helper import *
import streamlit as st
from datetime import datetime, date
import matplotlib.pyplot as plt

st.set_page_config(page_title='Web bán hàng',layout='wide')
st.title('Quản lý bán hàng',text_alignment='center')

file_name = 'don_hang.csv'
df=data_source(file_name)

menu=st.sidebar.selectbox('Menu',['Trang chủ','Danh sách','Thêm hàng','Sửa xóa','Thống kê'])
if menu == 'Trang chủ':
    st.header('Day la trang chu')
    so_don= len(df)
    st.metric('Tong don',so_don,border = True)
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        so_don_huy =  len(df[df['trang_thai']=='Huy'])
        st.metric('So don huy',so_don_huy, border = True)
    with col2:
        so_don_da_giao = len(df[df['trang_thai']=='Da giao'])
        st.metric('So don dang giao',so_don_da_giao, border=True)
    with col3:
        so_don_dang_giao = len(df[df['trang_thai']=='Dang giao'])
        st.metric('So don da huy',so_don_dang_giao,border= True)
    with col4:
        so_don_cho_xu_ly = len(df[df['trang_thai']=='Cho xu ly'])
        st.metric('So don cho xu ly',so_don_cho_xu_ly, border= True)
    doanh_thu_da_giao = df[df['trang_thai']=='Da giao']['thanh_tien'].sum()
    st.metric('Doang thu da giao',format(doanh_thu_da_giao,','),border= True)
elif menu == 'Danh sách':
    st.header('Xem dang sach hang hoa theo trang thai')
    st.subheader('Tất cả dữ liệu')
    st.dataframe(df)
    st.subheader('Dữ liệu sau khi lọc')
    loc_trang_thai = st.selectbox('Danh sach trang thai',list(df['trang_thai'].unique()))
    loc_sp = st.selectbox('Danh sach san pham',list(df['san_pham'].unique()))
    loc_khach_hang = st.selectbox('Danh sach khach hang',list(df['khach_hang'].unique()))
    st.dataframe(df[(df['trang_thai']==loc_trang_thai)
                    & (df['san_pham']== loc_sp)
                    & (df['khach_hang']==loc_khach_hang)])
    df_download = df[(df['trang_thai']==loc_trang_thai)
                    & (df['san_pham']== loc_sp)
                    & (df['khach_hang']==loc_khach_hang)]
    if len(df_download) == 0:
        st.error('No data available to download')
    st.download_button('Download',
                       data=df_download.to_csv(index=False),
                       file_name='Danh_sach_KH.csv',
                       mime='text/csv',
                       disabled=len(df_download) == 0)
elif menu == 'Thêm hàng':
    st.header('Them hang moi')
    with st.form('Form nhap hang'):
        # Generate ma_don based on max existing ID, not dataframe length
        existing_ids = pd.to_numeric(df['ma_don'].str.replace('DH', ''), errors='coerce')
        next_id = int(existing_ids.max()) + 1 if len(existing_ids) > 0 else 1
        ma_don = 'DH' + str(next_id).zfill(3)
        khach_hang = st.text_input('Nhap ten khach hang')
        sp = st.selectbox('Chon san pham',list(df['san_pham'].unique()))
        so_luong = st.number_input('Dien so luong',value = 0, min_value= 0, max_value=100,step=1)
        don_gia = df[df['san_pham']==sp]['don_gia'].iloc[0]
        trang_thai = st.selectbox('Chon trang thai',list(df['trang_thai'].unique()))
        ngay_dat = st.date_input('Chon ngay',min_value=date(2026,1,1),max_value=datetime.today())
        thanh_tien = so_luong * don_gia
        submit = st.form_submit_button('Them hang')
        if submit:
            if not khach_hang:
                st.error('Ten KH khong de trong')
            else:
                ds_hang_moi = {
                    'ma_don': ma_don,
                    'khach_hang': khach_hang,
                    'san_pham': sp,
                    'so_luong': so_luong,
                    'don_gia': don_gia,
                    'trang_thai': trang_thai,
                    'ngay_dat': ngay_dat,
                    'thanh_tien': thanh_tien
                }
                dong_moi = pd.DataFrame([ds_hang_moi])
                df_moi = pd.concat([df, dong_moi], ignore_index=True)
                df_moi.to_csv('don_hang.csv')
                st.success('Them hang thanh cong')
                # st.rerun()
elif menu =='Sửa xóa':
    st.header('Sua va xoa don hang')
    
    # Delete Section
    st.subheader('Xoa don hang')
    with st.form('Xoa hang theo don'):
        ma_don_del = st.selectbox('Chon don can xoa', list(df['ma_don'].unique()))
        submit_del = st.form_submit_button('Xoa hang')
        if submit_del:
            df = df[df['ma_don'] != ma_don_del]
            df.to_csv(file_name, index=False)
            st.success('Da xoa hang thanh cong')
            st.rerun()

    # Edit Section
    st.subheader('Sua don hang')
    selected_id = st.selectbox('Chon don can sua', list(df['ma_don'].unique()))
    selected_row = df.loc[df['ma_don'] == selected_id].iloc[0]

    with st.form('Sua hang theo don'):
        khach_hang = st.text_input('Nhap ten khach hang', value=selected_row['khach_hang'])
        
        # San pham selection
        san_pham_options = list(df['san_pham'].unique())
        sp_index = san_pham_options.index(selected_row['san_pham']) if selected_row['san_pham'] in san_pham_options else 0
        sp = st.selectbox('Chon san pham', san_pham_options, index=sp_index)
        
        so_luong = st.number_input('Dien so luong', value=int(selected_row['so_luong']), min_value=1, max_value=100, step=1)
        don_gia = st.number_input('Don gia', value=float(selected_row['don_gia']), min_value=0.0, step=1000.0)
        
        # Status selection
        trang_thai_options = list(df['trang_thai'].unique())
        tt_index = trang_thai_options.index(selected_row['trang_thai']) if selected_row['trang_thai'] in trang_thai_options else 0
        trang_thai = st.selectbox('Chon trang thai', trang_thai_options, index=tt_index)
        
        # Fix: Allowed min_value to be earlier to avoid the API Exception
        current_date = pd.to_datetime(selected_row['ngay_dat']).date()
        ngay_dat = st.date_input('Chon ngay', value=current_date, min_value=date(2020,1,1), max_value=date(2026,12,31))
        
        thanh_tien = so_luong * don_gia
        
        # Essential Submit Button
        button_submit = st.form_submit_button('Luu thay doi')
        
        if button_submit:
    # Convert the date object to a pandas datetime object
            ngay_dat_converted = pd.to_datetime(ngay_dat)
            
            # Update the row
            df.loc[df['ma_don'] == selected_id, 
                ['khach_hang', 'san_pham', 'so_luong', 'don_gia', 'trang_thai', 'ngay_dat', 'thanh_tien']
            ] = [khach_hang, sp, so_luong, don_gia, trang_thai, ngay_dat_converted, thanh_tien]
            
            # Save to CSV
            df.to_csv(file_name, index=False)
            st.success('Cap nhat don hang thanh cong')
elif menu == 'Thống kê':
    with st.container(border =True):
        st.subheader('Top 5 san pham co doanh thu cao')
        df_top5 =df.groupby('san_pham')['thanh_tien'].sum().reset_index().sort_values(by='thanh_tien').head()
        fig,ax = plt.subplots(figsize = (8,4))
        ax.barh(df_top5['san_pham'],df_top5['thanh_tien'])
        st.pyplot(fig)
    with st.container(border =True):
        st.subheader('Ti le don hang')
        df_trang_thai =df.groupby('trang_thai')['ma_don'].count().reset_index()
        fig,ax = plt.subplots(figsize = (6,4))
        ax.pie(df_trang_thai['ma_don'],labels=df_trang_thai['trang_thai'],autopct='%1.1f%%')
        st.pyplot(fig)
    new_df_2= st.file_uploader('Upload file csv',type='csv')

    