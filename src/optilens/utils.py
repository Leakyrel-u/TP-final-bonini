"""Utilidades y validaciones con tipado estático completo"""

import os
from pathlib import Path
from typing import Union
from .exceptions import ParametroInvalidoError

# Este módulo tiene como objetivo centralizar las funciones de soporte del sistema para verificar 
# la existencia de rutas físicas y la correcta 
# creación de directorios en el almacenamiento.
# Asimismo, actúa como una capa de seguridad técnica que valida que los parámetros
# numéricos de procesamiento se mantengan dentro de rangos seguros,
# interrumpiendo la ejecución mediante excepciones personalizadas ante cualquier anomalía.

def validar_ruta(ruta: Union[str, Path]) -> bool:
    """
    Valida si una ruta existe en el sistema de archivos.

    Args:
        ruta (Union[str, Path]): La ruta a validar.

    Returns:
        bool: True si la ruta existe, False en caso contrario.
    """
    return Path(ruta).exists()

def validar_factor(factor: float, minimo: float = 0.0, maximo: float = 2.0) -> bool:
    """
    Valida si un factor numérico se encuentra dentro del rango seguro especificado.

    Args:
        factor (float): El factor numérico a evaluar.
        minimo (float): El límite inferior aceptable.
        maximo (float): El límite superior aceptable.

    Returns:
        bool: True si el factor está en rango.

    Raises:
        ParametroInvalidoError: Si el factor no es un número o está fuera del rango.
    """
    if not isinstance(factor, (int, float)):
        raise ParametroInvalidoError(f"El factor debe ser numérico, recibido: {type(factor)}")
    
    if not (minimo <= factor <= maximo):
        raise ParametroInvalidoError(f"Factor {factor} fuera de rango [{minimo}, {maximo}]")
    
    return True

def crear_directorio(ruta: Union[str, Path]) -> None:
    """
    Crea un directorio y sus padres si no existen en el disco.

    Args:
        ruta (Union[str, Path]): Ruta del directorio a crear.
    """
    Path(ruta).mkdir(parents=True, exist_ok=True)