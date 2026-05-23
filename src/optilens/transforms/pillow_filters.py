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