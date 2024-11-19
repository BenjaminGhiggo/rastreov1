import streamlit as st
from chat import analizar_ruta_o_url, responder_consulta_usuario

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

# Sección para ingresar carpetas a ignorar
carpetas_ignorar_input = st.text_area("Ingrese las carpetas o patrones a ignorar (una por línea, con '/' al final para carpetas):")

# Botón para analizar la carpeta o URL
if st.button("Analizar Carpeta o URL"):
    if carpeta_input.strip():
        carpetas_a_ignorar = carpetas_ignorar_input.split("\n") if carpetas_ignorar_input.strip() else []
        respuesta = analizar_ruta_o_url(carpeta_input.strip(), carpetas_a_ignorar)
        st.success("Análisis completo. Puedes empezar a hacer preguntas sobre esta carpeta.")
        st.text_area("Resultados del análisis:", value=respuesta, height=200)
    else:
        st.warning("Por favor, ingrese una ruta válida o URL.")

# Sección de chat interactivo para consultas
st.header("💬 Consultas sobre la carpeta analizada")
consulta_input = st.text_input("Haz una pregunta sobre el contenido analizado:", value="")

if st.button("Enviar Consulta"):
    if consulta_input.strip():
        respuesta_consulta = responder_consulta_usuario(consulta_input.strip())
        st.text_area("Respuesta del Chatbot:", value=respuesta_consulta, height=150)
    else:
        st.warning("Por favor, ingrese una consulta antes de enviar.")

# Pie de página
st.markdown("---")
st.caption("Desarrollado con Streamlit y Gemini API.")
