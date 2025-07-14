# =====================
# 1. IMPORTS Y LOGIN MULTIUSUARIO
# =====================
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import yaml

# --- Configuración de usuarios para login multiusuario ---
#Un usuario maestro y un usuario sin acceso completo
config = {
    'credentials': {
        'usernames': {
            'admin': {
                'email': 'seba.villalba@hotmail.com',
                'name': 'Master User',
                'password': stauth.Hasher(['adminpass']).generate()[0]
            },
            'sebastian': {
                'email': 'seba.villalba@hotmail.com',
                'name': 'admin',
                'password': stauth.Hasher(['admin']).generate()[0]
            }
        }
    },
    'cookie': {'expiry_days': 1},
    'preauthorized': {}
}

# Login y control de sesión
authenticator = stauth.Authenticate(
    config['credentials'],
    "app_cookie", "random_key", config['cookie']['expiry_days']
)
name, authentication_status, username = authenticator.login('Iniciar sesión', 'main')

if authentication_status is None:
    st.warning("Ingrese usuario y contraseña")
    st.stop()
elif authentication_status is False:
    st.error("Usuario/contraseña incorrectos")
    st.stop()
else:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido, {name}!")

# =====================
# 2. MENÚ Y NAVEGACIÓN
# =====================
page = st.sidebar.radio(
    "Navegación",
    ["Página 1: DATOS FISICO", "Página 2: DATOS FUTBOLISTICOS"],
    key="mainmenu"
)

# =====================
# 3. CONEXIÓN A GOOGLE SHEETS (Página 1)
# =====================
@st.cache_data(show_spinner="Conectando a Google Sheets...")
def cargar_gsheet():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/e/2PACX-1vS5rtNSfkU6OaYmPWb-OeGfV7xfuHce2G76mArU-6HfldXAUAF8fErz20Lo9FyR6Fb9bBQdQsHNwgw_/pubhtml?gid=0&single=true").sheet1
    data = pd.DataFrame(sheet.get_all_records())
    return data

if page == "Página 1: DATOS FISICOS":
    st.header("Datos desde Google Sheets")
    try:
        df_sheet = cargar_gsheet()
        st.dataframe(df_sheet)
        if not df_sheet.empty:
            # Visualización
            col1 = df_sheet.columns[0]
            col2 = df_sheet.columns[1] if len(df_sheet.columns) > 1 else df_sheet.columns[0]
            fig = px.bar(df_sheet, x=col1, y=col2, title=f"Gráfica {col1} vs {col2}")
            st.plotly_chart(fig)
            # Botón exportar a CSV
            st.download_button("Exportar a CSV", df_sheet.to_csv(index=False), file_name="datos_fisicos.csv", mime="text/csv")
            # Botón imprimir
            if st.button("Imprimir página"):
                st.write("Presione **Ctrl+P** en su navegador para imprimir esta página.")
    except Exception as e:
        st.error("Error al conectar a Google Sheets: " + str(e))

# =====================
# 4. CONEXIÓN A API FÚTBOL ARGENTINO (Página 2)
# =====================
# Clave de acceso personal (copiar desde https://dashboard.api-football.com/)
API_KEY = "601d3521218542e683b5083f6ebd969f"  # ← Reemplazá por tu clave real
headers = {"x-apisports-key": API_KEY}

@st.cache_data(show_spinner="Cargando datos de jugadores...")
def get_union_team_id():
    url = "https://v3.football.api-sports.io/teams?search=union"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for team in data["response"]:
            if team["team"]["name"].lower() == "union santa fe":
                return team["team"]["id"]
    return None

@st.cache_data(show_spinner="Obteniendo estadísticas de jugadores...")
def get_jugadores_union(team_id):
    jugadores_total = []
    for season in [2022, 2023, 2024, 2025]:
        url = f"https://v3.football.api-sports.io/players?team={team_id}&season={season}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for item in data["response"]:
                jugador = {
                    "nombre": item["player"]["name"],
                    "edad": item["player"]["age"],
                    "posición": item["statistics"][0]["games"]["position"],
                    "temporada": season,
                    "partidos": item["statistics"][0]["games"]["appearences"],
                    "titular": item["statistics"][0]["games"]["lineups"],
                    "goles": item["statistics"][0]["goals"]["total"],
                    "asistencias": item["statistics"][0]["goals"]["assists"],
                    "minutos": item["statistics"][0]["games"]["minutes"],
                }
                jugadores_total.append(jugador)
    return pd.DataFrame(jugadores_total)

# Streamlit: Página 2
if page == "Página 2: API Fútbol Argentino":
    st.header("Estadísticas por Jugador - Unión de Santa Fe (2022-2025)")
    team_id = get_union_team_id()

    if team_id:
        df_jugadores = get_jugadores_union(team_id)
        if not df_jugadores.empty:
            st.dataframe(df_jugadores)

            # Visualización: Goles por jugador
            fig = px.bar(
                df_jugadores.groupby("nombre")["goles"].sum().reset_index(),
                x="nombre", y="goles",
                title="Goles acumulados por jugador (2022-2025)",
                text_auto=True, template="plotly_white"
            )
            st.plotly_chart(fig)

            # Exportar CSV
            st.download_button("Exportar a CSV", df_jugadores.to_csv(index=False),
                               file_name="jugadores_union_2022_2025.csv", mime="text/csv")

            # Botón imprimir
            if st.button("Imprimir página"):
                st.info("Presione **Ctrl+P** en su navegador para imprimir esta página.")
        else:
            st.warning("No se encontraron datos de jugadores.")
    else:
        st.error("No se pudo encontrar el ID del equipo Unión de Santa Fe.")
# =====================
# 5. NOTA SOBRE OPTIMIZACIÓN (CACHE)
# =====================
# Todas las funciones de conexión usan @st.cache_data para acelerar la app.

# =====================
# 6. NOTA FINAL SOBRE DESPLIEGUE
# =====================
# Una vez creado app.py y requirements.txt, sube ambos a GitHub y despliega en Streamlit Cloud.
