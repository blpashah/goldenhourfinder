import streamlit as st
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, date
import requests

# ---------- CONFIG ----------
st.set_page_config(page_title="Golden Hour Finder", page_icon="🌅")

st.title("🌅 Golden Hour & Weather Finder")

st.write("📍 Enter a precise address or landmark to find golden hour times and weather!")

# ---------- INPUT ----------
address = st.text_input("Address or Location", value="Eiffel Tower, Paris")
selected_date = st.date_input("Select Date", date.today())

# ---------- GEOCODING ----------
def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(url, params=params, headers={'User-Agent': 'streamlit-app'})
    data = response.json()
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        display_name = data[0]['display_name']
        return lat, lon, display_name
    else:
        return None, None, None

# ---------- PROCESS ----------
if address:
    lat, lon, location_name = geocode_address(address)

    if lat and lon:
        st.success(f"📍 Found: {location_name} (Lat: {lat:.4f}, Lon: {lon:.4f})")

        loc = LocationInfo(name=location_name, region="", timezone="UTC", latitude=lat, longitude=lon)
        s = sun(loc.observer, date=selected_date)

        # Calculate golden hour (approx: hour after sunrise & hour before sunset)
        sunrise = s['sunrise'].astimezone()
        sunset = s['sunset'].astimezone()
        golden_start = sunrise
        golden_end = sunrise.replace(hour=sunrise.hour+1)
        golden_start2 = sunset.replace(hour=sunset.hour-1)
        golden_end2 = sunset

        st.subheader("🌞 Solar Times")
        st.write(f"**Sunrise:** {sunrise.strftime('%H:%M')}")
        st.write(f"**Golden Hour Morning:** {golden_start.strftime('%H:%M')} – {golden_end.strftime('%H:%M')}")
        st.write(f"**Golden Hour Evening:** {golden_start2.strftime('%H:%M')} – {golden_end2.strftime('%H:%M')}")
        st.write(f"**Sunset:** {sunset.strftime('%H:%M')}")

        # ---------- WEATHER ----------
        st.subheader("🌤️ Weather Forecast")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,cloudcover_mean&timezone=auto&start_date={selected_date}&end_date={selected_date}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if 'daily' in weather_data:
            temp_max = weather_data['daily']['temperature_2m_max'][0]
            temp_min = weather_data['daily']['temperature_2m_min'][0]
            clouds = weather_data['daily']['cloudcover_mean'][0]
            precip = weather_data['daily']['precipitation_sum'][0]

            st.write(f"**Temperature:** {temp_min}°C – {temp_max}°C")
            st.write(f"**Cloud Cover:** {clouds}%")
            st.write(f"**Precipitation:** {precip} mm")

        else:
            st.warning("Could not fetch weather forecast. Try again later.")

    else:
        st.error("❌ Could not find that address. Try something more specific!")
