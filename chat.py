import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configurar la clave API de Gemini desde la variable de entorno
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("La clave API de Gemini no se encontró. Asegúrate de configurar 'GENAI_API_KEY' en tu archivo .env")

genai.configure(api_key=api_key)

# Función reutilizable para generar respuestas con Gemini
def chat_con_gemini(mensaje):
    try:
        model_name = "models/gemini-1.5-flash"  # Asegúrate de que este modelo esté disponible
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(mensaje)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# Función para analizar archivos en una carpeta local o desde una URL expuesta
def analizar_ruta_o_url(ruta):
    if ruta.startswith("http://") or ruta.startswith("https://"):
        try:
            # Hacer la solicitud GET a la URL
            response = requests.get(ruta)
            response.raise_for_status()

            # Intentar interpretar la respuesta como JSON o texto plano
            try:
                archivos = response.json()
                if not archivos:
                    return "La carpeta expuesta está vacía."
                prompt = f"Tengo la siguiente lista de archivos obtenida de la URL {ruta}:\n" + ", ".join(archivos)
            except ValueError:
                # Si la respuesta no es JSON, manejar como texto plano
                archivos = response.text.splitlines()
                if not archivos:
                    return "La URL no devolvió contenido utilizable."
                prompt = f"Tengo la siguiente lista de archivos obtenida de la URL {ruta}:\n" + ", ".join(archivos)
            
            return chat_con_gemini(prompt)
        except requests.exceptions.RequestException as e:
            return f"Error al acceder a la URL: {e}"
    elif os.path.isdir(ruta):
        # Si es una ruta local, listar archivos
        try:
            archivos = os.listdir(ruta)
            if not archivos:
                return "La carpeta local está vacía."
            prompt = f"Tengo la siguiente lista de archivos en la carpeta local {ruta}:\n" + ", ".join(archivos)
            return chat_con_gemini(prompt)
        except Exception as e:
            return f"Error al acceder a la carpeta local: {e}"
    else:
        return "Por favor, ingrese una ruta de carpeta válida o una URL expuesta con Ngrok."
