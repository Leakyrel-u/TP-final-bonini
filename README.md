
# Parcial Procesamiento de imágenes en el IFTS
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)


---

# Script de Procesamiento Digital de Imágenes
### Parcial 1 - Técnicas de Procesamiento de Imágenes
*Docente:* Juan Ignacio Bonini  
*Integrantes del Equipo:*
- Daniel Sanchez
- Agustin 
- Jazmin Pineda 

## Características


## 📌 Índice
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación de Métodos](#-documentación-de-métodos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Licencia](#-licencia)

## ✨ Características
* *Redimensionado Inteligente:* Cambia el tamaño de imágenes de alta resolución manteniendo la relación de aspecto original de forma automática.
* *Conversión y Optimización Web:* Transforma formatos pesados de origen (.png, .tiff) al formato moderno .webp, reduciendo drásticamente el peso de carga (LCP) sin perder calidad visual.
* *Marca de Agua Automatizada:* Superpone de manera sistemática un logotipo con transparencia (RGBA) en una esquina específica de todo el lote de imágenes.
* *Estandarización de Color:* Normaliza el perfil de color de los archivos crudos (ej. convirtiendo de CMYK de impresión a RGB estándar) para asegurar una visualización correcta en cualquier pantalla.
* *Ajustes Avanzados y Binarización:* Permite modificar el contraste, la saturación y aplicar umbralización selectiva mediante transformaciones directas en los píxeles.

## 🛠️ Tecnologías
* *Lenguaje:* [Python 3.11+](https://www.python.org)
* *Procesamiento de Imágenes:* [Pillow (PIL)](https://python-pillow.org)
* *Gestión de Entorno y Paquetes:* [uv (Astral)](https://github.com/astral-sh/uv)

## Instalación uv
Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

MacOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Configurar environment

```bash
uv venv
```

```bash
uv sync
```

## Funciones 

El procesador ejecuta transformaciones controladas sobre los canales y matrices de la imagen:

1. *Redimensionamiento Avanzado (ImageOps.fit):* Modifica las dimensiones geométricas de la imagen recortándola hacia el centro para encajar de forma exacta en el aspecto deseado. Utiliza el filtro de interpolación de alta calidad LANCZOS, reduciendo drásticamente el aliasing (efecto serrucho) en los bordes.
2. *Ajuste de Brillo y Contraste Lineal (ImageEnhance):* Realza o disminuye la luminancia y el rango dinámico de los píxeles mapeando de forma matemática las matrices de color mediante un factor de escala.
3. *Composición de Marca de Agua Alfa (Alpha Blending):* Convierte dinámicamente imágenes a espacio de color RGBA (Red, Green, Blue, Alpha) para incrustar logotipos comerciales con opacidad matemática transparente en coordenadas calculadas de la esquina inferior derecha.


## Decisiones Técnicas y Arquitectura

* *Separación de Responsabilidades:* El script divide estrictamente el parseo de argumentos (main.py), la lógica matemática de procesamiento (src/optilens/core.py), las excepciones personalizadas (exceptions.py) y las funciones de validación e I/O en (utils.py).
* *Uso de Entornos y Gestión Modernos:* Se adoptó uv para compilar un candado de dependencias estricto (uv.lock) garantizando la reproducibilidad exacta del entorno virtual Python.
* *Formatos Eficientes:* Se predetermina el formato de salida a WEBP debido a su superioridad en algoritmos de compresión con y sin pérdida en comparación con los formatos tradicionales JPEG y PNG.


## 📂 Estructura del Proyecto
```text
PARCIAL/
├── src/
│   └── optilens/          # Código principal del módulo
│       ├── _init_.py
│       ├── core.py        # Lógica del ProcesadorImagen
│       ├── exceptions.py
│       └── utils.py
├── examples/
│   └── ejemplo.py         # Script de demostración de uso
├── pyproject.toml         # Configuración del proyecto y dependencias
└── uv.lock                # Bloqueo de versiones de uv
