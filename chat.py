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

# Variable global para almacenar el análisis de la carpeta
contenido_analizado = ""

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
def analizar_ruta_o_url(ruta, carpetas_a_ignorar):
    global contenido_analizado  # Permitir que se actualice la variable global
    if ruta.startswith("http://") or ruta.startswith("https://"):
        try:
            response = requests.get(ruta)
            response.raise_for_status()

            try:
                archivos = response.json()
                if not archivos:
                    return "La carpeta expuesta está vacía."
                contenido_analizado = f"Tengo la siguiente lista de archivos obtenida de la URL {ruta}:\n" + ", ".join(archivos)
            except ValueError:
                archivos = response.text.splitlines()
                if not archivos:
                    return "La URL no devolvió contenido utilizable."
                contenido_analizado = f"Tengo la siguiente lista de archivos obtenida de la URL {ruta}:\n" + ", ".join(archivos)
        except requests.exceptions.RequestException as e:
            return f"Error al acceder a la URL: {e}"
    elif os.path.isdir(ruta):
        contenido_analizado = analizar_carpeta_recursiva(ruta, carpetas_a_ignorar)
    else:
        return "Por favor, ingrese una ruta de carpeta válida o una URL expuesta con Ngrok."
    
    return "Análisis completo. Puedes empezar a hacer preguntas sobre esta carpeta."

# Función para analizar recursivamente una carpeta local ignorando las especificadas
def analizar_carpeta_recursiva(ruta_carpeta, carpetas_a_ignorar):
    try:
        # Convertir carpetas a ignorar a rutas absolutas normalizadas
        carpetas_a_ignorar_abs = {os.path.normpath(os.path.join(ruta_carpeta, ignorar.rstrip('/'))) for ignorar in carpetas_a_ignorar}
        
        contenido = []
        for root, dirs, files in os.walk(ruta_carpeta):
            # Excluir carpetas ignoradas en la iteración de os.walk
            dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in carpetas_a_ignorar_abs]
            
            relative_path = os.path.relpath(root, ruta_carpeta)
            contenido.append(f"📂 Carpeta: {relative_path}")
            for archivo in files:
                contenido.append(f"    📄 Archivo: {archivo}")
        
        return f"Estoy analizando la carpeta '{ruta_carpeta}' y encontré lo siguiente:\n\n" + "\n".join(contenido)
    except Exception as e:
        return f"Error al analizar la carpeta local: {e}"

# Función para responder preguntas basadas en el análisis
def responder_consulta_usuario(pregunta):
    global contenido_analizado
    if not contenido_analizado:
        return "Primero debes analizar una carpeta antes de hacer consultas."
    
    prompt = f"""
Basándote en el siguiente contenido de la carpeta:

{contenido_analizado}

Responde a la siguiente pregunta del usuario:

{pregunta}
"""
    return chat_con_gemini(prompt)
