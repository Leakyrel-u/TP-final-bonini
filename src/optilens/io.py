"""Módulo responsable de la carga y guardado de imágenes en disco."""

from pathlib import Path
from typing import Union, Optional
from PIL import Image
from .exceptions import ImagenNoEncontradaError, ImagenNoCargadaError
from .utils import crear_directorio

class ImageIO:
    """Clase responsable de aislar las operaciones de lectura y escritura en el sistema de archivos."""

    @staticmethod
    def cargar(ruta_acceso: Union[str, Path]) -> Image.Image:
        """
        Carga una imagen desde el disco de manera segura.
        Carga explícitamente los píxeles en memoria para evitar descriptores de archivo abiertos.

        Args:
            ruta_acceso (Union[str, Path]): Ruta del archivo de imagen.

        Returns:
            Image.Image: Objeto de imagen PIL.

        Raises:
            ImagenNoEncontradaError: Si el archivo no existe o no se puede procesar.
        """
        ruta = Path(ruta_acceso)
        if not ruta.exists():
            raise ImagenNoEncontradaError(f"No se encontró el archivo: {ruta_acceso}")
        
        try:
            with Image.open(ruta) as img:
                img.load()  # Fuerza la carga en memoria y cierra el archivo de inmediato
                return img
        except Exception as e:
            raise ImagenNoEncontradaError(f"Error al abrir la imagen: {e}")

    @staticmethod
    def guardar(
        imagen: Image.Image,
        carpeta_salida: Union[str, Path] = "procesadas",
        nombre: Optional[str] = None,
        formato: str = "JPEG",
        nombre_original: str = "imagen.jpg"
    ) -> Path:
        """
        Guarda una imagen en disco bajo el formato y nombre especificados.
        Realiza conversiones automáticas de canales de color si el formato de destino no lo soporta (ej. JPEG no soporta canales alfa).

        Args:
            imagen (Image.Image): La imagen PIL a guardar.
            carpeta_salida (Union[str, Path]): Carpeta donde guardar el archivo.
            nombre (Optional[str]): Nombre de archivo final. Si es None, se autogenera basándose en nombre_original.
            formato (str): Formato del archivo resultante (WEBP, JPEG, PNG).
            nombre_original (str): Nombre de la imagen original para la autogeneración.

        Returns:
            Path: Ruta absoluta o relativa final de la imagen guardada.

        Raises:
            ImagenNoCargadaError: Si la imagen recibida es None o no válida.
        """
        if imagen is None:
            raise ImagenNoCargadaError("No hay imagen provista para guardar.")

        crear_directorio(carpeta_salida)
        formato_upper = formato.upper()

        if nombre is None:
            nombre_base = Path(nombre_original).stem
            ext = "jpg" if formato_upper in ["JPEG", "JPG"] else formato_upper.lower()
            nombre = f"{nombre_base}_editada.{ext}"

        ruta_final = Path(carpeta_salida) / nombre

        # Conversión de seguridad: JPEG no soporta modos de imagen con transparencia (ej. RGBA, P, LA)
        imagen_guardar = imagen
        if formato_upper in ["JPEG", "JPG"] and imagen.mode in ("RGBA", "LA", "P"):
            imagen_guardar = imagen.convert("RGB")

        imagen_guardar.save(ruta_final, format=formato_upper, quality=90)
        return ruta_final
