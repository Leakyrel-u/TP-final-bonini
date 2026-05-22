from pathlib import Path
from typing import Union
from PIL import Image, ImageEnhance
from .base import BaseTransform
from ..utils import validar_ruta, validar_factor
from ..exceptions import ImagenNoEncontradaError

class WatermarkTransform(BaseTransform):
    """
    Transformación de composición de marca de agua alfa (Alpha Blending).
    Superpone un logotipo con transparencia matemática (RGBA) en la esquina inferior derecha.
    """

    def __init__(self, ruta_logo: Union[str, Path], opacidad: float = 0.5, escala: float = 0.25):
        """
        Args:
            ruta_logo (Union[str, Path]): Ruta al archivo del logotipo.
            opacidad (float): Transparencia de la marca (0.0 = invisible, 1.0 = opaco).
            escala (float): Relación de tamaño de la marca respecto al ancho de la imagen (de 0.05 a 0.5).
        """
        if not validar_ruta(ruta_logo):
            raise ImagenNoEncontradaError(f"Logo no encontrado en: {ruta_logo}")
        
        validar_factor(opacidad, 0.0, 1.0)
        validar_factor(escala, 0.05, 0.5)

        self.ruta_logo = Path(ruta_logo)
        self.opacidad = opacidad
        self.escala = escala

    def apply(self, imagen: Image.Image) -> Image.Image:
        """
        Superpone la marca de agua en una copia de la imagen.

        Args:
            imagen (Image.Image): Imagen base.

        Returns:
            Image.Image: Nueva imagen con la marca de agua aplicada.
        """
        # Asegurar espacio de color RGBA
        imagen_rgba = imagen if imagen.mode == "RGBA" else imagen.convert("RGBA")

        with Image.open(self.ruta_logo) as logo:
            # Calcular dimensiones proporcionales
            ancho_logo = int(imagen_rgba.width * self.escala)
            alto_logo = int(logo.height * (ancho_logo / logo.width))
            logo_resized = logo.resize((ancho_logo, alto_logo), Image.Resampling.LANCZOS)

            # Aplicar opacidad
            if logo_resized.mode != "RGBA":
                logo_resized = logo_resized.convert("RGBA")

            alpha = logo_resized.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(self.opacidad)
            logo_resized.putalpha(alpha)

            # Posicionar en esquina inferior derecha con un margen de 20 píxeles
            pos_x = imagen_rgba.width - ancho_logo - 20
            pos_y = imagen_rgba.height - alto_logo - 20

            # Realizar mezcla de canales (Paste) sin alterar la imagen original
            resultado = imagen_rgba.copy()
            resultado.paste(logo_resized, (pos_x, pos_y), logo_resized)

            # Devolver en el formato original si no era RGBA (ej. RGB, L)
            if imagen.mode != "RGBA":
                return resultado.convert(imagen.mode)
            
            return resultado
