import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt 
from datetime import datetime
import pandas as pd 
import numpy as np 

# API 호출을 위한 라이브러리 임포트 
import requests

# 프로펫 라이브러리 임포트
from fbprophet import Prophet

def main() :
    st.header('Online Stock Price Ticker')

    # yfiance 실행 

    symbol = st.text_input('심볼 입력 : ')
    # symbol = 'AAPL' # 애플, 'MSFT' 마이크로소프트

    data = yf.Ticker(symbol)

    today = datetime.now().date().isoformat()

    df = data.history( start = '2010-06-01', end = today )

    st.dataframe(df)

    st.subheader('종가')
    st.line_chart(df['Close'])

    st.subheader('거래량')
    st.line_chart(df['Volume'])

    # yfinance # 라이브러리만의 정보 
    # data.info # 회사정보 다나와
    # data.calendar # 주식정보 데이터프레임
    # data.major_holders # 대주주들 
    # data.institutional_holders   # 은행정보
    # data.recommendations # 어느기관이 삿냐 추천했는지
    # data.dividends # 배당정보, 각날짜별로 배당이 얼마인지
    div_df = data.dividends 
    st.dataframe( div_df.resample('Y').sum() ) # 년도별로 데이터 총합 

    new_df = div_df.reset_index() 
    new_df['Year'] = new_df['Date'].dt.year # 날짜를 컬ㄹ럼으로 올린다 

    st.dataframe(new_df)

    fig = plt.figure() 
    plt.bar(new_df['Year'], new_df['Dividends'])
    st.pyplot(fig)


    # 여러 주식 데이터를 한번에 보여주기.
    favorites = ['msft', 'tsla', 'nvda', 'aapl', 'amzn']
    f_df = pd.DataFrame()

    for stock in favorites : 
        f_df[stock] = yf.Ticker(stock).history(start= '2010-01-01', end= today)['Close']

    st.dataframe(f_df)
    st.line_chart(f_df)
    # 멀티셀렉트 응용해서 하는것도 굿 


    # 스탁트윗의 API를 호출
    res = requests.get('https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(symbol))

    # JSON 형식이므로, .json() 이용
    res_data = res.json() 

    # 파이썬의 딕셔너리와 리스트의 조합으로 사용가능 
    st.write(res_data) # 전체데이터

    # 필요한건 messages, 파싱 원하는데이터 찾아서 표시하는방법
    for message in res_data['messages'] :
        col1, col2 = st.beta_columns( [1, 4] ) # 비율을 정할 수 있다. 1:4 비율로 컬럼잡아달라 
        
        with col1 :
            st.image( message['user']['avatar_url'] )

        with col2 :
            st.write( '유저 이름 : ' + message['user']['username'] )
            st.write( '트윗 내용 : ' + message['body'] )
            st.write( '올린 시간 : ' + message['created_at'] )
            st.markdown('---')

    p_df = df.reset_index()
    p_df.rename(columns = {'Date' : 'ds', 'Close' : 'y'}, inplace = True)

    st.dataframe(p_df) # 잘바뀌었는지 확인

    # 에측가능!
    # m = Prophet()
    # m.fit(p_df)

    # future = m.make_future_dataframe(periods= 365)
    # forecast = m.predict(future)

    # # st.dataframe(forecast)

    # fig1 = m.plot(forecast)
    # st.pyplot(fig1)

    # fig2 = m.plot_components(forecast)
    # st.pyplot(fig2)




if __name__ == '__main__' :
    main() 
