import streamlit as st
import requests

# ===== CONFIGURACIÓN DE PÁGINA =====
st.set_page_config(page_title="Clima El Salvador 🌤️", page_icon="☀️", layout="centered")

# ===== ESTILOS PERSONALIZADOS =====
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #5f2c82, #49a09d);
            background-attachment: fixed;
            color: #ffffff;
        }
        .titulo {
            text-align: center;
            font-size: 44px;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
            margin-bottom: 5px;
        }
        .subtitulo {
            text-align: center;
            font-size: 18px;
            color: #e0f7fa;
            margin-bottom: 25px;
        }
        .tarjeta {
            background: rgba(255,255,255,0.15);
            border-radius: 20px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.25);
            margin-top: 15px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
        }
        div.stButton > button {
            background: linear-gradient(90deg, #ff758c, #ff7eb3);
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
            padding: 10px 30px;
            transition: all 0.3s ease;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #ff7eb3, #ff758c);
            transform: scale(1.07);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e3c72, #2a5298);
            color: white;
        }
        .stSelectbox label, .stTextInput label {
            color: #ffffff !important;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# ===== CABECERA =====
st.markdown('<div class="titulo">🌈 Clima en El Salvador</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Elegí el departamento y municipio para conocer el clima actual ☀️🌧️</div>', unsafe_allow_html=True)

# ===== DEPARTAMENTOS Y MUNICIPIOS =====
municipios_por_departamento = {
    "Ahuachapán": ["Ahuachapán", "Apaneca", "Atiquizaya", "Turín"],
    "Santa Ana": ["Santa Ana", "Metapán", "Chalchuapa", "Coatepeque"],
    "Sonsonate": ["Sonsonate", "Nahuizalco", "Izalco", "Armenia"],
    "Chalatenango": ["Chalatenango", "La Palma", "Nueva Concepción"],
    "La Libertad": ["Santa Tecla", "Antiguo Cuscatlán", "Nuevo Cuscatlán", "Comasagua"],
    "San Salvador": ["San Salvador", "Soyapango", "Mejicanos", "Ilopango", "Ciudad Delgado"],
    "Cuscatlán": ["Cojutepeque", "Suchitoto", "San Rafael Cedros"],
    "La Paz": ["Zacatecoluca", "Olocuilta", "San Juan Talpa"],
    "Cabañas": ["Sensuntepeque", "Victoria", "Ilobasco"],
    "San Vicente": ["San Vicente", "Tecoluca", "Apastepeque"],
    "Usulután": ["Usulután", "Jiquilisco", "Santiago de María"],
    "San Miguel": [
        "Carolina", "Chapeltique", "Chinameca", "Chirilagua", "Ciudad Barrios", "Comacarán",
        "El Tránsito", "Lolotique", "Moncagua", "Nueva Guadalupe", "Nuevo Edén de San Juan",
        "Quelepa", "San Antonio", "San Gerardo", "San Jorge", "San Luis de la Reina", "San Miguel",
        "San Rafael Oriente", "Sesori", "Uluazapa"
    ],
    "Morazán": ["San Francisco Gotera", "Jocoro", "Sociedad"],
    "La Unión": ["La Unión", "Conchagua", "Anamorós"]
}

API_KEY = "2dd69aa6409c97ff65127af01a603d9a"

# ===== ENTRADA PRINCIPAL =====
departamento = st.selectbox(" Seleccioná un departamento", list(municipios_por_departamento.keys()))
municipio = st.selectbox(" Seleccioná un municipio (opcional)", [""] + municipios_por_departamento[departamento])

# ===== SIDEBAR =====
with st.sidebar:
    st.header("⚙️ Opciones rápidas")
    dep_sidebar = st.selectbox("Departamento (sidebar)", [""] + list(municipios_por_departamento.keys()))
    mun_sidebar = st.selectbox("Municipio (sidebar)", [""] + (municipios_por_departamento.get(dep_sidebar, []) if dep_sidebar else []))
    ver_clima_sidebar = st.button("🌤️ Ver clima desde sidebar")

# ===== BOTÓN PRINCIPAL =====
if st.button("🌦️ Ver clima") or ver_clima_sidebar:
    # Priorizar: municipio sidebar > municipio principal > departamento
    if mun_sidebar:
        lugar = mun_sidebar
    elif municipio:
        lugar = municipio
    elif dep_sidebar:
        lugar = dep_sidebar
    else:
        lugar = departamento

    if lugar:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={lugar},SV&appid={API_KEY}&units=metric&lang=es"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            info = {
                "País": data["sys"]["country"],
                "Ciudad": data["name"],
                "Temperatura": f"{data['main']['temp']}°C",
                "Humedad": f"{data['main']['humidity']}%",
                "Descripción": data["weather"][0]["description"].capitalize(),
                "Viento": f"{data['wind']['speed']} km/h"
            }

            st.markdown(f"""
                <div class="tarjeta">
                    <h4>📍 {info['Ciudad']}, {info['País']}</h4>
                    <p>🌡️ <b>Temperatura:</b> {info['Temperatura']}</p>
                    <p>💧 <b>Humedad:</b> {info['Humedad']}</p>
                    <p>🌤️ <b>Clima:</b> {info['Descripción']}</p>
                    <p>💨 <b>Viento:</b> {info['Viento']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("No se encontró la ciudad o municipio.")
    else:
        st.warning("Seleccioná al menos un departamento o municipio.")
