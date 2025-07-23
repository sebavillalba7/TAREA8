# Panel Deportivo - Streamlit App

## Descripción

Esta aplicación permite la visualización, filtrado y exportación de datos físicos y futbolísticos de jugadores, integrando datos de Google Sheets y estadísticas vía API. Permite login seguro, visualización interactiva y descarga de reportes personalizados en PDF.

- **Autor:** Mag. Sebastián Villalba
- **Licencia:** Uso académico

---

## Estructura del proyecto

```plaintext
TAREA/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── assets/
│   └── logo.png
├── .streamlit/
│   └── config.toml
├── data/
├── models/
├── controllers/
├── common/
└── pages/
```


## Instalación y ejecución

1. **Crea y activa el entorno:**
    ```bash
    conda activate tarea_m8
    ```

2. **Ubícate en el directorio:**
    ```bash
    cd C:\Users\union\Documents\Python_CAU\M8\TAREA
    ```

3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecuta la aplicación:**
    ```bash
    streamlit run app.py
    ```

5. **Accede desde el navegador:**
    - [http://localhost:8501](http://localhost:8501) *(o la URL de red que te muestra Streamlit)*

---

## Usuario y contraseña

- **Usuario:** admin
- **Contraseña:** admin

---

## Funcionalidades principales

- Autenticación y login seguro con Streamlit Authenticator.
- Filtros avanzados sobre datos físicos de Google Sheets (por temporada, fecha, jugador, rival, posición, etc.).
- Integración de estadísticas futbolísticas vía API.
- Visualización interactiva de métricas y gráficos con Plotly.
- Exportación de reportes individuales a PDF.
- Descarga de archivos PDF personalizados desde la app.
- Uso de caché para optimizar el acceso y visualización de datos.

---

## Manejo de caché

Se implementó el decorador `@st.cache_data` en la función de carga de datos de Google Sheets para mejorar la eficiencia de las consultas y la experiencia de usuario.

---

## Personalización visual

La aplicación utiliza una paleta de colores personalizada y CSS inyectado para mejorar la experiencia de usuario, manteniendo coherencia con el logo y la identidad visual del proyecto.

---

## Configuración de Streamlit

El archivo `.streamlit/config.toml` configura parámetros del servidor y el tema de la app.

---

## Créditos

Desarrollada por Mag. Sebastián Villalba – [SV Sports Scientist](mailto:svsports.scientist@gmail.com)


