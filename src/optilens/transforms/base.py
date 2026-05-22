from abc import ABC, abstractmethod
from PIL import Image

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
