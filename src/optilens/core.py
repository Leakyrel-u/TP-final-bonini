"""Clase principal de procesamiento (Fachada y Orquestador de Pipeline)"""

import logging
from pathlib import Path
from typing import Union, Optional, List
from PIL import Image

from .exceptions import ImagenNoCargadaError
from .io import ImageIO
from .transforms.base import BaseTransform
from .transforms.resize import ResizeTransform
from .transforms.brightness import BrightnessTransform
from .transforms.contrast import ContrastTransform
from .transforms.saturation import SaturationTransform
from .transforms.watermark import WatermarkTransform
from .transforms.threshold import ThresholdTransform

logger = logging.getLogger(__name__)

class ProcesadorImagen:
    """
    Procesador de imágenes con capacidades de redimensionamiento,
    ajuste de brillo/contraste, marca de agua y binarización.
    
    Funciona como una Fachada (Facade Pattern) que mantiene una interfaz fluida e intuitiva,
    y como un Orquestador que delega las operaciones a clases de transformación específicas y modulares.
    """
    
    def __init__(self, verbose: bool = True):
        """
        Args:
            verbose (bool): Si True, imprime mensajes de progreso en la consola.
        """
        self.imagen_original: Optional[Image.Image] = None
        self.imagen_procesada: Optional[Image.Image] = None
        self.nombre_archivo: str = ""
        self.verbose: bool = verbose
        self._pipeline: List[BaseTransform] = []

    """
    Este método funciona como un sistema de registro interno (o logger) encargado de 
    centralizar y canalizar los mensajes informativos generados durante el ciclo de 
    ejecución de la clase. Al recibir un mensaje, el método evalúa primero la bandera 
    condicional self.verbose; si esta se encuentra activa (True), imprime el texto de manera 
    inmediata en la consola o terminal estándar para ofrecer retroalimentación en tiempo real al usuario.
    """   
    def _log(self, mensaje: str) -> None:
        """Logger interno de ejecución."""
        if self.verbose:
            try:
                print(mensaje)
            except UnicodeEncodeError:
                # Fallback seguro para consolas que no soportan codificación de emojis (ej. CP1252 en Windows)
                mensaje_seguro = mensaje.replace("✅", "[OK]").replace("💾", "[GUARDADO]").replace("🔄", "[RESETEADO]").replace("->", "->")
                try:
                    print(mensaje_seguro)
                except UnicodeEncodeError:
                    print(mensaje_seguro.encode('ascii', errors='replace').decode('ascii'))
        logger.info(mensaje)
    
    def _verificar_imagen_cargada(self) -> None:
        """Verifica que haya una imagen cargada antes de realizar cualquier operación."""
        if self.imagen_procesada is None:
            raise ImagenNoCargadaError(
                "No hay imagen cargada. Usa cargar_imagen() primero."
            )
    
    def cargar_imagen(self, ruta_acceso: Union[str, Path]) -> "ProcesadorImagen":
        """
        Carga una imagen desde el sistema de archivos de forma no destructiva.
        
        Args:
            ruta_acceso (Union[str, Path]): Ruta al archivo de imagen.
            
        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
            
        Raises:
            ImagenNoEncontradaError: Si la ruta no existe o es ilegible.
        """
        self.imagen_original = ImageIO.cargar(ruta_acceso)
        self.imagen_procesada = self.imagen_original.copy()  # Realiza copia no destructiva
        self.nombre_archivo = Path(ruta_acceso).name
        self._pipeline.clear()
        self._log(f"✅ Imagen '{self.nombre_archivo}' cargada con éxito.")
        return self

    def aplicar_transformacion(self, transformacion: BaseTransform) -> "ProcesadorImagen":
        """
        Aplica una transformación modular sobre la imagen cargada y la registra en el historial del pipeline.
        Permite extender la funcionalidad inyectando transformaciones personalizadas externas (Principio Open/Closed).

        Args:
            transformacion (BaseTransform): Instancia de una clase de transformación.

        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        self._verificar_imagen_cargada()
        assert self.imagen_procesada is not None  # type safety para linters
        
        self.imagen_procesada = transformacion.apply(self.imagen_procesada)
        self._pipeline.append(transformacion)
        return self
    
    # --- API Fluido / Métodos de Fachada de Compatibilidad ---
    
    def redimensionar(self, ancho: int = 400, alto: int = 400) -> "ProcesadorImagen":
        """
        Redimensiona la imagen manteniendo proporciones.
        
        Args:
            ancho (int): Ancho objetivo en píxeles.
            alto (int): Alto objetivo en píxeles.
            
        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        self._log(f"   -> Redimensionado: {ancho}x{alto}")
        return self.aplicar_transformacion(ResizeTransform(ancho, alto))
    
    def ajustar_brillo(self, factor: float = 1.0) -> "ProcesadorImagen":
        """
        Ajusta el brillo de la imagen.
        
        Args:
            factor (float): Multiplicador (1.0 = sin cambios, 1.5 = +50%, 0.5 = -50%).
            
        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        self._log(f"   -> Brillo ajustado: x{factor}")
        return self.aplicar_transformacion(BrightnessTransform(factor))
    
    def ajustar_contraste(self, factor: float = 1.0) -> "ProcesadorImagen":
        """
        Ajusta el contraste de la imagen.
        
        Args:
            factor (float): Multiplicador (1.0 = sin cambios).
            
        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        self._log(f"   -> Contraste ajustado: x{factor}")
        return self.aplicar_transformacion(ContrastTransform(factor))
    
    def aplicar_marca_agua(self, ruta_logo: Union[str, Path], opacidad: float = 0.5, escala: float = 0.25) -> "ProcesadorImagen":
        """
        Aplica una marca de agua en la esquina inferior derecha.
        
        Args:
            ruta_logo (Union[str, Path]): Ruta al logotipo.
            opacidad (float): Transparencia (0.0 = invisible, 1.0 = opaco).
            escala (float): Tamaño relativo al ancho de la imagen (0.25 = 25%).
            
        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        self._log("   -> Marca de agua aplicada")
        return self.aplicar_transformacion(WatermarkTransform(ruta_logo, opacidad, escala))
    
    # Contraste y Saturación: Generar una versión de alto contraste
    # y una de alta saturación de la misma imagen. 
    # Objetivo: distinguir la diferencia entre modificar la 
    # diferencia tonal vs. la viveza del color.
    # Métodos: ImageEnhance.Contrast, ImageEnhance.Color

    def contraste(self, valor_contraste: float) -> "ProcesadorImagen":
        """
        Ajusta el contraste de la imagen (alias y compatibilidad).

        Args:
            valor_contraste (float): Factor de contraste.

        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        return self.ajustar_contraste(valor_contraste)

    def saturacion(self, valor_saturacion: float) -> "ProcesadorImagen":
        """
        Ajusta la saturación de color de la imagen.

        Args:
            valor_saturacion (float): Factor de saturación.

        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        self._log(f"   -> Saturación ajustada: x{valor_saturacion}")
        return self.aplicar_transformacion(SaturationTransform(valor_saturacion))
    
    def umbralizacion(self, valor_umbral: int) -> "ProcesadorImagen":
        """
        Binariza la imagen evaluando cada píxel con una función lambda que asigna blanco (255)
        si supera el valor umbral o negro (0) en caso contrario. 

        Args:
            valor_umbral (int): Límite de binarización entre 0 y 255.

        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        self._log(f"   -> Umbralización aplicada: {valor_umbral}")
        return self.aplicar_transformacion(ThresholdTransform(valor_umbral))
    
    def guardar_resultado(self, carpeta_salida: Union[str, Path] = "procesadas", nombre: Optional[str] = None, formato: str = "JPEG") -> str:
        """
        Guarda la imagen procesada en disco.
        
        Args:
            carpeta_salida (Union[str, Path]): Directorio de destino.
            nombre (Optional[str]): Nombre de archivo final personalizado.
            formato (str): Formato del archivo resultante (WEBP, JPEG, PNG).

        Returns:
            str: Ruta final del archivo guardado.
        """
        self._verificar_imagen_cargada()
        assert self.imagen_procesada is not None  # type safety
        
        ruta_final = ImageIO.guardar(
            self.imagen_procesada,
            carpeta_salida=carpeta_salida,
            nombre=nombre,
            formato=formato,
            nombre_original=self.nombre_archivo
        )
        self._log(f"💾 Guardado en: {ruta_final}")
        return str(ruta_final)
    
    def resetear(self) -> "ProcesadorImagen":
        """
        Restaura la imagen procesada al estado original cargado.
        
        Returns:
            ProcesadorImagen: La propia instancia para encadenamiento.
        """
        if self.imagen_original:
            self.imagen_procesada = self.imagen_original.copy()
            self._pipeline.clear()
            self._log("🔄 Imagen restaurada al original")
        return self