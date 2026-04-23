import math

class GeometryValidator:
    @staticmethod
    def calcular_distancia(p1, p2):
        """Calcula la distancia euclidiana entre dos puntos."""
        return math.hypot(p2['x'] - p1['x'], p2['y'] - p1['y'])

    @staticmethod
    def calcular_angulo(p1, p2, p3):
        """
        Calcula el ángulo en el punto p2 formado por los puntos p1, p2, p3.
        Retorna el ángulo en grados (0-180).
        """
        # Vectores p2->p1 y p2->p3
        v1 = (p1['x'] - p2['x'], p1['y'] - p2['y'])
        v2 = (p3['x'] - p2['x'], p3['y'] - p2['y'])

        # Ángulos polares
        ang1 = math.atan2(v1[1], v1[0])
        ang2 = math.atan2(v2[1], v2[0])

        diff = math.degrees(ang1 - ang2)
        # Normalizar a un ángulo positivo menor que 180
        diff = abs(diff)
        if diff > 180:
            diff = 360 - diff
        
        return diff

    @classmethod
    def validar_angulo(cls, datos, meta):
        """
        Valida un ángulo construido. 
        Requiere que 'puntos' contenga al menos 3 puntos. 
        Se asume un orden específico o se puede mejorar para buscar el ángulo objetivo.
        """
        puntos = list(datos['puntos'].values())
        if len(puntos) < 3:
            return False, 999
        
        # En esta versión inicial, calculamos el ángulo formado por los 3 primeros puntos recibidos
        # Siendo el segundo punto el vértice (B en el test).
        p1, p2, p3 = puntos[0], puntos[1], puntos[2]
        angulo_calculado = cls.calcular_angulo(p1, p2, p3)
        
        error = abs(angulo_calculado - meta['objetivo'])
        es_valido = error <= meta['tolerancia']
        
        return es_valido, error

    @classmethod
    def validar_distancia(cls, datos, meta):
        """Valida la distancia entre los dos primeros puntos recibidos."""
        puntos = list(datos['puntos'].values())
        if len(puntos) < 2:
            return False, 999
        
        dist_calculada = cls.calcular_distancia(puntos[0], puntos[1])
        error = abs(dist_calculada - meta['objetivo'])
        es_valido = error <= meta['tolerancia']
        
        return es_valido, error
