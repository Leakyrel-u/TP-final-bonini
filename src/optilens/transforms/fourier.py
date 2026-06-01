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