"""Módulo responsable de la carga y guardado de imágenes (disco local y nube)."""

from abc import ABC, abstractmethod
import io
from pathlib import Path
from typing import Union, Optional
import urllib.parse
import urllib.request
from PIL import Image
from .exceptions import (
    OptiLensError,
    ImagenNoEncontradaError,
    ImagenNoCargadaError,
    ParametroInvalidoError,
)
from .utils import crear_directorio

class CargadorImagen(ABC):
    """Clase base abstracta para la carga de imágenes."""

    @abstractmethod
    def cargar(self, origen: Union[str, Path]) -> Image.Image:
        """
        Carga una imagen desde el origen especificado.

        Args:
            origen (Union[str, Path]): Ruta local o URL de la imagen.

        Returns:
            Image.Image: Objeto de imagen PIL cargado en memoria.
        """
        pass

class CargadorLocal(CargadorImagen):
    """Cargador de imágenes desde el disco duro local."""

    def cargar(self, origen: Union[str, Path]) -> Image.Image:
        origen_str = str(origen)
        if "://" in origen_str or origen_str.startswith(("http://", "https://", "ftp://")):
            raise ParametroInvalidoError(f"La ruta local no puede ser una URL: {origen_str}")
        ruta = Path(origen)
        if not ruta.exists():
            raise ImagenNoEncontradaError(f"No se encontró el archivo: {origen}")
        
        try:
            with Image.open(ruta) as img:
                img.load()  # Fuerza la carga en memoria y cierra el archivo de inmediato
                return img
        except Exception as e:
            raise ImagenNoEncontradaError(f"Error al abrir la imagen local: {e}")

