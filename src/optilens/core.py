"""Clase principal de procesamiento"""

from PIL import Image, ImageEnhance, ImageOps
from pathlib import Path
import logging

from .exceptions import ImagenNoEncontradaError, ImagenNoCargadaError
from .utils import validar_ruta, validar_factor, crear_directorio

logger = logging.getLogger(__name__)

class ProcesadorImagen:
    """
    Procesador de imágenes con capacidades de redimensionamiento,
    ajuste de brillo/contraste y marca de agua.

    """
    
    def __init__(self, verbose=True):
        """
        Args:
            verbose (bool): Si True, imprime mensajes en consola
        """
        self.imagen_original = None
        self.imagen_procesada = None
        self.nombre_archivo = ""
        self.verbose = verbose
    """
    Este método funciona como un sistema de registro interno (o logger) encargado de 
    centralizar y canalizar los mensajes informativos generados durante el ciclo de 
    ejecución de la clase. Al recibir un mensaje, el método evalúa primero la bandera 
    condicional self.verbose; si esta se encuentra activa (True), imprime el texto de manera 
    inmediata en la consola o terminal estándar para ofrecer retroalimentación en tiempo real al usuario
    """   
    def _log(self, mensaje):
        """Logger interno"""
        if self.verbose:
            print(mensaje)
        logger.info(mensaje)

    
    
    def _verificar_imagen_cargada(self):
        """Verifica que haya una imagen cargada"""
        if self.imagen_procesada is None:
            raise ImagenNoCargadaError(
                "No hay imagen cargada. Usa cargar_imagen() primero."
            )
    
    def cargar_imagen(self, ruta_acceso):
        """
        Carga una imagen desde el sistema de archivos.
        
        Args:
            ruta_acceso (str): Ruta al archivo de imagen
            
        Raises:
            ImagenNoEncontradaError: Si la ruta no existe
        """
        ruta = Path(ruta_acceso)
        
        if not ruta.exists():
            raise ImagenNoEncontradaError(f"No se encontró: {ruta_acceso}")
        
        try:
            self.imagen_original = Image.open(ruta)
            self.imagen_procesada = self.imagen_original.copy() # Realiza copia
            self.nombre_archivo = ruta.name
            self._log(f"✅ Imagen '{self.nombre_archivo}' cargada con éxito.")
        except Exception as e:
            raise ImagenNoEncontradaError(f"Error al abrir imagen: {e}")
    
    def redimensionar(self, ancho=400, alto=400):
        """
        Redimensiona la imagen manteniendo proporciones.
        
        Args:
            ancho (int): Ancho objetivo en píxeles
            alto (int): Alto objetivo en píxeles
        """
        self._verificar_imagen_cargada()
        
        self.imagen_procesada = ImageOps.fit(
            self.imagen_procesada, 
            (ancho, alto), 
            Image.Resampling.LANCZOS
        )
        self._log(f"   -> Redimensionado: {ancho}x{alto}")
        return self  # Para encadenar métodos
    
    def ajustar_brillo(self, factor=1.0):
        """
        Ajusta el brillo de la imagen.
        
        Args:
            factor (float): Multiplicador (1.0 = sin cambios, 1.5 = +50%, 0.5 = -50%)
        """
        self._verificar_imagen_cargada()
        validar_factor(factor, 0.0, 3.0)
        
        realzador = ImageEnhance.Brightness(self.imagen_procesada)
        self.imagen_procesada = realzador.enhance(factor)
        self._log(f"   -> Brillo ajustado: x{factor}")
        return self
    
    def ajustar_contraste(self, factor=1.0):
        """
        Ajusta el contraste de la imagen.
        
        Args:
            factor (float): Multiplicador (1.0 = sin cambios)
        """
        self._verificar_imagen_cargada()
        validar_factor(factor, 0.0, 3.0)
        
        realzador = ImageEnhance.Contrast(self.imagen_procesada)
        self.imagen_procesada = realzador.enhance(factor)
        self._log(f"   -> Contraste ajustado: x{factor}")
        return self
    
    def aplicar_marca_agua(self, ruta_logo, opacidad=0.5, escala=0.25):
        """
        Aplica una marca de agua en la esquina inferior derecha.
        
        Args:
            ruta_logo (str): Ruta al logo
            opacidad (float): Transparencia (0.0 = invisible, 1.0 = opaco)
            escala (float): Tamaño relativo al ancho de la imagen (0.25 = 25%)
        """
        self._verificar_imagen_cargada()
        
        if not validar_ruta(ruta_logo):
            raise ImagenNoEncontradaError(f"Logo no encontrado: {ruta_logo}")
        
        validar_factor(opacidad, 0.0, 1.0)
        validar_factor(escala, 0.05, 0.5)
        
        with Image.open(ruta_logo) as logo:
            # Calcular dimensiones proporcionales
            ancho_logo = int(self.imagen_procesada.width * escala)
            alto_logo = int(logo.height * (ancho_logo / logo.width))
            logo = logo.resize((ancho_logo, alto_logo), Image.Resampling.LANCZOS)
            
            # Aplicar transparencia
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            
            alpha = logo.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacidad)
            logo.putalpha(alpha)
            
            # Posicionar en esquina inferior derecha
            pos_x = self.imagen_procesada.width - ancho_logo - 20
            pos_y = self.imagen_procesada.height - alto_logo - 20
            
            if self.imagen_procesada.mode != 'RGBA':
                self.imagen_procesada = self.imagen_procesada.convert('RGBA')
            
            self.imagen_procesada.paste(logo, (pos_x, pos_y), logo)
            self._log("   -> Marca de agua aplicada")
        
        return self
    
     
