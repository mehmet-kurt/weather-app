import streamlit as st
import requests

# Sayfa yapılandırması
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# PySide6'daki CSS stilini Streamlit'e aktarma
st.markdown("""
<style>
    .main-title {
        font-family: Calibri, sans-serif;
        font-size: 32px;
        font-style: italic;
        text-align: center;
        color: #555;
        margin-bottom: 0.5rem;
    }
    .weather-icon {
        font-family: 'Segoe UI Emoji', sans-serif;
        font-size: 80px;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0px;
    }
    .temp-text {
        font-family: Calibri, sans-serif;
        font-size: 68px;
        font-weight: bold;
        text-align: center;
        margin: 0px;
    }
    .condition-text {
        font-family: Calibri, sans-serif;
        font-size: 40px;
        text-align: center;
        color: #666;
        margin-top: 0px;
    }
    div.stButton > button {
        width: 100%;
        font-size: 24px;
        font-weight: bold;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

def weather_emoji(weather_id: int) -> str:
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌦️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "❄️"
    elif 700 <= weather_id <= 781:
        if weather_id in (701, 721, 741):
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🌀"
        elif weather_id == 781:
            return "🌪️"
        return ""
    elif weather_id == 800:
        return "☀️"
    elif weather_id > 800:
        return "☁️"
    return ""

st.markdown('<div class="main-title">Enter a city name:</div>', unsafe_allow_html=True)

# Şehir giriş alanı ve Enter butonu
city_name = st.text_input("Enter city name", label_visibility="collapsed")
get_weather_btn = st.button("Enter")

if get_weather_btn:
    if not city_name.strip():
        st.warning("Please enter a valid city name.")
    else:
        api_key = "d727127cbf3120c324fba5a0c22a8b0d"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name.strip()}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("cod") == 200:
                temp_k = data["main"]["temp"]
                temp_c = temp_k - 273.15
                weather_desc = data["weather"][0]["description"].capitalize()
                emoji = weather_emoji(data["weather"][0]["id"])

                # Kart düzeninde sonuçları bas
                st.markdown(f'<div class="weather-icon">{emoji}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="temp-text">{temp_c:.0f}°C</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="condition-text">{weather_desc}</div>', unsafe_allow_html=True)

        except requests.exceptions.HTTPError:
            status = response.status_code
            if status == 400:
                st.error("Bad Request:\nPlease check your input")
            elif status == 401:
                st.error("Unauthorized:\nInvalid API key")
            elif status == 404:
                st.error("Not Found:\nCity could not found")
            elif status == 500:
                st.error("Internal Server Error\nPlease try again later")
            else:
                st.error("HTTP error occured")

        except requests.exceptions.ConnectionError:
            st.error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.RequestException:
            st.error("Please Try Again Later")