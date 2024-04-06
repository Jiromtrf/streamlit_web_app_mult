import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 銘柄のリスト
tickers = {
    'apple': 'AAPL',
    'facebook': 'META',
    'google': 'GOOGL',
    'microsoft': 'MSFT',
    'netflix': 'NFLX',
    'amazon': 'AMZN',
    'mandom': '4917.T',
    'TOYOTA': '7203.T',
}

st.title('株価可視化アプリ')

# 日数の選択
days = st.sidebar.slider('日数', 1, 365, 60)

# 株価範囲の指定
price_range = st.sidebar.slider('株価の範囲指定', 100.0, 2000.0, (120.0, 200.0))

# ティッカーの複数選択
selected_tickers = st.multiselect('ティッカーを選択してください', list(tickers.keys()), ['apple'])

@st.cache_data
def get_data(ticker, days=20):
    tkr = yf.Ticker(tickers[ticker])
    hist = tkr.history(period=f'{days}d')
    return hist

# 色のリストを定義（必要に応じて拡張可能）
colors = {
    'apple': '#1f77b4',  # 青
    'facebook': '#ff7f0e',  # オレンジ
    'google': '#2ca02c',  # 緑
    'microsoft': '#d62728',  # 赤
    'netflix': '#9467bd',  # 紫
    'amazon': '#8c564b',  # 茶
    'mandom': '#e377c2',  # ピンク
    'TOYOTA': '#7f7f7f',  # グレー
}

fig = go.Figure()

# 選択されたティッカーごとにチャートを重ねて追加
for ticker in selected_tickers:
    df = get_data(ticker, days)
    color = colors.get(ticker, '#000000')  # ティッカーに対応する色を取得、デフォルトは黒
    
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'],
                                 increasing_line_color=color, decreasing_line_color=color,
                                 name=ticker))  # ティッカー名を追加

# レイアウトの設定
fig.update_layout(
    yaxis_range=[price_range[0], price_range[1]],
    xaxis=dict(
        rangeslider=dict(
            visible=False
        )
    )
)

st.plotly_chart(fig, use_container_width=True)


