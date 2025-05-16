import streamlit as st
import folium
from folium.features import CustomIcon
from streamlit_folium import folium_static
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="🧭 Clínicas cercanas", layout="centered")
st.title("📍 Clínicas, hospitales y laboratorios cercanos")

# Coordenadas fijas
lat = 25.6502102
lon = -100.2901238

# Crear mapa base
mapa = folium.Map(location=[lat, lon], zoom_start=15)
folium.Marker(
    [lat, lon],
    tooltip="📍 Punto de partida",
    popup="Coordenadas iniciales",
    icon=folium.Icon(color="blue")
).add_to(mapa)

# --- CONSULTA A GOOGLE PLACES API ---
API_KEY = st.secrets["google_places_key"]

tipo_iconos = {
    "hospital": "https://cdn-icons-png.flaticon.com/512/1484/1484848.png",
    "clínica": "https://cdn-icons-png.flaticon.com/512/2967/2967350.png",
    "laboratorio": "https://cdn-icons-png.flaticon.com/512/3343/3343841.png"
}

for keyword, icon_url in tipo_iconos.items():
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lon}&radius=3000&keyword={keyword}&key={API_KEY}"
    )
    response = requests.get(url)
    lugares = response.json().get("results", [])

    for lugar in lugares:
        nombre = lugar.get("name", "Sin nombre")
        direccion = lugar.get("vicinity", "")
        ubicacion = lugar["geometry"]["location"]

        icono_personalizado = CustomIcon(icon_image=icon_url, icon_size=(40, 40))

        folium.Marker(
            [ubicacion["lat"], ubicacion["lng"]],
            popup=f"{nombre}\n{direccion}",
            tooltip=nombre,
            icon=icono_personalizado
        ).add_to(mapa)

# Mostrar solo el mapa
folium_static(mapa)
