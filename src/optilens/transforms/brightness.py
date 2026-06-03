from PIL import Image, ImageEnhance
from .base import BaseTransform
from ..utils import validar_factor

class BrightnessTransform(BaseTransform):
    """
    Transformación de ajuste de brillo lineal.
    Realza o disminuye la luminancia general de los píxeles multiplicándolos por un factor.
    """

    def __init__(self, factor: float = 1.0):
        """
        Args:
            factor (float): Multiplicador (1.0 = sin cambios, 1.5 = +50%, 0.5 = -50%).
        """
        validar_factor(factor, 0.0, 3.0)
        self.factor = factor

    def apply(self, imagen: Image.Image) -> Image.Image:
        """
        Aplica el realce de brillo.

        Args:
            imagen (Image.Image): Imagen a modificar.

        Returns:
            Image.Image: Nueva imagen con brillo ajustado.
        """
        original_mode = imagen.mode
        if original_mode == "1":
            imagen = imagen.convert("L")

        realzador = ImageEnhance.Brightness(imagen)
        resultado = realzador.enhance(self.factor)

        if original_mode == "1":
            resultado = resultado.convert("1")
        return resultado
