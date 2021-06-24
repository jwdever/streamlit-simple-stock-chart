import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

st.title('Stock Price Chart')

#ticker input
symb = st.text_input("Ticker Symbol").upper()
button_clicked = st.button("GO")


#date selector
page = st.sidebar.selectbox("Date Range", ['Past 7 Days', 'Past 30 Days', 'Past 100 Days'], index=1)
if page == 'Past 7 Days':
    num=7
elif page == 'Past 30 Days':
    num=30
elif page == 'Past 100 Days':
    num=100

#control flow    
if not button_clicked:
    st.warning('Please input a valid ticker symbol.')
    st.stop()



def main():
    # get price data for ticker
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s'%(symb,get_api())
    r = requests.get(url)
    data = dict(r.json())
    data_high={}
    
    
    #exception handling in case ticker symbol is not valid
    try:
        for x in data['Time Series (Daily)']:
            data_high[x]=float(data['Time Series (Daily)'][x]['2. high'])
    except KeyError:
        st.warning('Invalid symbol. Please enter a valid ticker symbol, and try again.')
        st.stop()
    else:
        pass
        
    #format data
    df_high=pd.Series(data_high)
    df_high.index= pd.to_datetime(df_high.index)
    df_high=df_high.reset_index()
    df_high.columns=['Day', 'Closing Price (USD)']
    df_high=df_high[:num]
    
    #plot
    fig = px.line(df_high, x='Day', y='Closing Price (USD)')
    fig.update_layout(
        title="Closing Price for %s, Past %d Trading Days"%(symb, num),
        xaxis_title="Day",
        yaxis_title="Closing Price (USD)",
        font=dict(
           family='Courier',
           color="Black"
        )
    )
    st.plotly_chart(fig)

@st.cache
#API
def get_api():
    API_KEY = os.getenv('MY_API_KEY')
    return API_KEY


if __name__ == '__main__':
    main()