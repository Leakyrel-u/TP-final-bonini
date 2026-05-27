Te implementaré el plan de acción siguiendo las buenas prácticas DRY, SOLID y Clean Code. Comenzaré con las modificaciones y nuevas implementaciones:

## 1. Primero, modifiquemos `pyproject.toml` para agregar las dependencias

```python
# pyproject.toml (modificación)
[project]
name = "optilens"
version = "0.1.0"
description = "Librería de procesamiento de imágenes con Pillow y OpenCV"
requires-python = ">=3.8"
dependencies = [
    "Pillow>=9.0.0",
    "numpy>=1.20.0",
    "opencv-python>=4.5.0"
]
```

## 2. Clase base para transformaciones

```python
# src/optilens/transforms/base.py
from abc import ABC, abstractmethod
from PIL import Image
import numpy as np
import cv2
from typing import Any, Dict

class BaseTransform(ABC):
    """Clase base abstracta para todas las transformaciones"""
    
    @abstractmethod
    def apply(self, image: Image.Image, **kwargs) -> Image.Image:
        """Aplica la transformación a una imagen PIL"""
        pass
    
    @staticmethod
    def pil_to_numpy(image: Image.Image) -> np.ndarray:
        """Convierte PIL Image a numpy array RGB"""
        return np.array(image.convert('RGB'))
    
    @staticmethod
    def pil_to_cv2(image: Image.Image) -> np.ndarray:
        """Convierte PIL Image a formato OpenCV (BGR)"""
        rgb = np.array(image.convert('RGB'))
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    
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
```

## 3. Filtros de Pillow

```python
# src/optilens/transforms/pillow_filters.py
from PIL import Image, ImageFilter
from .base import BaseTransform
from typing import Union, Tuple

class PillowFilterTransform(BaseTransform):
    """Suite de filtros rápidos basados en Pillow"""
    
    FILTERS = {
        'gaussian': ImageFilter.GaussianBlur,
        'median': ImageFilter.MedianFilter,
        'sharpen': ImageFilter.SHARPEN,
        'detail': ImageFilter.DETAIL,
        'smooth': ImageFilter.SMOOTH,
        'edge_enhance': ImageFilter.EDGE_ENHANCE,
        'emboss': ImageFilter.EMBOSS,
        'find_edges': ImageFilter.FIND_EDGES,
        'blur': ImageFilter.BLUR,
        'min': ImageFilter.MinFilter,
        'max': ImageFilter.MaxFilter,
    }
    
    def apply(self, image: Image.Image, filter_type: str = 'gaussian', 
              radius: int = 2, size: int = 3, **kwargs) -> Image.Image:
        """
        Aplica un filtro de Pillow a la imagen.
        
        Args:
            image: Imagen PIL de entrada
            filter_type: Tipo de filtro ('gaussian', 'median', 'sharpen', etc.)
            radius: Radio para GaussianBlur
            size: Tamaño para MedianFilter, MinFilter, MaxFilter
            
        Returns:
            Imagen PIL filtrada
        """
        filter_type = filter_type.lower()
        
        if filter_type not in self.FILTERS:
            raise ValueError(f"Filtro '{filter_type}' no soportado. "
                           f"Opciones: {list(self.FILTERS.keys())}")
        
        filter_class = self.FILTERS[filter_type]
        
        # Filtros parametrizables
        if filter_type == 'gaussian':
            filtro = filter_class(radius=radius)
        elif filter_type in ('median', 'min', 'max'):
            filtro = filter_class(size=size)
        else:
            filtro = filter_class
        
        return image.filter(filtro)
```

## 4. Convoluciones y filtros OpenCV

