import streamlit as st
import folium
from folium.features import CustomIcon
from streamlit_folium import folium_static
import requests
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="🧭 Clínicas cercanas", layout="centered")
st.title("📍 Resultados desde coordenadas fijas")

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
    "clinic": "https://cdn-icons-png.flaticon.com/512/2967/2967350.png",
    "laboratory": "https://cdn-icons-png.flaticon.com/512/3343/3343841.png"
}

# Lista para guardar resultados
resultados_tabla = []

for tipo, icon_url in tipo_iconos.items():
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lon}&radius=3000&type={tipo}&key={API_KEY}"
    )
    response = requests.get(url)
    lugares = response.json().get("results", [])

    for lugar in lugares:
        nombre = lugar.get("name", "Sin nombre")
        direccion = lugar.get("vicinity", "")
        ubicacion = lugar["geometry"]["location"]

        # Agregar al mapa
        icono_personalizado = CustomIcon(icon_image=icon_url, icon_size=(40, 40))
        folium.Marker(
            [ubicacion["lat"], ubicacion["lng"]],
            popup=f"{nombre}\n{direccion}",
            tooltip=nombre,
            icon=icono_personalizado
        ).add_to(mapa)

        # Agregar a tabla
        resultados_tabla.append({
            "Nombre": nombre,
            "Dirección": direccion,
            "Tipo": tipo.capitalize()
        })

# Mostrar mapa
folium_static(mapa)

# Mostrar tabla
if resultados_tabla:
    st.subheader("📋 Lugares encontrados")
    df_resultados = pd.DataFrame(resultados_tabla)
    st.dataframe(df_resultados)
else:
    st.info("No se encontraron lugares cercanos.")
