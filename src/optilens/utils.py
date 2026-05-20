"""Utilidades y validaciones"""

import os
from pathlib import Path
from .exceptions import ParametroInvalidoError

#Este módulo tiene como objetivo centralizar las funciones de soporte del sistema para verificar 
# la existencia de rutas físicas y la correcta 
# creación de directorios en el almacenamiento.
# Asimismo, actúa como una capa de seguridad técnica que valida que los parámetros
# numéricos de procesamiento se mantengan dentro de rangos seguros,
# interrumpiendo la ejecución mediante excepciones personalizadas ante cualquier anomalía.

def validar_ruta(ruta):
    """Valida que una ruta exista"""
    return Path(ruta).exists()

def validar_factor(factor, minimo=0.0, maximo=2.0):
    """Valida que un factor esté en rango válido"""
    if not isinstance(factor, (int, float)):
        raise ParametroInvalidoError(f"El factor debe ser numérico, recibido: {type(factor)}")
    
    if not minimo <= factor <= maximo:
        raise ParametroInvalidoError(f"Factor {factor} fuera de rango [{minimo}, {maximo}]")
    
    return True

def crear_directorio(ruta):
    """Crea un directorio si no existe"""
    Path(ruta).mkdir(parents=True, exist_ok=True)