class CargadorUrl(CargadorImagen):
    """Cargador de imágenes desde una URL remota (HTTP/HTTPS)."""

    def cargar(self, origen: Union[str, Path]) -> Image.Image:
        url_str = str(origen)
        
        # Validar URL
        try:
            parsed = urllib.parse.urlparse(url_str)
            if not parsed.scheme or parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ParametroInvalidoError(f"URL de imagen inválida: {url_str}")
        except Exception as e:
            if isinstance(e, OptiLensError):
                raise
            raise ParametroInvalidoError(f"Error al parsear la URL '{url_str}': {e}")

        # Cargar desde la red de forma cross-platform
        try:
            req = urllib.request.Request(
                url_str,
                headers={"User-Agent": "OptiLens-Image-Loader/1.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                image_data = response.read()
            
            img = Image.open(io.BytesIO(image_data))
            img.load()  # Fuerza la carga en memoria
            return img
        except Exception as e:
            raise ImagenNoEncontradaError(f"Error al descargar la imagen desde la URL '{url_str}': {e}")

class GuardadorImagen(ABC):
    """Clase base abstracta para el guardado de imágenes."""

    @abstractmethod
    def validar(self, destino: Union[str, Path]) -> None:
        """
        Valida si el destino es correcto para este método de guardado.

        Args:
            destino (Union[str, Path]): Ruta de destino o URL.
        """
        pass

    @abstractmethod
    def guardar(
        self,
        imagen: Image.Image,
        destino: Union[str, Path],
        formato: str = "JPEG",
        **kwargs
    ) -> str:
        """
        Guarda la imagen en el destino especificado.

        Args:
            imagen (Image.Image): La imagen PIL a guardar.
            destino (Union[str, Path]): Ruta local o URL de destino.
            formato (str): Formato final (WEBP, JPEG, PNG, etc.).

        Returns:
            str: Ruta física o URL final donde se guardó.
        """
        pass

class GuardadorLocal(GuardadorImagen):
    """Guardador de imágenes en el disco duro local."""

    def validar(self, destino: Union[str, Path]) -> None:
        destino_str = str(destino)
        if "://" in destino_str or destino_str.startswith(("http://", "https://", "ftp://")):
            raise ParametroInvalidoError(f"La ruta local no puede ser una URL o contener un protocolo: {destino_str}")
        try:
            Path(destino)
        except Exception as e:
            raise ParametroInvalidoError(f"Ruta local inválida: {destino_str}. Error: {e}")

    def guardar(
        self,
        imagen: Image.Image,
        destino: Union[str, Path],
        formato: str = "JPEG",
        **kwargs
    ) -> str:
        if imagen is None:
            raise ImagenNoCargadaError("No hay imagen provista para guardar.")
        
        self.validar(destino)
        ruta_final = Path(destino)
        
        if ruta_final.parent:
            crear_directorio(ruta_final.parent)
            
        formato_upper = formato.upper()
        
        # Conversión de seguridad: JPEG no soporta canales alfa (RGBA/LA/P)
        imagen_guardar = imagen
        if formato_upper in ["JPEG", "JPG"] and imagen.mode in ("RGBA", "LA", "P"):
            imagen_guardar = imagen.convert("RGB")
            
        imagen_guardar.save(ruta_final, format=formato_upper, quality=90)
        return str(ruta_final.resolve())

class GuardadorNube(GuardadorImagen):
    """Guardador simulado de imágenes en la nube."""

    def validar(self, destino: Union[str, Path]) -> None:
        destino_str = str(destino)
        try:
            parsed = urllib.parse.urlparse(destino_str)
            if not parsed.scheme or parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ParametroInvalidoError(f"URL de destino en la nube inválida: {destino_str}")
        except Exception as e:
            if isinstance(e, OptiLensError):
                raise
            raise ParametroInvalidoError(f"Error al parsear la URL de la nube '{destino_str}': {e}")

    def guardar(
        self,
        imagen: Image.Image,
        destino: Union[str, Path],
        formato: str = "JPEG",
        **kwargs
    ) -> str:
        if imagen is None:
            raise ImagenNoCargadaError("No hay imagen provista para guardar.")
            
        destino_str = str(destino)
        self.validar(destino_str)
        
        # Simular serialización en el formato solicitado
        # Esto sirve para validar que el formato de imagen sea soportado por Pillow
        buf = io.BytesIO()
        formato_upper = formato.upper()
        
        imagen_guardar = imagen
        if formato_upper in ["JPEG", "JPG"] and imagen.mode in ("RGBA", "LA", "P"):
            imagen_guardar = imagen.convert("RGB")
            
        try:
            imagen_guardar.save(buf, format=formato_upper)
        except Exception as e:
            raise ParametroInvalidoError(f"Error al codificar imagen en formato '{formato_upper}': {e}")
            
        tamanio_bytes = len(buf.getvalue())
        print(f"[NUBE] Subiendo imagen procesada ({tamanio_bytes} bytes) a la nube en destino: {destino_str}")
        
        return destino_str

class ImageIO:
    """
    Clase responsable de aislar las operaciones de lectura y escritura.
    Mantiene compatibilidad con la firma estática original.
    """

    @staticmethod
    def cargar(ruta_acceso: Union[str, Path]) -> Image.Image:
        ruta_str = str(ruta_acceso)
        if ruta_str.startswith(("http://", "https://")):
            loader = CargadorUrl()
        else:
            loader = CargadorLocal()
        return loader.cargar(ruta_acceso)

    @staticmethod
    def guardar(
        imagen: Image.Image,
        carpeta_salida: Union[str, Path] = "procesadas",
        nombre: Optional[str] = None,
        formato: str = "JPEG",
        nombre_original: str = "imagen.jpg"
    ) -> Path:
        formato_upper = formato.upper()
        if nombre is None:
            nombre_base = Path(nombre_original).stem
            ext = "jpg" if formato_upper in ["JPEG", "JPG"] else formato_upper.lower()
            nombre = f"{nombre_base}_editada.{ext}"

        ruta_final = Path(carpeta_salida) / nombre
        
        saver = GuardadorLocal()
        saver.guardar(imagen, ruta_final, formato=formato)
        return ruta_final

