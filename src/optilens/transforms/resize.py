from PIL import Image, ImageOps
from .base import BaseTransform

class ResizeTransform(BaseTransform):
    """
    Transformación de redimensionado avanzado de imagen.
    Modifica las dimensiones geométricas de la imagen recortándola hacia el centro para encajar de forma exacta
    en el aspecto deseado, utilizando el filtro LANCZOS para reducir el serrucho (aliasing).
    """

    def __init__(self, ancho: int = 400, alto: int = 400):
        """
        Args:
            ancho (int): Ancho objetivo en píxeles.
            alto (int): Alto objetivo en píxeles.
        """
        if ancho <= 0 or alto <= 0:
            raise ValueError("El ancho y alto deben ser números mayores que cero.")
        self.ancho = ancho
        self.alto = alto

    def apply(self, imagen: Image.Image) -> Image.Image:
        """
        Aplica redimensionamiento geométrico recortado.
        
        Args:
            imagen (Image.Image): Imagen de entrada.
            
        Returns:
            Image.Image: Imagen redimensionada.
        """
        return ImageOps.fit(
            imagen, 
            (self.ancho, self.alto), 
            Image.Resampling.LANCZOS
        )
