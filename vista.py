import streamlit as st
import os
import requests
from chat import analizar_archivos_en_carpeta

# Configurar la página
st.set_page_config(
    page_title="Análisis de Carpeta con Gemini",
    page_icon="📂",
    layout="centered"
)

# Título de la aplicación
st.title("📂 Análisis de Carpeta con Gemini")
st.subheader("Explora y clasifica los archivos en una carpeta o desde una URL expuesta con Ngrok.")

# Sección para ingresar la ruta de la carpeta o URL
carpeta_input = st.text_input("Ingrese la ruta de la carpeta o URL expuesta con Ngrok:", value="")

# Función para manejar URLs y carpetas locales
def analizar_ruta_o_url(ruta):
    if ruta.startswith("http://") or ruta.startswith("https://"):
        try:
            # Hacer la solicitud GET a la URL
            response = requests.get(ruta)
            response.raise_for_status()
            
            # Verificar si la URL contiene una lista de archivos
            archivos = response.json()  # Suponiendo que la URL expuesta devuelve un JSON con la lista de archivos
            if not archivos:
                return "La carpeta expuesta está vacía."
            
            # Crear un prompt con los nombres de los archivos
            prompt = f"Tengo la siguiente lista de archivos obtenida de la URL {ruta}:\n" + ", ".join(archivos)
            return analizar_archivos_en_carpeta(prompt)
        except requests.exceptions.RequestException as e:
            return f"Error al acceder a la URL: {e}"
        except ValueError:
            return "La URL no devolvió una lista de archivos válida."
    elif os.path.isdir(ruta):
        # Si es una ruta local, usar la función de análisis de archivos
        return analizar_archivos_en_carpeta(ruta)
    else:
        return "Por favor, ingrese una ruta de carpeta válida o una URL expuesta con Ngrok."

# Botón para analizar la carpeta o URL
if st.button("Analizar Carpeta o URL"):
    if carpeta_input.strip():
        respuesta = analizar_ruta_o_url(carpeta_input.strip())
        st.text_area("Resultados del análisis:", value=respuesta, height=200)
    else:
        st.warning("Por favor, ingrese una ruta válida o URL.")

# Pie de página
st.markdown("---")
st.caption("Desarrollado con Streamlit y Gemini API.")
