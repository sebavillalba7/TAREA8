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


---

## Requisitos previos

- **Python 3.9 o superior**
- (Opcional) Entorno virtual con Conda o venv

## Instalación y ejecución

1. **(Opcional) Crear y activar entorno virtual:**
    - Si usas Conda:
      ```bash
      conda create -n tarea_m8 python=3.9
      conda activate tarea_m8
      ```
    - O con venv (alternativa):
      ```bash
      python -m venv venv
      # En Windows:
      venv\Scripts\activate
      # En Mac/Linux:
      source venv/bin/activate
      ```

2. **Ubícate en la carpeta del proyecto:**
    - Si descomprimiste el ZIP, entra a la carpeta raíz del proyecto. Ejemplo:
      ```bash
      cd ruta/a/la/carpeta/del/proyecto
      ```

3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **(Opcional) Configura variables de entorno:**
    - Si la app usa claves API, edita el archivo `.env` según las instrucciones del código.

5. **Ejecuta la aplicación:**
    ```bash
    streamlit run app.py
    ```

6. **Accede desde el navegador:**
    - Generalmente se abre en `http://localhost:8501` automáticamente.
    - Si quieres ver la app publicada, accede a:
      [https://tarea8-djz2ttg77xpypxg9veqjza.streamlit.app/]

7. **Login:**
    - Usuario: `admin`
    - Contraseña: `admin`
	
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

Desarrollada por Mag. Sebastián Villalba – [SV Sports Scientist](sebastiangvillalba@gmail.com)