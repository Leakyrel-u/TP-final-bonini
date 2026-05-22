from PIL import Image, ImageEnhance
from .base import BaseTransform
from ..utils import validar_factor

class SaturationTransform(BaseTransform):
    """
    Transformación de ajuste de saturación (color/viveza).
    Modifica la viveza e intensidad de los colores utilizando ImageEnhance.Color.
    """

    def __init__(self, factor: float = 1.0):
        """
        Args:
            factor (float): Multiplicador de saturación (1.0 = sin cambios).
        """
        validar_factor(factor, 0.0, 3.0)
        self.factor = factor

    def apply(self, imagen: Image.Image) -> Image.Image:
        """
        Aplica la modificación de color/saturación.

        Args:
            imagen (Image.Image): Imagen a modificar.

        Returns:
            Image.Image: Nueva imagen con color/saturación ajustada.
        """
        realzador = ImageEnhance.Color(imagen)
        return realzador.enhance(self.factor)
