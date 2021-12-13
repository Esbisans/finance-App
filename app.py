import streamlit as st
import pandas as pd
import yfinance as yf
import time
import logging
import threading
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from streamlit.report_thread import add_report_ctx



logging.basicConfig(
    level=logging.DEBUG,
    format='%(threadName)s %(message)s'
)


def search():

    def relativeret(df):
        rel = df.pct_change()
        cumret = (1+rel).cumprod() - 1
        cumret = cumret.fillna(0)
        return cumret

    if len(dropdown) > 0:
        df = relativeret(yf.download(dropdown, start, end)['Adj Close'])
        st.header('Resultados de {}'.format(dropdown))
        st.line_chart(df)


df = dict()

def buscar(elemento, event):

        global df

        def relativeret(df):
            rel = df.pct_change()
            cumret = (1+rel).cumprod() - 1
            cumret = cumret.fillna(0)
            return cumret

        df = relativeret(yf.download(elemento, start, end)['Adj Close'])
        event.set()
        return df


if __name__ == '__main__':
    event = threading.Event()

    #search()

    with ThreadPoolExecutor(max_workers=4, thread_name_prefix='hilo') as executor:

        st.title('Tablero de finanzas ')

        tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'GOOG', 'AMD', 'INTC', 'SONY')
        dropdown = st.multiselect('Selecciona la opción', tickers)

        start = st.date_input('Fecha de inicio', value = pd.to_datetime('2021-01-01'))
        end = st.date_input('Fecha de fin', value = pd.to_datetime('today'))

        if st.button('Buscar'):
                #futuros = [ executor.submit(buscar, url, event) for url in dropdown]
            
            for drop in dropdown:

                executor.submit(buscar, drop, event)
                

                event.wait()
                st.header('Resultados de {}'.format(drop))
                event.clear()
                st.line_chart(df)
            if len(dropdown) > 1:    
                search()



            



