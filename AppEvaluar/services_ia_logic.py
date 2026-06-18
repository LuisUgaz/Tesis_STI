from google import genai
from google.genai import types
import os
import json
import logging
from django.conf import settings
import base64
from pydantic import BaseModel, Field
from typing import List

logger = logging.getLogger(__name__)

class RepresentacionFormalSchema(BaseModel):
    puntos: List[str] = Field(description="Lista de puntos geométricos identificados en el ejercicio, por ejemplo: ['A', 'B', 'C']")
    datos: List[str] = Field(description="Lista de datos geométricos o ecuaciones numéricas dadas en el enunciado")
    meta: str = Field(description="La incógnita, valor o propiedad que se busca calcular o demostrar")
    teoremas_sugeridos: List[str] = Field(description="Lista de teoremas geométricos sugeridos para resolver el problema")

def generar_representacion_formal(ejercicio):
    """
    Usa el SDK moderno 'google-genai' (2026) con Structured Outputs (response_schema)
    para convertir el enunciado en una estructura JSON lógica perfecta y sin errores de parseo.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        logger.error("GEMINI_API_KEY no configurada.")
        return None

    try:
        client = genai.Client(api_key=api_key)

        prompt = (
            f"Eres un experto en geometría formal. Tu tarea es traducir el siguiente ejercicio "
            f"a una representación estructurada JSON para un motor de razonamiento simbólico.\n\n"
            f"ENUNCIADO: {ejercicio.texto}\n"
            f"TEMA: {ejercicio.tema.nombre}\n\n"
            f"REGLAS:\n"
            f"1. Devuelve ÚNICAMENTE la estructura JSON requerida.\n"
            f"2. Si hay una imagen, analízala para extraer relaciones espaciales."
        )

        contents = [prompt]

        if ejercicio.imagen:
            try:
                with open(ejercicio.imagen.path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                    contents.append(types.Part.from_bytes(
                        data=base64.b64decode(image_data),
                        mime_type="image/png"
                    ))
            except Exception as e:
                logger.error(f"Error procesando imagen para SDK: {e}")

        # Usar gemini-2.5-flash ya que está disponible y soporta Structured Outputs de forma nativa
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RepresentacionFormalSchema,
            temperature=0.1
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=config
        )

        if response and response.text:
            return json.loads(response.text.strip())

        return None

    except Exception as e:
        logger.error(f"Error en enriquecimiento IA (SDK 2026) para ID {ejercicio.id}: {e}")
        return None