```python
# src/optilens/transforms/opencv_conv.py
import numpy as np
import cv2
from .base import BaseTransform
from typing import Optional, Union

class OpenCVConvolutionTransform(BaseTransform):
    """Filtros convolucionales y reducción de ruido con OpenCV"""
    
    PRESETS = {
        'box_blur': np.ones((5, 5), np.float32) / 25,
        'sharpen': np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]]),
        'edge_enhance': np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]]),
        'emboss': np.array([[-2, -1, 0],
                           [-1, 1, 1],
                           [0, 1, 2]]),
        'laplacian': np.array([[0, 1, 0],
                              [1, -4, 1],
                              [0, 1, 0]]),
    }
    
    def apply(self, image: Image.Image, kernel: Optional[Union[str, np.ndarray]] = None,
              bilateral_d: int = 9, bilateral_sigma_color: float = 75, 
              bilateral_sigma_space: float = 75, median_ksize: int = 5,
              filter_type: str = 'convolution', **kwargs) -> Image.Image:
        """
        Aplica filtros convolucionales o no lineales usando OpenCV.
        
        Args:
            image: Imagen PIL de entrada
            kernel: Kernel personalizado o nombre de preset
            bilateral_d: Diámetro para filtro bilateral
            bilateral_sigma_color: Sigma color para bilateral
            bilateral_sigma_space: Sigma espacio para bilateral
            median_ksize: Tamaño del kernel para mediana
            filter_type: 'convolution', 'bilateral', 'median'
            
        Returns:
            Imagen PIL filtrada
        """
        # Convertir a OpenCV
        img_cv = self.pil_to_cv2(image)
        
        if filter_type == 'convolution':
            # Determinar el kernel
            if isinstance(kernel, str):
                if kernel not in self.PRESETS:
                    raise ValueError(f"Preset '{kernel}' no encontrado. "
                                   f"Opciones: {list(self.PRESETS.keys())}")
                kernel = self.PRESETS[kernel]
            elif kernel is None:
                kernel = self.PRESETS['box_blur']
            
            # Aplicar convolución
            result = cv2.filter2D(img_cv, -1, kernel)
            
        elif filter_type == 'bilateral':
            result = cv2.bilateralFilter(img_cv, bilateral_d, 
                                        bilateral_sigma_color, 
                                        bilateral_sigma_space)
            
        elif filter_type == 'median':
            median_ksize = median_ksize if median_ksize % 2 == 1 else median_ksize + 1
            result = cv2.medianBlur(img_cv, median_ksize)
            
        else:
            raise ValueError(f"Tipo de filtro '{filter_type}' no soportado")
        
        return self.cv2_to_pil(result)
```

## 5. Detección de bordes

```python
# src/optilens/transforms/opencv_edges.py
import numpy as np
import cv2
from .base import BaseTransform
from typing import Tuple

class OpenCVEdgeDetectionTransform(BaseTransform):
    """Detección de bordes usando Sobel, Laplacian y Canny"""
    
    def apply(self, image: Image.Image, method: str = 'canny',
              threshold1: int = 100, threshold2: int = 200,
              aperture_size: int = 3, ksize: int = 3,
              dx: int = 1, dy: int = 0, **kwargs) -> Image.Image:
        """
        Detecta bordes en la imagen.
        
        Args:
            image: Imagen PIL de entrada
            method: 'canny', 'sobel', 'laplacian', 'sobel_x', 'sobel_y'
            threshold1: Umbral bajo para Canny
            threshold2: Umbral alto para Canny
            aperture_size: Tamaño de apertura para Canny y Laplacian
            ksize: Tamaño del kernel para Sobel
            dx: Orden de derivada en x para Sobel
            dy: Orden de derivada en y para Sobel
            
        Returns:
            Imagen PIL con bordes detectados
        """
        # Convertir a escala de grises y luego a OpenCV
        gray_pil = image.convert('L')
        gray_cv = np.array(gray_pil)
        
        method = method.lower()
        
        if method == 'canny':
            edges = cv2.Canny(gray_cv, threshold1, threshold2, 
                            apertureSize=aperture_size)
            
        elif method == 'sobel':
            edges = cv2.Sobel(gray_cv, cv2.CV_64F, dx, dy, ksize=ksize)
            edges = np.absolute(edges)
            edges = np.clip(edges, 0, 255).astype(np.uint8)
            
        elif method == 'sobel_x':
            edges = cv2.Sobel(gray_cv, cv2.CV_64F, 1, 0, ksize=ksize)
            edges = np.absolute(edges)
            edges = np.clip(edges, 0, 255).astype(np.uint8)
            
        elif method == 'sobel_y':
            edges = cv2.Sobel(gray_cv, cv2.CV_64F, 0, 1, ksize=ksize)
            edges = np.absolute(edges)
            edges = np.clip(edges, 0, 255).astype(np.uint8)
            
        elif method == 'laplacian':
            edges = cv2.Laplacian(gray_cv, cv2.CV_64F, ksize=aperture_size)
            edges = np.absolute(edges)
            edges = np.clip(edges, 0, 255).astype(np.uint8)
            
        else:
            raise ValueError(f"Método '{method}' no soportado. "
                           f"Opciones: 'canny', 'sobel', 'sobel_x', 'sobel_y', 'laplacian'")
        
        return self.numpy_to_pil(edges)
```

