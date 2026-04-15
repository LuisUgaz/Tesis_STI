import pdfplumber
from docx import Document
import google.generativeai as genai
import json
import os
from django.conf import settings

def extraer_texto_pdf(file):
    texto = ""
    try:
        with pdfplumber.open(file) as pdf:
            for pagina in pdf.pages:
                texto += pagina.extract_text() or ""
    except Exception as e:
        print(f"Error extrayendo PDF: {e}")
    return texto

def extraer_texto_docx(file):
    texto = ""
    try:
        doc = Document(file)
        texto = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Error extrayendo DOCX: {e}")
    return texto

def analizar_preguntas_con_gemini(texto, api_key=None):
    # Intentar obtener API Key de settings si no se provee
    api_key = api_key or getattr(settings, 'GEMINI_API_KEY', None)
    
    if not api_key:
        return {"error": "API Key de Gemini no configurada. Por favor, confígurala en los ajustes del sistema."}
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Analiza el siguiente texto de un banco de preguntas de geometría y extráelas en un formato JSON estructurado.
    
    Para cada pregunta identifica:
    1. El enunciado (texto).
    2. Las opciones (lista de strings).
    3. Cuál es la opción correcta (el texto exacto de la opción).
    4. El tema sugerido (debe ser uno de estos: 'Ángulos', 'Triángulos', 'Segmentos'). Si no encaja, usa el más cercano.
    5. La dificultad (Básico, Intermedio, Avanzado).
    6. Una explicación técnica breve (opcional).

    Texto del documento:
    {texto}

    REGLAS CRÍTICAS:
    - Devuelve ÚNICAMENTE un objeto JSON válido.
    - No incluyas explicaciones fuera del JSON.
    - Asegúrate de que la 'correcta' esté incluida exactamente igual en la lista de 'opciones'.
    - Si el texto no contiene preguntas claras, devuelve una lista vacía.

    Esquema esperado:
    {{
      "preguntas": [
        {{
          "enunciado": "Enunciado de la pregunta",
          "opciones": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
          "correcta": "Opción 2",
          "tema": "Triángulos",
          "dificultad": "Básico",
          "explicacion": "Explicación breve"
        }}
      ]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text_response = response.text
        # Limpiar posibles delimitadores de markdown
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0]
            
        return json.loads(text_response.strip())
    except Exception as e:
        return {"error": f"Error al procesar con IA: {str(e)}"}
