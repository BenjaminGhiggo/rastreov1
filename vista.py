import streamlit as st
from chat import chat_con_gemini  # Importar la función del chatbot desde chat.py

# Configurar la página
st.set_page_config(
    page_title="Chatbot con Gemini",
    page_icon="🤖",
    layout="centered"
)

# Título de la aplicación
st.title("🤖 Chatbot con Gemini")
st.subheader("Interfaz sencilla para interactuar con el chatbot.")

# Área de entrada del usuario
user_input = st.text_input("Escribe tu mensaje aquí:", value="", max_chars=200)

# Botón para enviar el mensaje
if st.button("Enviar"):
    if user_input.strip():
        # Obtener la respuesta del chatbot
        try:
            respuesta = chat_con_gemini(user_input)
            st.text_area("Respuesta del Chatbot:", value=respuesta, height=150)
        except Exception as e:
            st.error(f"Error al obtener la respuesta: {e}")
    else:
        st.warning("Por favor, ingresa un mensaje antes de enviar.")

# Pie de página
st.markdown("---")
st.caption("Desarrollado con Streamlit y Gemini API.")

