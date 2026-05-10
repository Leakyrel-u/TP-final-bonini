"""
OptiLens - Librería de procesamiento de imágenes
"""

__version__ = "0.1.0"

from .core import ProcesadorImagen
from .exceptions import ImagenNoEncontradaError, ImagenNoCargadaError

__all__ = [
    "ProcesadorImagen",
    "ImagenNoEncontradaError", 
    "ImagenNoCargadaError"
]