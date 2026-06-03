"""
OptiLens - Librería de procesamiento digital de imágenes
"""

__version__ = "0.1.0"

from .core import ProcesadorImagen
from .io import (
    ImageIO,
    CargadorImagen,
    CargadorLocal,
    CargadorUrl,
    GuardadorImagen,
    GuardadorLocal,
    GuardadorNube,
)
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
    WienerRestorationTransform
)

__all__ = [
    "ProcesadorImagen",
    "ImageIO",
    "CargadorImagen",
    "CargadorLocal",
    "CargadorUrl",
    "GuardadorImagen",
    "GuardadorLocal",
    "GuardadorNube",
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
    "WienerRestorationTransform"
]
