"""
OptiLens - Librería de procesamiento digital de imágenes
"""

__version__ = "0.1.0"

from .core import ProcesadorImagen
from .io import ImageIO
from .exceptions import (
    OptiLensError,
    ImagenNoEncontradaError,
    ImagenNoCargadaError,
    ParametroInvalidoError,
)
from .transforms import (
    BaseTransform,
    ResizeTransform,
    BrightnessTransform,
    ContrastTransform,
    SaturationTransform,
    WatermarkTransform,
    ThresholdTransform,
)

__all__ = [
    "ProcesadorImagen",
    "ImageIO",
    "OptiLensError",
    "ImagenNoEncontradaError",
    "ImagenNoCargadaError",
    "ParametroInvalidoError",
    "BaseTransform",
    "ResizeTransform",
    "BrightnessTransform",
    "ContrastTransform",
    "SaturationTransform",
    "WatermarkTransform",
    "ThresholdTransform",
]