## 6. Transformada de Fourier

```python
# src/optilens/transforms/fourier.py
import numpy as np
from .base import BaseTransform
from typing import Literal

class FourierTransform(BaseTransform):
    """Transformada de Fourier y filtrado en frecuencia"""
    
    def apply(self, image: Image.Image, 
              filter_type: Literal['lowpass', 'highpass'] = 'lowpass',
              cutoff_radius: int = 30, 
              filter_shape: Literal['ideal', 'gaussian', 'butterworth'] = 'ideal',
              butterworth_order: int = 2,
              output_mode: Literal['filtered', 'spectrum'] = 'filtered',
              **kwargs) -> Image.Image:
        """
        Aplica filtrado en el dominio de la frecuencia.
        
        Args:
            image: Imagen PIL de entrada
            filter_type: 'lowpass' o 'highpass'
            cutoff_radius: Radio de corte en píxeles
            filter_shape: 'ideal', 'gaussian', 'butterworth'
            butterworth_order: Orden para filtro Butterworth
            output_mode: 'filtered' para imagen reconstruida, 'spectrum' para visualización
            
        Returns:
            Imagen filtrada o espectro de magnitud
        """
        # Convertir a escala de grises
        gray = image.convert('L')
        img_array = np.array(gray, dtype=np.float32)
        
        # Calcular FFT 2D
        f = np.fft.fft2(img_array)
        fshift = np.fft.fftshift(f)
        
        # Crear el filtro
        rows, cols = img_array.shape
        crow, ccol = rows // 2, cols // 2
        
        # Crear matriz de distancias
        y, x = np.ogrid[:rows, :cols]
        distance = np.sqrt((y - crow)**2 + (x - ccol)**2)
        
        # Crear filtro según el tipo
        if filter_shape == 'ideal':
            mask = self._ideal_filter(distance, cutoff_radius, filter_type)
        elif filter_shape == 'gaussian':
            mask = self._gaussian_filter(distance, cutoff_radius, filter_type)
        elif filter_shape == 'butterworth':
            mask = self._butterworth_filter(distance, cutoff_radius, 
                                           butterworth_order, filter_type)
        else:
            raise ValueError(f"Forma de filtro '{filter_shape}' no soportada")
        
        if output_mode == 'spectrum':
            # Visualizar espectro de magnitud
            magnitude_spectrum = np.log(np.abs(fshift) + 1)
            magnitude_spectrum = (magnitude_spectrum / magnitude_spectrum.max()) * 255
            return self.numpy_to_pil(magnitude_spectrum.astype(np.uint8))
        
        # Aplicar filtro
        fshift_filtered = fshift * mask
        
        # IFFT para reconstruir la imagen
        f_ishift = np.fft.ifftshift(fshift_filtered)
        img_filtered = np.fft.ifft2(f_ishift)
        img_filtered = np.abs(img_filtered)
        
        # Normalizar al rango [0, 255]
        img_filtered = ((img_filtered - img_filtered.min()) / 
                       (img_filtered.max() - img_filtered.min()) * 255)
        
        return self.numpy_to_pil(img_filtered.astype(np.uint8))
    
    def _ideal_filter(self, distance: np.ndarray, cutoff: int, 
                     filter_type: str) -> np.ndarray:
        """Filtro ideal pasa-bajos o pasa-altos"""
        if filter_type == 'lowpass':
            return (distance <= cutoff).astype(np.float32)
        else:  # highpass
            return (distance > cutoff).astype(np.float32)
    
    def _gaussian_filter(self, distance: np.ndarray, cutoff: int, 
                        filter_type: str) -> np.ndarray:
        """Filtro Gaussiano pasa-bajos o pasa-altos"""
        h = np.exp(-(distance**2) / (2 * (cutoff**2)))
        if filter_type == 'highpass':
            h = 1 - h
        return h
    
    def _butterworth_filter(self, distance: np.ndarray, cutoff: int, 
                          order: int, filter_type: str) -> np.ndarray:
        """Filtro Butterworth pasa-bajos o pasa-altos"""
        h = 1 / (1 + (distance / cutoff)**(2 * order))
        if filter_type == 'highpass':
            h = 1 - h
        return h
```

