import google.generativeai as genai
from django.conf import settings
import logging
import re

logger = logging.getLogger(__name__)

def generar_codigo_grafico(enunciado, error_previo=None):
    """
    Solicita a la IA (Gemini) código Matplotlib para representar una figura geométrica. (HU48)
    """
    if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY no configurada.")
        return None

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = (
        f"Eres un experto en Python y Matplotlib. Tu tarea es generar código para dibujar una figura geométrica.\n\n"
        f"CONTEXTO:\n"
        f"- Enunciado: {enunciado}\n"
        f"- Estilo: Didáctico Colorido (usa colores distintos para partes clave, etiquetas claras).\n"
        f"- Formato: Matplotlib (pyplot).\n\n"
        f"REGLAS ESTRICTAS:\n"
        f"1. Devuelve EXCLUSIVAMENTE el código Python puro, sin bloques markdown (no use ```python).\n"
        f"2. No use plt.show(). Use plt.savefig(buffer, format='svg') al final.\n"
        f"3. No importe librerías peligrosas (os, sys, etc). Solo use: import matplotlib.pyplot as plt, import numpy as np.\n"
        f"4. Asegúrese de que el gráfico sea proporcional y legible.\n"
    )

    if error_previo:
        prompt += f"\nNOTA: El intento anterior falló con este error: {error_previo}. Por favor, corrígelo.\n"

    try:
        response = model.generate_content(prompt)
        codigo = response.text.strip()
        
        # Limpiar posibles bloques markdown si la IA ignora la instrucción
        codigo = re.sub(r'```python|```', '', codigo).strip()
        
        return codigo
    except Exception as e:
        logger.error(f"Error llamando a Gemini para gráfico: {e}")
        return None

def validar_codigo_seguro(codigo):
    """
    Realiza una validación básica de seguridad (Sandbox) sobre el código generado. (HU48)
    """
    if not codigo:
        return False
    
    # Lista negra de términos peligrosos
    blacklist = [
        'os.', 'sys.', 'subprocess', 'eval(', 'exec(', 'getattr', 'setattr', 
        '__import__', 'open(', 'write(', 'read(', 'shutil', 'socket'
    ]
    
    for term in blacklist:
        if term in codigo:
            logger.warning(f"Código bloqueado por seguridad: Contiene '{term}'")
            return False
            
    # Lista blanca de imports permitidos (debe contener al menos matplotlib)
    if 'import matplotlib' not in codigo and 'from matplotlib' not in codigo:
        logger.warning("Código bloqueado: No importa matplotlib")
        return False
        
    return True

import io
from django.core.files.base import ContentFile
from .models import Ejercicio

def ejecutar_grafico_y_guardar(codigo, ejercicio_id):
    """
    Ejecuta el código Matplotlib en un entorno controlado y guarda el SVG resultante. (HU48)
    """
    if not validar_codigo_seguro(codigo):
        return False, "Código no seguro"

    buffer = io.BytesIO()
    
    # Entorno local para la ejecución
    loc = {'plt': None, 'np': None, 'buffer': buffer}
    
    # Preparar el código para usar el buffer
    # Asegurarnos de que no intente abrir ventanas y que guarde en el buffer
    pre_script = (
        "import matplotlib\n"
        "matplotlib.use('Agg')\n" # Backend no interactivo
        "import matplotlib.pyplot as plt\n"
        "import numpy as np\n"
        "plt.figure(figsize=(6, 4))\n"
    )
    post_script = "\nplt.savefig(buffer, format='svg')\nplt.close()"
    
    full_script = pre_script + codigo + post_script
    
    try:
        # Ejecución controlada. Matplotlib necesita __import__ para funcionar internamente.
        # La seguridad se garantiza principalmente mediante validar_codigo_seguro previo.
        exec(full_script, {"__builtins__": __builtins__}, loc)
        
        # Guardar en el modelo
        ejercicio = Ejercicio.objects.get(id=ejercicio_id)
        nombre_archivo = f"auto_graphic_{ejercicio_id}.svg"
        
        buffer.seek(0)
        ejercicio.imagen.save(nombre_archivo, ContentFile(buffer.read()), save=True)
        
        return True, None
    except Exception as e:
        logger.error(f"Error ejecutando código de gráfico para ejercicio {ejercicio_id}: {e}")
        return False, str(e)

def procesar_imagen_automatica(enunciado, ejercicio):
    """
    Orquestador de generación de imagen con reintento único. (HU48)
    """
    # Intento 1
    codigo = generar_codigo_grafico(enunciado)
    if not codigo:
        return False

    success, error = ejecutar_grafico_y_guardar(codigo, ejercicio.id)
    
    if success:
        return True
    
    # Intento 2 (Reintento con error detallado)
    logger.info(f"Reintentando generación de gráfico para ejercicio {ejercicio.id} debido a error: {error}")
    codigo_retry = generar_codigo_grafico(enunciado, error_previo=error)
    if not codigo_retry:
        return False
        
    success_retry, error_retry = ejecutar_grafico_y_guardar(codigo_retry, ejercicio.id)
    
    if not success_retry:
        logger.error(f"Fallo definitivo en generación de gráfico para ejercicio {ejercicio.id}: {error_retry}")
        
    return success_retry
