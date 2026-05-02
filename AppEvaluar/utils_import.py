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
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    Extrae TODAS las preguntas de geometría del siguiente texto en un JSON estructurado.
    
    Campos por pregunta:
    - enunciado: Texto de la pregunta.
    - opciones: Lista de strings con las alternativas.
    - correcta: Texto exacto de la opción correcta.
    - tema: Elegir entre 'Ángulos', 'Triángulos', 'Segmentos'.
    - dificultad: Básico, Intermedio o Avanzado.

    Texto:
    {texto}

    REGLAS:
    - Devuelve ÚNICAMENTE el JSON. Sin introducciones ni explicaciones.
    - No inventes preguntas, extrae solo las presentes.
    - Formato: {{"preguntas": [{{...}}, {{...}}]}}
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
