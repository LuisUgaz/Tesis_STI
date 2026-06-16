import google.generativeai as genai
from django.conf import settings
import logging
import json
from PIL import Image

logger = logging.getLogger(__name__)

def generar_representacion_formal(ejercicio):
    """
    Usa Gemini para convertir el enunciado y/o imagen de un ejercicio 
    en una estructura JSON lógica (predicados) apta para motores simbólicos.
    """
    if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY no configurada.")
        return None

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = (
            f"Eres un experto en geometría formal. Tu tarea es traducir el siguiente ejercicio "
            f"a una representación estructurada JSON para un motor de razonamiento simbólico.\n\n"
            f"ENUNCIADO: {ejercicio.texto}\n"
            f"TEMA: {ejercicio.tema.nombre}\n\n"
            f"REGLAS:\n"
            f"1. Devuelve ÚNICAMENTE un objeto JSON.\n"
            f"2. Campos requeridos:\n"
            f"   - 'puntos': Lista de letras que representan puntos (ej. ['A', 'B', 'C']).\n"
            f"   - 'datos': Lista de predicados o ecuaciones (ej. ['Segment(A,B) = 10', 'IsParallel(L1, L2)', 'Angle(A,B,C) = 90']).\n"
            f"   - 'meta': Lo que se busca calcular (ej. 'Length(A,D)' o 'x').\n"
            f"   - 'teoremas_sugeridos': Lista de teoremas de secundaria aplicables (ej. ['SumaÁngulosInternos', 'Pitágoras', 'Tales']).\n"
            f"3. Si hay una imagen, analízala para extraer relaciones espaciales no mencionadas en el texto."
        )

        if ejercicio.imagen:
            try:
                img = Image.open(ejercicio.imagen.path)
                response = model.generate_content([prompt, img])
            except Exception as e:
                logger.error(f"Error procesando imagen: {e}")
                response = model.generate_content(prompt)
        else:
            response = model.generate_content(prompt)

        if not response or not response.text:
            return None

        # Limpiar respuesta (quitar bloques ```json)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return json.loads(text.strip())

    except Exception as e:
        logger.error(f"Error generando representación formal para ejercicio {ejercicio.id}: {e}")
        return None
