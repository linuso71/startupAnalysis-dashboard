import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors = 'coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

st.set_page_config(layout='wide',page_title='StartUp Analysis')

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())


    # Max amount infused in a startup
    max_startup_name = df.groupby('startup')['amount'].sum().sort_values(ascending = False).head(1).index[0]
    max_funding = round(df.groupby('startup')['amount'].sum().sort_values(ascending = False).head(1).values[0])

    # average ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()

    # total funded startup
    num_startup =df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')

    with col2:
        st.metric('Max' + '(' + max_startup_name + ')',str(max_funding)+'Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding))+'Cr')

    with col4:
        st.metric('Funded Startup',num_startup)

    selected_option = st.selectbox('Select Type',['Total','Count'])
    st.header('MoM Graph')
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig2, ax2 = plt.subplots()
    ax2.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig2)

def load_investor_details(investor):
    st.title(investor)
    # load recent 5 investments of the investor
    last_5df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)


    col1,col2 = st.columns(2)
    with col1:
        #   biggest investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()
        st.header('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        # vertical investment
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.header('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct = '%0.01f%%')
        st.pyplot(fig1)

    col3,col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.header('Rounds Invested In')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.01f%%')
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.header('City Invested In')
        fig3,ax3 = plt.subplots()
        ax3.pie(city_series,labels = city_series.index,autopct = '%0.01f%%')
        st.pyplot(fig3)


    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.header('YoY investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index,year_series.values)
    st.pyplot(fig4)



st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Detail')
    st.title('StartUp')
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Detail')
    if btn2:
        load_investor_details(selected_investor)
