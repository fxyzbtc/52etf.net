import streamlit as st
import pandas as pd
import numpy as np
import os

def app():
    @st.cache(ttl=1*60)
    def load_csv():
        with open("data/etf.csv", encoding="utf8") as fp:
            return pd.read_csv(fp)

    etf = load_csv()
  
    cols_left = ['ticker', 'name', 'indexName', 'indexTicker', 'assetalNet', \
            'navChange1y', 'navAnnualReturns2y', 'navAnnualReturns5y', 'navAnnualReturns10y', \
            'manageName', 'organizationformName']
    cols_right = set(etf.columns)-set(cols_left)
    columns = cols_left + list(cols_right)

    option = st.multiselect(
            '输入指数名称或下拉选择',
            etf['indexName'].unique(),
        )

    search = st.text_input('输入基金名称或代码')
    search_text = search.title()

    st.markdown("#### 查询结果")
    with st.empty():
        if len(search_text):

            index_ticker_bool = etf['indexTicker'].astype(str).str.contains(search_text)
            index_name_bool = etf['indexName'].str.contains(search_text)
            ticker_bool = etf['ticker'].astype(str).str.contains(search_text)
            name_bool = etf['name'].str.contains(search_text)        
            result = etf[ticker_bool | name_bool | index_ticker_bool | index_name_bool]
            result = result.drop_duplicates().sort_values(by=['assetalNet'], ascending=False)
            st.write(result[columns])

        if option:
            st.empty()
            result = etf[etf['indexName'].isin(option)].sort_values(by=['assetalNet'], \
                ascending=False)
            st.write(result[columns])

