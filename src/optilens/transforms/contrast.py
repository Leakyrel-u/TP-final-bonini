from PIL import Image, ImageEnhance
from .base import BaseTransform
from ..utils import validar_factor

class ContrastTransform(BaseTransform):
    """
    Transformación de ajuste de contraste lineal.
    Modifica la diferencia tonal entre los elementos más oscuros y más claros.
    """

    def __init__(self, factor: float = 1.0):
        """
        Args:
            factor (float): Multiplicador de contraste (1.0 = sin cambios).
        """
        validar_factor(factor, 0.0, 3.0)
        self.factor = factor

    def apply(self, imagen: Image.Image) -> Image.Image:
        """
        Aplica el realce de contraste.

        Args:
            imagen (Image.Image): Imagen a modificar.

        Returns:
            Image.Image: Nueva imagen con contraste ajustado.
        """
        realzador = ImageEnhance.Contrast(imagen)
        return realzador.enhance(self.factor)
