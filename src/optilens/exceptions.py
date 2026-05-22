"""Excepciones personalizadas"""

# Este bloque define una jerarquía de excepciones personalizadas estructurada a partir de una
# clase base común denominada.
# Su objetivo es centralizar y tipificar los errores específicos del sistema, 
# permitiendo interceptar de forma clara fallos críticos como rutas de archivos inexistentes,
# omisiones en la carga de datos o valores de configuración fuera de rango.
# Al heredar directamente de Exception, proporciona al desarrollador un control preciso 
# y semántico para capturar anomalías operativas de manera independiente y limpia.

class OptiLensError(Exception):
    """Excepción base para todos los errores de la librería OptiLens."""
    pass

class ImagenNoEncontradaError(OptiLensError):
    """Se lanza cuando no se encuentra una imagen o logotipo en la ruta especificada."""
    pass

class ImagenNoCargadaError(OptiLensError):
    """Se lanza cuando se intenta realizar un procesamiento sin haber cargado una imagen previamente."""
    pass

class ParametroInvalidoError(OptiLensError):
    """Se lanza cuando un parámetro de transformación (como el factor de brillo, contraste o escala) está fuera de los rangos válidos."""
    pass