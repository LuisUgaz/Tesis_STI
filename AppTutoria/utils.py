import re

def extraer_youtube_id(url):
    """
    Extrae el ID de un video de YouTube a partir de su URL.
    Soportar formatos: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID
    """
    if not url:
        return None
        
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def generar_youtube_thumbnail(url):
    """
    Genera la URL de la miniatura de alta calidad para un video de YouTube.
    """
    video_id = extraer_youtube_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    return None
