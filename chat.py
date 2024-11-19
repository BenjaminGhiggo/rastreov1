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

        if os.path.isdir(user_input):
            respuesta = analizar_archivos_en_carpeta(user_input)
        else:
            respuesta = chat_con_gemini(user_input)
        
        print(f"Chatbot: {respuesta}")

# Función para usar Gemini para clasificar tipos de archivos
def analizar_archivos_en_carpeta(ruta_carpeta):
    try:
        archivos = os.listdir(ruta_carpeta)
        if not archivos:
            return "La carpeta está vacía."

        prompt = f"""
Tengo la siguiente lista de archivos en la carpeta {ruta_carpeta}:
{', '.join(archivos)}

Por favor, analiza y clasifica cada archivo indicando qué tipo de archivo es según su extensión y, si es posible, su propósito.
Proporciona una descripción breve para cada tipo de archivo.
"""
        model_name = "models/gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"Error al analizar la carpeta: {e}"

# Función reutilizable para generar respuestas de texto general con Gemini
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