## 7. Restauración de Wiener

```python
# src/optilens/transforms/wiener.py
import numpy as np
from .base import BaseTransform
from typing import Literal, Tuple

class WienerRestorationTransform(BaseTransform):
    """Restauración de imágenes usando filtro de Wiener"""
    
    def apply(self, image: Image.Image,
              degradation_type: Literal['gaussian', 'motion'] = 'gaussian',
              gaussian_sigma: float = 3.0,
              motion_size: int = 15,
              motion_angle: float = 0,
              K: float = 0.01,
              **kwargs) -> Image.Image:
        """
        Restaura una imagen degradada usando deconvolución de Wiener.
        
        Args:
            image: Imagen PIL degradada
            degradation_type: 'gaussian' o 'motion'
            gaussian_sigma: Sigma para blur Gaussiano
            motion_size: Longitud del motion blur
            motion_angle: Ángulo del motion blur en grados
            K: Parámetro de regularización (relación ruido/señal inversa)
            
        Returns:
            Imagen PIL restaurada
        """
        # Convertir a escala de grises y a float
        gray = image.convert('L')
        img_array = np.array(gray, dtype=np.float32) / 255.0
        
        rows, cols = img_array.shape
        
        # Crear PSF (Point Spread Function) en el dominio de frecuencia
        if degradation_type == 'gaussian':
            h = self._create_gaussian_psf(rows, cols, gaussian_sigma)
        elif degradation_type == 'motion':
            h = self._create_motion_psf(rows, cols, motion_size, motion_angle)
        else:
            raise ValueError(f"Tipo de degradación '{degradation_type}' no soportado")
        
        # Transformada de Fourier de la imagen y la PSF
        G = np.fft.fft2(img_array)
        H = np.fft.fft2(h)
        
        # Aplicar filtro de Wiener
        H_conj = np.conj(H)
        H_abs_sq = np.abs(H) ** 2
        
        # Fórmula de Wiener: F = (H* / (|H|^2 + K)) * G
        F_hat = (H_conj / (H_abs_sq + K)) * G
        
        # Transformada inversa
        f_restored = np.fft.ifft2(F_hat)
        f_restored = np.abs(f_restored)
        
        # Normalizar
        f_restored = ((f_restored - f_restored.min()) / 
                     (f_restored.max() - f_restored.min()) * 255)
        
        return self.numpy_to_pil(f_restored.astype(np.uint8))
    
    def _create_gaussian_psf(self, rows: int, cols: int, sigma: float) -> np.ndarray:
        """Crea PSF Gaussiana normalizada"""
        y, x = np.ogrid[:rows, :cols]
        center_y, center_x = rows // 2, cols // 2
        
        psf = np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2))
        return psf / psf.sum()
    
    def _create_motion_psf(self, rows: int, cols: int, size: int, 
                          angle: float) -> np.ndarray:
        """Crea PSF de movimiento lineal"""
        psf = np.zeros((rows, cols))
        center_y, center_x = rows // 2, cols // 2
        
        # Convertir ángulo a radianes
        angle_rad = np.deg2rad(angle)
        
        # Crear línea
        for i in range(size):
            x_offset = int(center_x + i * np.cos(angle_rad))
            y_offset = int(center_y + i * np.sin(angle_rad))
            
            if 0 <= x_offset < cols and 0 <= y_offset < rows:
                psf[y_offset, x_offset] = 1
        
        # Normalizar
        return psf / psf.sum()
```

