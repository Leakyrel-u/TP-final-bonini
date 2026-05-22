from PIL import Image
from .base import BaseTransform

class ThresholdTransform(BaseTransform):
    """
    Transformación de umbralización selectiva (Binarización).
    Binariza la imagen evaluando cada píxel con una función lambda que asigna blanco (255)
    si supera el valor umbral o negro (0) en caso contrario, compactando el resultado en 1-bit.
    """

    def __init__(self, valor_umbral: int = 127):
        """
        Args:
            valor_umbral (int): Valor límite de corte entre 0 y 255.
        """
        if not (0 <= valor_umbral <= 255):
            raise ValueError(f"El valor de umbral debe estar en el rango [0, 255], recibido: {valor_umbral}")
        self.valor_umbral = valor_umbral

    def apply(self, imagen: Image.Image) -> Image.Image:
        """
        Binariza la imagen usando el umbral establecido.

        Args:
            imagen (Image.Image): Imagen a binarizar.

        Returns:
            Image.Image: Nueva imagen binarizada en formato de 1 bit (blanco y negro puro).
        """
        # Convertir a escala de grises para aplicar binarización de luminancia
        imagen_gris = imagen.convert("L")
        
        # Binariza evaluando cada píxel con una función lambda
        imagen_procesada = imagen_gris.point(lambda x: 255 if x > self.valor_umbral else 0)
        
        # El paso final .convert('1') simplemente compacta esa información al formato de 1 bit (blanco/negro puro)
        return imagen_procesada.convert("1")
