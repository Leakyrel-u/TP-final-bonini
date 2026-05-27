## 4. Convoluciones y filtros OpenCV
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
