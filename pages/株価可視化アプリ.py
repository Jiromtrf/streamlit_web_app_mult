import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 銘柄のリスト
tickers = {
    'マンダム': '4917.T',
    '花王': '4452.T',
    'コーセー': '4922.T',
    '資生堂': '4911.T',
    'ライオン': '4912.T',
    '小林製薬': '4967.T',
    'ポーラHD': '4927.T',
    'ユニ・チャーム': '8113.T',
}

st.title('株価可視化アプリ')

# グラフの前に案内テキストを追加
st.write("""
### ローソク足の説明
- **青色**のローソク: **陽線**
- **赤色**のローソク: **陰線**
""")

image_path = "色の説明.png"

# 画像を表示
st.image(image_path, caption='例：マンダムのローソク足')

@st.cache_data
def get_data(ticker_symbol, days=20):
    tkr = yf.Ticker(ticker_symbol)
    hist = tkr.history(period=f'{days}d')
    return hist

# 日数の選択
days = st.sidebar.slider('日数', 1, 365, 60)

# ティッカーの複数選択
selected_tickers = st.multiselect('ティッカーを選択してください', options=list(tickers.keys()), default=['マンダム'])

# 選択された銘柄の株価データを取得し、最高値と最低値を計算
highest_prices = []
lowest_prices = []
for ticker_name in selected_tickers:
    ticker_symbol = tickers[ticker_name]  # 辞書からティッカーシンボルを取得
    df = get_data(ticker_symbol, days)
    highest_prices.append(df['High'].max())
    lowest_prices.append(df['Low'].min())

# 最高値と最低値
highest_price = max(highest_prices) if highest_prices else 2000
lowest_price = min(lowest_prices) if lowest_prices else 1000

# スライダーバーによる価格範囲の選択
price_range = st.sidebar.slider(
    label="株価の選択範囲",
    min_value=int(lowest_price - 100),  # 安値の少し下
    max_value=int(highest_price + 100),  # 高値の少し上
    value=(int(lowest_price), int(highest_price))
)




# 色のリストを定義（必要に応じて拡張可能）
colors = {
    'マンダム': {'increasing': '#1f77b4', 'decreasing': '#d62728'},  # 青と赤
    '花王': {'increasing': '#ff7f0e', 'decreasing': '#9467bd'},  # オレンジと紫
    'コーセー': {'increasing': '#2ca02c', 'decreasing': '#7f7f7f'},  # 緑とグレー
    '資生堂': {'increasing': '#17becf', 'decreasing': '#1f77b4'},  # シアンと青
    'ライオン': {'increasing': '#e377c2', 'decreasing': '#f7b6d2'},  # ピンクとライトピンク
    '小林製薬': {'increasing': '#7f7f7f', 'decreasing': '#c7c7c7'},  # グレーとライトグレー
    'ポーラHD': {'increasing': '#bcbd22', 'decreasing': '#dbdb8d'},  # オリーブグリーンとライトオリーブグリーン
    'ユニ・チャーム': {'increasing': '#8c564b', 'decreasing': '#c49c94'},  # 茶色とライトブラウン
}

fig = go.Figure()

# 選択されたティッカーごとにチャートを重ねて追加
for ticker_name in selected_tickers:
    ticker_symbol = tickers[ticker_name]
    df = get_data(ticker_symbol, days)
    color_set = colors.get(ticker_name, {'increasing': '#2ca02c', 'decreasing': '#d62728'})  # デフォルトの色
    
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'],
                                 increasing=dict(line=dict(color=color_set['increasing'])),
                                 decreasing=dict(line=dict(color=color_set['decreasing'])),
                                 name=ticker_name))
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