## 8. Actualizar __init__.py de transforms

```python
# src/optilens/transforms/__init__.py
from .pillow_filters import PillowFilterTransform
from .opencv_conv import OpenCVConvolutionTransform
from .opencv_edges import OpenCVEdgeDetectionTransform
from .fourier import FourierTransform
from .wiener import WienerRestorationTransform

__all__ = [
    'PillowFilterTransform',
    'OpenCVConvolutionTransform',
    'OpenCVEdgeDetectionTransform',
    'FourierTransform',
    'WienerRestorationTransform',
]
```

## 9. Actualizar core.py con los nuevos métodos

```python
# src/optilens/core.py
from PIL import Image
from .transforms import (
    PillowFilterTransform,
    OpenCVConvolutionTransform,
    OpenCVEdgeDetectionTransform,
    FourierTransform,
    WienerRestorationTransform,
)

class ProcesadorImagen:
    """Fachada principal para procesamiento de imágenes con API fluida"""
    
    def __init__(self, image: Image.Image = None):
        self._image = image
        self._pillow_filter = PillowFilterTransform()
        self._opencv_conv = OpenCVConvolutionTransform()
        self._opencv_edges = OpenCVEdgeDetectionTransform()
        self._fourier = FourierTransform()
        self._wiener = WienerRestorationTransform()
    
    def cargar(self, ruta: str):
        """Carga una imagen desde archivo"""
        self._image = Image.open(ruta)
        return self
    
    def aplicar_filtro_pillow(self, filter_type: str = 'gaussian', **kwargs):
        """Aplica filtros de Pillow"""
        self._image = self._pillow_filter.apply(self._image, filter_type, **kwargs)
        return self
    
    def convolucion_opencv(self, kernel=None, filter_type='convolution', **kwargs):
        """Aplica convoluciones y filtros OpenCV"""
        self._image = self._opencv_conv.apply(self._image, kernel, filter_type=filter_type, **kwargs)
        return self
    
    def detectar_bordes(self, method='canny', **kwargs):
        """Detecta bordes en la imagen"""
        self._image = self._opencv_edges.apply(self._image, method, **kwargs)
        return self
    
    def filtrado_fourier(self, filter_type='lowpass', output_mode='filtered', **kwargs):
        """Aplica filtrado en el dominio de frecuencia"""
        self._image = self._fourier.apply(self._image, filter_type, 
                                         output_mode=output_mode, **kwargs)
        return self
    
    def restaurar_wiener(self, degradation_type='gaussian', K=0.01, **kwargs):
        """Restaura imagen usando filtro de Wiener"""
        self._image = self._wiener.apply(self._image, degradation_type, K=K, **kwargs)
        return self
    
    def guardar(self, ruta: str):
        """Guarda la imagen procesada"""
        if self._image:
            self._image.save(ruta)
        return self
    
    def obtener_imagen(self):
        """Retorna la imagen PIL actual"""
        return self._image
```

## 10. Actualizar el __init__.py principal

```python
# src/optilens/__init__.py
from .core import ProcesadorImagen
from .transforms import (
    PillowFilterTransform,
    OpenCVConvolutionTransform,
    OpenCVEdgeDetectionTransform,
    FourierTransform,
    WienerRestorationTransform,
)

__version__ = "0.1.0"
__all__ = [
    'ProcesadorImagen',
    'PillowFilterTransform',
    'OpenCVConvolutionTransform',
    'OpenCVEdgeDetectionTransform',
    'FourierTransform',
    'WienerRestorationTransform',
]
```

