import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Ubicación GPS", layout="centered")
st.title("📍 Obtener ubicación con un clic")

# Botón para obtener la ubicación
location = streamlit_geolocation()

# Verificar si se obtuvo la ubicación
if location and location.get("latitude") and location.get("longitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"✅ Coordenadas obtenidas:\nLatitud: {lat}\nLongitud: {lon}")

    # Mostrar mapa con marcador
    mapa = folium.Map(location=[lat, lon], zoom_start=16)
    folium.Marker([lat, lon], tooltip="📍 Aquí estás").add_to(mapa)
    folium_static(mapa)
else:
    st.warning("⚠ Presiona el botón para obtener tu ubicación.")