# Contraste y Saturación Generar una versión de alto contraste
# y una de alta saturación de la misma imagen. 
# Objetivo: distinguir la diferencia entre modificar la 
# diferencia tonal vs. la viveza del color.
# Métodos: ImageEnhance.Contrast, ImageEnhance.Color

# Metodo contraste
    def contraste(self, valor_contraste: float) -> "Tono":
        self._image = ImageEnhance.Contrast(self._image).enhance(valor_contraste)
        return self
# Metodo saturacion
    def saturacion(self, valor_saturacion:float) -> "Tono":
        self._image = ImageEnhance.Color(self._image).enhance(valor_saturacion)
        return self

# Binariza la imagen evaluando cada píxel con una función lambda que asigna blanco (255)
# si supera el valor umbral o negro (0) en caso contrario.    
    def umbralizacion(self, valor_umbral): # Cambiamos el nombre aquí
    # Ahora usamos 'valor_umbral' dentro del lambda
        self._image = self._image.point(lambda x: 255 if x > valor_umbral else 0)
    #El paso final .convert('1') simplemente compacta esa información al formato de 1 bit que buscabas.

        self._image = self._image.convert('1')
        return self
    
    ## Se guarda resultado 


    def guardar_resultado(self, carpeta_salida="procesadas", nombre=None, formato="WEBP"):
        """
        Guarda la imagen procesada.
        
        Args:
            carpeta_salida (str): Directorio de destino
            nombre (str): Nombre personalizado (opcional)
            formato (str): Formato de salida (WEBP, JPEG, PNG)
        """
        self._verificar_imagen_cargada()
        
        crear_directorio(carpeta_salida)
        
        if nombre is None:
            nombre_base = Path(self.nombre_archivo).stem
            nombre = f"{nombre_base}_editada.{formato.lower()}"
        
        ruta_final = Path(carpeta_salida) / nombre
        
        # Convertir a RGB si es necesario
        imagen_guardar = self.imagen_procesada
        if formato.upper() in ["JPEG", "JPG"]:
            imagen_guardar = self.imagen_procesada.convert("RGB")
        
        imagen_guardar.save(ruta_final, formato.upper(), quality=90)
        self._log(f"💾 Guardado en: {ruta_final}")
        
        return str(ruta_final)
    
    def resetear(self):
        """Restaura la imagen al estado original"""
        if self.imagen_original:
            self.imagen_procesada = self.imagen_original.copy()
            self._log("🔄 Imagen restaurada al original")
        return self