## 11. Demo de ejemplo

```python
# examples/demo_advanced_filters.py
import sys
sys.path.append('src')

from optilens import ProcesadorImagen

def demo_advanced_filters():
    """Demostración de todos los filtros avanzados"""
    
    # Crear procesador
    proc = ProcesadorImagen()
    
    # 1. Filtros Pillow
    proc.cargar('pajaro.jpg')
    proc.aplicar_filtro_pillow('gaussian', radius=3)
    proc.guardar('output/pillow_gaussian.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.aplicar_filtro_pillow('sharpen')
    proc.guardar('output/pillow_sharpen.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.aplicar_filtro_pillow('median', size=5)
    proc.guardar('output/pillow_median.jpg')
    
    # 2. Convoluciones OpenCV
    proc.cargar('pajaro.jpg')
    proc.convolucion_opencv('sharpen')
    proc.guardar('output/opencv_sharpen.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.convolucion_opencv(filter_type='bilateral', 
                           bilateral_d=9, 
                           bilateral_sigma_color=75,
                           bilateral_sigma_space=75)
    proc.guardar('output/opencv_bilateral.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.convolucion_opencv(filter_type='median', median_ksize=5)
    proc.guardar('output/opencv_median.jpg')
    
    # 3. Detección de bordes
    proc.cargar('pajaro.jpg')
    proc.detectar_bordes('canny', threshold1=100, threshold2=200)
    proc.guardar('output/edges_canny.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.detectar_bordes('sobel')
    proc.guardar('output/edges_sobel.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.detectar_bordes('laplacian')
    proc.guardar('output/edges_laplacian.jpg')
    
    # 4. Filtrado en frecuencia (Fourier)
    proc.cargar('pajaro.jpg')
    proc.filtrado_fourier('lowpass', cutoff_radius=30, 
                         filter_shape='gaussian')
    proc.guardar('output/fourier_lowpass.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.filtrado_fourier('highpass', cutoff_radius=30, 
                         filter_shape='gaussian')
    proc.guardar('output/fourier_highpass.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.filtrado_fourier('lowpass', output_mode='spectrum')
    proc.guardar('output/fourier_spectrum.jpg')
    
    # 5. Restauración Wiener
    proc.cargar('pajaro.jpg')
    proc.restaurar_wiener('gaussian', gaussian_sigma=3.0, K=0.01)
    proc.guardar('output/wiener_gaussian.jpg')
    
    proc.cargar('pajaro.jpg')
    proc.restaurar_wiener('motion', motion_size=15, 
                         motion_angle=45, K=0.01)
    proc.guardar('output/wiener_motion.jpg')
    
    print("¡Demostración completada! Revisa la carpeta 'output/'")

if __name__ == '__main__':
    demo_advanced_filters()
```

## 12. Tests unitarios

