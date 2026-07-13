from abc import ABC, abstractmethod
from PIL import Image
import numpy as np

class BaseTransform(ABC):
    """Clase base abstracta para representar todas las operaciones de transformación de imágenes."""

    @abstractmethod
    def apply(self, imagen: Image.Image) -> Image.Image:
        """
        Aplica la transformación correspondiente a la imagen.
        Debe retornar una nueva imagen (no mutar la original en la medida de lo posible).

        Args:
            imagen (Image.Image): Imagen PIL sobre la cual aplicar la transformación.

        Returns:
            Image.Image: Nueva imagen PIL resultante del procesamiento.
        """
        pass

    @staticmethod
    def numpy_to_pil(array: np.ndarray) -> Image.Image:
        """Convierte numpy array a PIL Image"""
        # Asegurar valores en rango [0, 255]
        if array.dtype != np.uint8:
            array = np.clip(array, 0, 255).astype(np.uint8)
        return Image.fromarray(array)