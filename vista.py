import streamlit as st
from chat import analizar_ruta_o_url

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