```python
# tests/test_advanced_transforms.py
import unittest
import numpy as np
from PIL import Image
import sys
sys.path.append('src')

from optilens.transforms import (
    PillowFilterTransform,
    OpenCVConvolutionTransform,
    OpenCVEdgeDetectionTransform,
    FourierTransform,
    WienerRestorationTransform,
)

class TestAdvancedTransforms(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Crear imagen de prueba"""
        cls.test_image = Image.new('RGB', (100, 100), color='red')
        # Crear imagen con patrón
        arr = np.zeros((100, 100, 3), dtype=np.uint8)
        arr[25:75, 25:75] = [255, 255, 255]  # Cuadrado blanco
        cls.pattern_image = Image.fromarray(arr)
    
    def test_pillow_filter_dimensions(self):
        """Verificar que los filtros Pillow no cambien dimensiones"""
        transform = PillowFilterTransform()
        result = transform.apply(self.test_image, 'gaussian', radius=2)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_pillow_filter_types(self):
        """Verificar diferentes tipos de filtros Pillow"""
        transform = PillowFilterTransform()
        
        for filter_type in ['gaussian', 'median', 'sharpen', 'smooth', 'detail']:
            result = transform.apply(self.test_image, filter_type)
            self.assertIsInstance(result, Image.Image)
            self.assertEqual(result.size, self.test_image.size)
    
    def test_opencv_convolution_presets(self):
        """Verificar presets de convolución OpenCV"""
        transform = OpenCVConvolutionTransform()
        
        for preset in ['box_blur', 'sharpen', 'edge_enhance', 'emboss']:
            result = transform.apply(self.pattern_image, preset)
            self.assertIsInstance(result, Image.Image)
            self.assertEqual(result.size, self.pattern_image.size)
    
    def test_opencv_bilateral_filter(self):
        """Verificar filtro bilateral"""
        transform = OpenCVConvolutionTransform()
        result = transform.apply(self.pattern_image, filter_type='bilateral')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_opencv_median_filter(self):
        """Verificar filtro de mediana"""
        transform = OpenCVConvolutionTransform()
        result = transform.apply(self.pattern_image, filter_type='median')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_edge_detection_canny(self):
        """Verificar detección de bordes Canny"""
        transform = OpenCVEdgeDetectionTransform()
        result = transform.apply(self.pattern_image, 'canny')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
        # Verificar que sea imagen binaria (solo 0 y 255)
        arr = np.array(result)
        self.assertTrue(np.all(np.isin(arr, [0, 255])))
    
    def test_edge_detection_sobel(self):
        """Verificar detección de bordes Sobel"""
        transform = OpenCVEdgeDetectionTransform()
        result = transform.apply(self.pattern_image, 'sobel')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_edge_detection_laplacian(self):
        """Verificar detección de bordes Laplacian"""
        transform = OpenCVEdgeDetectionTransform()
        result = transform.apply(self.pattern_image, 'laplacian')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_fourier_lowpass(self):
        """Verificar filtro pasa-bajos Fourier"""
        transform = FourierTransform()
        result = transform.apply(self.pattern_image, 'lowpass', 
                                cutoff_radius=30, output_mode='filtered')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_fourier_highpass(self):
        """Verificar filtro pasa-altos Fourier"""
        transform = FourierTransform()
        result = transform.apply(self.pattern_image, 'highpass', 
                                cutoff_radius=30, output_mode='filtered')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_fourier_spectrum(self):
        """Verificar visualización del espectro"""
        transform = FourierTransform()
        result = transform.apply(self.pattern_image, output_mode='spectrum')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_wiener_gaussian(self):
        """Verificar restauración Wiener para desenfoque Gaussiano"""
        transform = WienerRestorationTransform()
        result = transform.apply(self.pattern_image, 'gaussian', 
                                gaussian_sigma=3.0, K=0.01)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_wiener_motion(self):
        """Verificar restauración Wiener para motion blur"""
        transform = WienerRestorationTransform()
        result = transform.apply(self.pattern_image, 'motion', 
                                motion_size=15, motion_angle=45, K=0.01)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.pattern_image.size)
    
    def test_wiener_numerical_stability(self):
        """Verificar estabilidad numérica del filtro Wiener"""
        transform = WienerRestorationTransform()
        # Probar con diferentes valores de K
        for K in [0.001, 0.01, 0.1, 1.0]:
            result = transform.apply(self.pattern_image, 'gaussian', K=K)
            arr = np.array(result)
            self.assertFalse(np.any(np.isnan(arr)), f"NaN encontrados con K={K}")
            self.assertFalse(np.any(np.isinf(arr)), f"Inf encontrados con K={K}")

if __name__ == '__main__':
    unittest.main()
```

Esta implementación completa sigue estrictamente los principios DRY, SOLID y Clean Code, proporcionando una arquitectura modular y extensible para el procesamiento avanzado de imágenes.