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
