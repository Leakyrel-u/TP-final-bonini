from abc import ABC, abstractmethod
from PIL import Image
import numpy as np
import cv2

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
    def pil_to_numpy(image: Image.Image) -> np.ndarray:
        """Convierte PIL Image a numpy array RGB"""
        return np.array(image.convert('RGB'))

    @staticmethod
    def pil_to_cv2(image: Image.Image) -> np.ndarray:
        """Convierte PIL Image a formato OpenCV (BGR)"""
        rgb = np.array(image.convert('RGB'))
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    @staticmethod
    def numpy_to_pil(array: np.ndarray) -> Image.Image:
        """Convierte numpy array a PIL Image"""
        # Asegurar valores en rango [0, 255]
        if array.dtype != np.uint8:
            array = np.clip(array, 0, 255).astype(np.uint8)
        return Image.fromarray(array)
    
    @staticmethod
    def cv2_to_pil(array: np.ndarray) -> Image.Image:
        """Convierte imagen OpenCV (BGR) a PIL Image (RGB)"""
        if len(array.shape) == 2:  # Grayscale
            return Image.fromarray(array)
        rgb = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)