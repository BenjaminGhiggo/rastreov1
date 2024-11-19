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

# Función para analizar recursivamente una carpeta local o desde una URL expuesta
def analizar_ruta_o_url(ruta):
    if ruta.startswith("http://") or ruta.startswith("https://"):
        try:
            response = requests.get(ruta)
            response.raise_for_status()

            try:
                archivos = response.json()
                if not archivos:
                    return "La carpeta expuesta está vacía."
                prompt = f"Tengo la siguiente lista de archivos obtenida de la URL {ruta}:\n" + ", ".join(archivos)
            except ValueError:
                archivos = response.text.splitlines()
                if not archivos:
                    return "La URL no devolvió contenido utilizable."
                prompt = f"Tengo la siguiente lista de archivos obtenida de la URL {ruta}:\n" + ", ".join(archivos)
            
            return chat_con_gemini(prompt)
        except requests.exceptions.RequestException as e:
            return f"Error al acceder a la URL: {e}"
    elif os.path.isdir(ruta):
        return analizar_carpeta_recursiva(ruta)
    else:
        return "Por favor, ingrese una ruta de carpeta válida o una URL expuesta con Ngrok."

# Función para analizar recursivamente una carpeta local
def analizar_carpeta_recursiva(ruta_carpeta):
    try:
        contenido = []
        for root, dirs, files in os.walk(ruta_carpeta):
            relative_path = os.path.relpath(root, ruta_carpeta)
            contenido.append(f"📂 Carpeta: {relative_path}")
            for archivo in files:
                contenido.append(f"    📄 Archivo: {archivo}")
        
        prompt = f"Estoy analizando la carpeta '{ruta_carpeta}' y encontré lo siguiente:\n\n" + "\n".join(contenido)
        return chat_con_gemini(prompt)
    except Exception as e:
        return f"Error al analizar la carpeta local: {e}"
