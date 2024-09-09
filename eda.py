import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv('Amazon 2_Raw.csv')

with st.expander('View the data cleaning process'):
    st.write('Since this data is obtained Secandarity, cleaning will be the go to prerequisist. I started by looking if there are missing values from the data')
    st.write(df.isnull().sum())
    st.write('As from the data frame above we can see that all the respective columns do not have any missing values.')
    st.write('Next, I checked if there are duplicated entries.')
    st.write(df.duplicated().sum())
    st.write('There are no duplicated entires as seen above')
with st.expander('Let us Explore some the sales data'):
    st.write('checking out the number of different Products')
    st.write(df['Product Name'].nunique())
    st.write('checking out total number of categories')
    st.write(df['Category'].nunique())
    st.write('There are 17 distinct categories of goods and 1494 different products')
    df['Order Date']=pd.to_datetime(df['Order Date'])
    startdate=pd.to_datetime(df['Order Date'].min())
    enddate=pd.to_datetime(df['Order Date'].max())   
    st.write('I can Imagine if the company needs to know the sales and profit  made in different period(Maybe this year,month, or this week), it is important to filter the data with time to be able to see the KPI with respect to time') 
    st.write('Since the products are in different Category, It would be important the campany see the variation of sales in the respective Categories')
    
    col1,col2=st.columns((2))
    with col1:
        date1=pd.to_datetime(st.date_input('From',startdate))
    with col2:
        date2=pd.to_datetime(st.date_input('To',enddate))
    filtered_df=df[(df['Order Date']>=date1)&(df['Order Date']<=date2)].copy()
    filtered_df1=st.sidebar.multiselect('Select your Category',filtered_df['Category'].unique())
    if not filtered_df1:
        filtered_df1=filtered_df.copy()
    else:
        filtered_df1=filtered_df[filtered_df['Category'].isin(filtered_df1)]
    col11,col12=st.columns((2))
    with col11:
        st.write('total sales')
        st.write(filtered_df1['Sales'].sum())
    with col12:
        st.write('total Profit')
        st.write(filtered_df1['Profit'].sum())
    data1=filtered_df1.groupby('Category')['Sales'].sum().sort_values(ascending=True).reset_index()
    st.write(data1)
    fig2=px.bar(data1,x='Category',y='Sales',title='bar chart to compare sales in different categories')
    st.write(fig2)
    filtered_df1.sort_values(by='Order Date',inplace=True)
    fig3=px.line(filtered_df1,x='Order Date',y=['Sales','Profit'],title='combined Line Graph For sales, profit and Date')
    st.write(fig3)
    filtered_df1["Order Date"]= pd.to_datetime(filtered_df1["Order Date"])
    filtered_df1["Month"]= filtered_df1["Order Date"].dt.month
    filtered_df1["Day of week"]= filtered_df1["Order Date"].dt.dayofweek
    filtered_df1["Day Of Year"]= filtered_df1["Order Date"].dt.dayofyear
    filtered_df1["Yearly Quarters"]= filtered_df1["Order Date"].dt.quarter
    fig4=px.bar(filtered_df1,x='Month',y='Sales',title='bar graph for month and respective total sales')
    st.write(fig4)
    fig5=px.bar(filtered_df1,x='Day of week',y='Sales',title='bar graph for Day of week and respective total sales')
    st.write(fig5)
    fig6=px.bar(filtered_df1,x='Day Of Year',y='Sales',title='bar graph for Day Of Year and respective total sales')
    st.write(fig6)
    fig7=px.bar(filtered_df1,x='Yearly Quarters',y='Sales',title='bar graph for Yearly Quarters and respective total sales')
    st.write(fig7)