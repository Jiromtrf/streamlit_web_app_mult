import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
import pandas as pd

st.title('天気アプリ')
st.write("調べたい地域を選んでください")


city_code_list = {
    "大阪" : "270000",
    "徳島" : "360010",
}

city_code_index = "大阪"
city_code_index = st.selectbox('地域を選んでください',city_code_list.keys())

city_code = city_code_list[city_code_index]
current_city_code = st.empty()
current_city_code.write("選択中の地域:" + city_code_index)

url = "https://weather.tsukumijima.net/api/forecast/city/" + city_code

response = requests.get(url)

weather_json = response.json()

JST = timezone(timedelta(hours=+9))
now_hour = datetime.now(JST).hour

if 0 <= now_hour and now_hour < 6:
    weather_now = weather_json["forecasts"][0]["chanceOfRain"]["T00_06"]
elif 6 <= now_hour and now_hour < 12:
    weather_now = weather_json["forecasts"][0]["chanceOfRain"]["T06_12"]
elif 12 <= now_hour and now_hour < 18:
    weather_now = weather_json["forecasts"][0]["chanceOfRain"]["T12_18"]
else:
    weather_now = weather_json["forecasts"][0]["chanceOfRain"]["T18_24"]

weather_now_text = "現在の降水確率:" + weather_now
st.write(weather_now_text)

# 予報の日付を取得し、それをインデックスに使用
forecast_dates = [datetime.now(JST) + timedelta(days=i) for i in range(3)]
forecast_dates_str = [d.strftime('%Y-%m-%d') for d in forecast_dates] # YYYY-MM-DD 形式に変換

# 予報データから降水確率の部分を抽出し、新しいカラム名でDataFrameを作成
def format_rain_chance(chance_of_rain):
    # カラム名を変更する
    new_columns = {
        'T00_06': '0～6時',
        'T06_12': '6～12時',
        'T12_18': '12～18時',
        'T18_24': '18～24時',
    }
    return {new_columns[k]: v for k, v in chance_of_rain.items() if k in new_columns}

# 各日付に対するDataFrameを作成
df1 = pd.DataFrame(format_rain_chance(weather_json["forecasts"][0]["chanceOfRain"]), index=[forecast_dates_str[0]])
df2 = pd.DataFrame(format_rain_chance(weather_json["forecasts"][1]["chanceOfRain"]), index=[forecast_dates_str[1]])
df3 = pd.DataFrame(format_rain_chance(weather_json["forecasts"][2]["chanceOfRain"]), index=[forecast_dates_str[2]])

# 3日分のDataFrameを結合
df = pd.concat([df1, df2, df3])

# StreamlitでDataFrameを表示
st.dataframe(df)
