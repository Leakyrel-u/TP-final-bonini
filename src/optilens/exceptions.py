"""Excepciones personalizadas"""

# Este bloque define una jerarquía de excepciones personalizadas estructurada a partir de una
# clase base común denominada.
# Su objetivo es centralizar y tipificar los errores específicos del sistema, 
# permitiendo interceptar de forma clara fallos críticos como rutas de archivos inexistentes,
#  omisiones en la carga de datos o valores de configuración fuera de rango.
# Al heredar directamente de Exception, proporciona al desarrollador un control preciso 
# y semántico para capturar anomalías operativas de manera independiente y limpia.

class OptiLensError(Exception):
    """Excepción base para OptiLens"""
    pass

class ImagenNoEncontradaError(OptiLensError):
    """Se lanza cuando no se encuentra la imagen"""
    pass

class ImagenNoCargadaError(OptiLensError):
    """Se lanza cuando se intenta procesar sin imagen cargada"""
    pass

class ParametroInvalidoError(OptiLensError):
    """Se lanza cuando un parámetro es inválido"""
    pass