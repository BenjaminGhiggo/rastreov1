import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configurar la clave API de Gemini desde la variable de entorno
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("La clave API de Gemini no se encontró. Asegúrate de configurar 'GENAI_API_KEY' en tu archivo .env")

genai.configure(api_key=api_key)

# Función para manejar el chat directamente desde la terminal
def chat_con_usuario():
    print("Bienvenido al Chatbot con Gemini. Escribe 'salir' para terminar.")
    
    while True:
        # Obtener la entrada del usuario
        user_input = input("Tú: ").strip()
        if user_input.lower() == 'salir':
            print("Chat finalizado. ¡Hasta luego!")
            break
        
        try:
            # Llamar a la función que genera la respuesta
            respuesta = chat_con_gemini(user_input)
            print(f"Chatbot: {respuesta}")
        except Exception as e:
            print(f"Error al generar la respuesta: {e}")

# Función reutilizable para generar respuestas desde otros scripts
def chat_con_gemini(mensaje):
    try:
        model_name = "models/gemini-1.5-flash"  # Asegúrate de que este modelo esté disponible
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(mensaje)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    chat_con_usuario()
