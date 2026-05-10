"""Excepciones personalizadas"""

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