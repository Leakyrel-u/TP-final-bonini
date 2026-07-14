
# TP Final Optilens

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)

---

# Script de Procesamiento Digital de Imágenes

### Parcial 1 - Técnicas de Procesamiento de Imágenes

**Docente:** Juan Ignacio Bonini

**Integrantes del Equipo:**
- Daniel Sanchez
- Agustin Fernandez
- Jazmin Pineda

---

## Indice

- [Descripcion](#descripcion)
- [Caracteristicas](#caracteristicas)
- [Tecnologias](#tecnologias)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura y Decisiones Tecnicas](#arquitectura-y-decisiones-tecnicas)
- [Instalacion](#instalacion)
- [Uso](#uso)
- [Catalogo de Transformaciones](#catalogo-de-transformaciones)
- [Documentacion de la API](#documentacion-de-la-api)
- [Modulo de Entrada/Salida (IO)](#modulo-de-entradasalida-io)
- [Excepciones](#excepciones)
- [Pruebas](#pruebas)
- [Licencia](#licencia)

---

## Descripcion

OptiLens es una libreria de procesamiento digital de imagenes construida en Python sobre
[Pillow (PIL)](https://python-pillow.org) y [NumPy](https://numpy.org). Su objetivo es ofrecer
una interfaz fluida y extensible para aplicar transformaciones sobre imagenes: redimensionado,
ajustes de brillo, contraste y saturacion, marcas de agua, binarizacion, filtros de dominio
espacial (Pillow), filtrado en frecuencia (Transformada de Fourier) y restauracion por
deconvolucion de Wiener.

El componente central es la clase `ProcesadorImagen`, que actua como una **Fachada (Facade
Pattern)**: mantiene una API sencilla y encadenable, mientras orquesta internamente un pipeline
de transformaciones modulares. Cada operacion se delega a una clase concreta que hereda de
`BaseTransform`, lo que permite anadir nuevas transformaciones sin modificar el nucleo
(Principio Open/Closed).

La carga y el guardado de imagenes estan desacoplados del procesamiento mediante cargadores
(`CargadorLocal`, `CargadorUrl`) y guardadores (`GuardadorLocal`, `GuardadorNube`), tambien
basados en clases abstractas. Esto facilita soportar nuevos origenes o destinos (nube, base de
datos, etc.) sin tocar la logica de procesamiento.

---

## Caracteristicas

- **Redimensionado inteligente:** cambia el tamaño de imagenes de alta resolucion recortando
  hacia el centro para encajar en el aspecto deseado, usando el filtro LANCZOS de alta calidad
  para minimizar el aliasing (efecto serrucho).
- **Ajustes de color y tono:** modifica brillo, contraste y saturacion mediante
  `ImageEnhance` de Pillow, con validacion de rangos seguros.
- **Marca de agua automatizada:** superpone un logotipo con transparencia (RGBA) en la esquina
  inferior derecha, con control de opacidad y escala relativa.
- **Binarizacion (umbralizacion):** convierte la imagen a blanco y negro puro evaluando cada
  pixel contra un umbral.
- **Filtros de dominio espacial:** suite de filtros rapidos de Pillow (desenfoque gaussiano,
  mediano, realce de bordes, relieve, deteccion de bordes, etc.).
- **Filtrado en frecuencia:** Transformada de Fourier 2D con paso bajo / paso alto y mascaras
  ideal, gaussiana o Butterworth.
- **Restauracion de imagenes:** deconvolucion de Wiener para revertir degradaciones por
  desenfoque gaussiano o de movimiento.
- **Guardado flexible:** en disco local o (simulado) en la nube, con autodeteccion por la ruta
  y conversion automatica de modo para formatos sin canal alfa (JPEG).
- **Historial de cambios:** soporte de deshacer (`deshacer`) y rehacer (`rehacer`) con un limite
  configurable de pasos.
- **API fluida:** todos los metodos devuelven la propia instancia, permitiendo encadenar
  transformaciones en una sola linea.

---

## Tecnologias

- **Lenguaje:** [Python 3.13+](https://www.python.org)
- **Procesamiento de imagenes:** [Pillow (PIL)](https://python-pillow.org)
- **Computo numerico:** [NumPy](https://numpy.org)
- **Vision por computadora (utilidades):** [OpenCV](https://opencv.org)
- **Gestion de entorno y paquetes:** [uv (Astral)](https://github.com/astral-sh/uv)

---

## Estructura del Proyecto

```text
TP-final-bonini/
├── src/
│   └── optilens/                 # Codigo principal del paquete
│       ├── __init__.py           # Exporta la API publica
│       ├── core.py               # Clase ProcesadorImagen (fachada y orquestador)
│       ├── exceptions.py         # Excepciones personalizadas
│       ├── io.py                 # Carga/guardado (local, URL, nube)
│       ├── utils.py              # Validaciones y utilidades de rutas
│       ├── py.typed              # Marca el paquete como tipado
│       └── transforms/           # Transformaciones modulares
│           ├── base.py           # Clase abstracta BaseTransform
│           ├── resize.py         # Redimensionado
│           ├── brightness.py     # Brillo
│           ├── contrast.py       # Contraste
│           ├── saturation.py     # Saturacion
│           ├── watermark.py      # Marca de agua
│           ├── threshold.py      # Umbralizacion
│           ├── pillow_filters.py # Filtros de Pillow
│           ├── fourier.py        # Filtrado en frecuencia
│           └── weiner_restoration.py # Restauracion de Wiener
├── examples/
│   ├── ejemplo.py                # Demostracion de uso
│   ├── test_all_features.py      # Ejercita todas las funcionalidades
│   └── procesadas/               # Salida de ejemplos
├── tests/                        # Pruebas automatizadas (pytest)
│   ├── test_core.py
│   ├── test_history.py
│   ├── test_io.py
│   └── test_transforms.py
├── docs/                         # Documentacion tecnica complementaria
├── pyproject.toml                # Configuracion y dependencias del proyecto
├── requirements.txt             # Dependencias (pip)
└── README.md
```

---

## Arquitectura y Decisiones Tecnicas

- **Separacion de responsabilidades:** el procesamiento (`core.py`), la entrada/salida
  (`io.py`), las validaciones (`utils.py`) y las excepciones (`exceptions.py`) estan aislados.
  Cada transformacion vive en su propio modulo bajo `transforms/`.
- **Patron Fachada + Strategy:** `ProcesadorImagen` expone una API simple y encadenable, pero
  delega cada operacion a una instancia de `BaseTransform`. Para anadir una transformacion basta
  crear una subclase de `BaseTransform` e inyectarla con `aplicar_transformacion(...)`.
- **Inyeccion de cargadores/guardadores:** la carga y el guardado se resuelven mediante clases
  abstractas (`CargadorImagen`, `GuardadorImagen`). Si no se indica un cargador/guardador, se
  autodetecta a partir de si la ruta es una URL o una ruta de disco.
- **Procesamiento no destructivo:** al cargar, se trabaja sobre una copia (`imagen_procesada`)
  dejando intacta la `imagen_original`, que puede restaurarse con `resetear()`.
- **Gestion moderna de entornos:** se utiliza `uv` para crear el entorno virtual y fijar
  dependencias de forma reproducible.
- **Formatos eficientes:** el guardado local convierte automaticamente de RGBA/LA/P a RGB cuando
  el formato de salida es JPEG (que no soporta canal alfa), evitando errores.

---

## Instalacion

OptiLens usa `uv` para gestionar el entorno. Instalalo primero:

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Luego, en la raiz del proyecto, crea el entorno y sincroniza las dependencias:

```bash
uv venv
uv sync
```

Para instalar como paquete editable (para poder importar `optilens` desde cualquier script):

```bash
uv pip install -e .
```

> Tambien es posible usar `pip` con `requirements.txt` si no se cuenta con `uv`:
> `pip install -r requirements.txt`

---

## Uso

### Carga basica y guardado

```python
from optilens import ProcesadorImagen

proc = ProcesadorImagen()
proc.cargar_imagen("pajaro.jpg")          # carga desde disco local
proc.redimensionar(800, 600)              # recorta y ajusta a 800x600
proc.ajustar_brillo(1.5)                  # +50% de brillo
proc.guardar_resultado(nombre="salida.jpg", formato="JPEG")
```

### API fluida (encadenamiento de metodos)

Todos los metodos devuelven la propia instancia, por lo que puedes encadenar transformaciones
en una sola linea:

```python
from optilens import ProcesadorImagen

proc = ProcesadorImagen(verbose=False)
proc.cargar_imagen("pajaro.jpg") \
    .ajustar_brillo(1.5) \
    .contraste(1.2) \
    .saturacion(0.8) \
    .redimensionar(200, 200) \
    .guardar_resultado(nombre="pajaro_procesado.png", formato="PNG")
```

### Marca de agua

```python
from optilens import ProcesadorImagen

proc = ProcesadorImagen()
proc.cargar_imagen("pajaro.jpg")
proc.aplicar_marca_agua(
    ruta_logo="marca.png",   # logotipo con transparencia (RGBA)
    opacidad=0.5,            # 0.0 invisible .. 1.0 opaco
    escala=0.25              # 25% del ancho de la imagen
)
proc.guardar_resultado(nombre="pajaro_marca.png", formato="PNG")
```

### Carga desde URL y guardado en la nube (simulado)

El cargador y el guardador se autodetectan por la ruta. Si pasas una URL `http(s)` como destino,
se usa `GuardadorNube` (simulado, solo registra el tamaño y la URL):

```python
from optilens import ProcesadorImagen, GuardadorNube

proc = ProcesadorImagen()
proc.cargar_imagen("https://ejemplo.com/pajaro.jpg")   # CargadorUrl

# Opcion 1: autodeteccion por URL de destino
proc.guardar_resultado(
    destino="https://mi-nube-simulada.com/imagenes/pajaro.jpg",
    formato="JPEG"
)

# Opcion 2: guardador explicito
guardador = GuardadorNube()
proc.guardar_resultado(
    destino="https://mi-nube-simulada.com/imagenes/pajaro.png",
    guardador=guardador,
    formato="PNG"
)
```

### Deshacer, rehacer y resetear

El procesador mantiene un historial acotado por `max_cambios` (por defecto 5):

```python
from optilens import ProcesadorImagen

proc = ProcesadorImagen(max_cambios=10)
proc.cargar_imagen("pajaro.jpg")
proc.ajustar_brillo(1.5)
proc.contraste(1.2)

proc.deshacer()    # revierte el contraste
proc.rehacer()     # reaplica el contraste
proc.resetear()    # vuelve al estado original cargado
```

### Transformaciones avanzadas (Fourier y Wiener)

Estas transformaciones se aplican mediante `aplicar_transformacion` pasando la clase concreta:

```python
from optilens import ProcesadorImagen
from optilens.transforms import FourierTransform, WienerRestorationTransform

proc = ProcesadorImagen()
proc.cargar_imagen("pajaro.jpg")

# Filtro pasa bajos gaussiano en frecuencia
proc.aplicar_transformacion(
    FourierTransform().apply(
        proc.imagen_procesada,
        filter_type="lowpass",
        filter_shape="gaussian",
        cutoff_radius=30,
    )
)

# Restauracion de Wiener para desenfoque gaussiano
proc.aplicar_transformacion(
    WienerRestorationTransform().apply(
        proc.imagen_procesada,
        degradation_type="gaussian",
        gaussian_sigma=3.0,
        K=0.01,
    )
)

proc.guardar_resultado(nombre="restaurada.png", formato="PNG")
```

### Crear una transformacion personalizada

Gracias al diseno abierto, puedes definir tu propia transformacion sin tocar el nucleo:

```python
from PIL import ImageOps
from optilens import ProcesadorImagen
from optilens.transforms import BaseTransform

class InvertirTransform(BaseTransform):
    def apply(self, imagen):
        return ImageOps.invert(imagen.convert("RGB"))

proc = ProcesadorImagen()
proc.cargar_imagen("pajaro.jpg")
proc.aplicar_transformacion(InvertirTransform())
proc.guardar_resultado(nombre="invertida.jpg")
```

### Ejecutar los ejemplos incluidos

```bash
uv run python examples/ejemplo.py
```

---

## Catalogo de Transformaciones

Cada transformacion es una subclase de `BaseTransform` con un metodo `apply(imagen) -> imagen`.

| Transformacion            | Modulo                 | Efecto                                                        |
|---------------------------|------------------------|---------------------------------------------------------------|
| `ResizeTransform`         | `resize.py`            | Redimensiona recortando al centro con LANCZOS.                |
| `BrightnessTransform`     | `brightness.py`        | Multiplica la luminancia por un factor.                      |
| `ContrastTransform`       | `contrast.py`          | Ajusta la diferencia tonal por un factor.                    |
| `SaturationTransform`     | `saturation.py`        | Modifica la viveza del color (`ImageEnhance.Color`).         |
| `WatermarkTransform`      | `watermark.py`         | Superpone un logo RGBA en la esquina inferior derecha.       |
| `ThresholdTransform`      | `threshold.py`         | Binariza a 1 bit segun un umbral.                             |
| `PillowFilterTransform`   | `pillow_filters.py`    | Filtros rapidos de Pillow (blur, sharpen, edges, etc.).      |
| `FourierTransform`        | `fourier.py`           | Filtrado pasa bajo/alto en el dominio de frecuencia.         |
| `WienerRestorationTransform` | `weiner_restoration.py` | Restauracion por deconvolucion de Wiener.                |

### Descripcion de cada tecnica y su efecto

1. **Redimensionamiento avanzado (`ImageOps.fit`):** modifica las dimensiones geometricas
   recortando hacia el centro para encajar exactamente en el aspecto deseado. Usa el filtro de
   interpolacion LANCZOS, que reduce drasticamente el aliasing en los bordes.
2. **Brillo y contraste lineal (`ImageEnhance`):** realza o disminuye la luminancia y el rango
   dinamico mapeando las matrices de color mediante un factor de escala. `contraste()` es un
   alias de `ajustar_contraste()`.
3. **Composicion de marca de agua alfa (Alpha Blending):** convierte la imagen a RGBA para
   incrustar un logotipo con opacidad transparente en la esquina inferior derecha (margen de 20 px).
4. **Saturacion (`ImageEnhance.Color`):** modifica la intensidad y vivacidad de los colores
   segun un factor flotante, actualizando el estado y devolviendo la instancia para encadenar.
5. **Umbralizacion (binarizacion):** convierte a escala de grises y evalua cada pixel con una
   funcion lambda que asigna blanco (255) si supera el umbral o negro (0) en caso contrario,
   compactando el resultado a 1 bit.
6. **Filtros de Pillow:** suite de filtros espaciales (gaussiano, mediano, realce, detalle,
   suavizado, realce de bordes, relieve, deteccion de bordes, blur, min/max).
7. **Transformada de Fourier:** lleva la imagen al dominio de frecuencia para aplicar paso bajo
   (suaviza) o paso alto (resalta bordes) con mascaras ideal, gaussiana o Butterworth; puede
   devolver la imagen filtrada o el espectro de magnitud.
8. **Restauracion de Wiener:** aplica deconvolucion de Wiener para revertir degradaciones por
   desenfoque gaussiano o de movimiento, usando un parametro de regularizacion `K`.

---

## Documentacion de la API

### `ProcesadorImagen`

Clase principal. Constructor:

```python
ProcesadorImagen(verbose: bool = True, max_cambios: int = 5)
```

- `verbose`: si `True`, imprime mensajes de progreso (con fallback seguro para consolas sin
  soporte de emojis).
- `max_cambios`: cantidad maxima de pasos guardados para deshacer/rehacer.

Metodos principales (todos devuelven `self` para encadenar):

| Metodo | Descripcion | Parametros clave |
|--------|-------------|------------------|
| `cargar_imagen(ruta, cargador=None)` | Carga desde disco o URL (no destructivo). | `ruta`: archivo o URL. |
| `redimensionar(ancho=400, alto=400)` | Redimensiona recortando al centro. | `ancho`, `alto` en px. |
| `ajustar_brillo(factor=1.0)` | Brillo (1.0 = igual). | `factor`: 0.0–3.0. |
| `ajustar_contraste(factor=1.0)` | Contraste (1.0 = igual). | `factor`: 0.0–3.0. |
| `contraste(valor)` | Alias de `ajustar_contraste`. | `valor`: factor. |
| `saturacion(valor)` | Saturacion de color. | `valor`: 0.0–3.0. |
| `aplicar_marca_agua(ruta_logo, opacidad=0.5, escala=0.25)` | Superpone logo RGBA. | `opacidad`: 0–1; `escala`: 0.05–0.5. |
| `umbralizacion(valor_umbral)` | Binariza (0–255). | `valor_umbral`: 0–255. |
| `aplicar_transformacion(transformacion)` | Aplica cualquier `BaseTransform` y la registra en el pipeline. | instancia de transformacion. |
| `guardar_resultado(destino=None, guardador=None, carpeta_salida="procesadas", nombre=None, formato="JPEG")` | Guarda local o en nube. | `formato`: JPEG/WEBP/PNG. |
| `resetear()` | Restaura la imagen original cargada. | — |
| `deshacer()` | Revierte el ultimo cambio (hasta `max_cambios`). | — |
| `rehacer()` | Reaplica el ultimo cambio deshecho. | — |

Atributos utiles: `imagen_original`, `imagen_procesada`, `nombre_archivo`, `ultimo_guardado`.

---

## Modulo de Entrada/Salida (IO)

El modulo `io.py` aislala lectura y escritura mediante clases abstractas:

- **`CargadorImagen`** (abstracta)
  - `CargadorLocal`: carga desde disco; lanza `ImagenNoEncontradaError` si no existe.
  - `CargadorUrl`: descarga desde HTTP/HTTPS con un `User-Agent` propio.
- **`GuardadorImagen`** (abstracta)
  - `GuardadorLocal`: crea directorios si faltan y guarda en disco; convierte RGBA→RGB para JPEG.
  - `GuardadorNube`: guardador simulado que valida la URL y registra el tamaño subido.
- **`ImageIO`**: utilidad estatica con `cargar()` y `guardar()` para uso directo sin el procesador.

```python
from optilens.io import ImageIO

img = ImageIO.cargar("pajaro.jpg")
ImageIO.guardar(img, carpeta_salida="procesadas", nombre="out.jpg", formato="JPEG")
```

---

## Excepciones

Todas heredan de `OptiLensError` (base) y se encuentran en `exceptions.py`:

- `OptiLensError`: base de todas las excepciones del paquete.
- `ImagenNoEncontradaError`: el archivo o URL de origen no existe o no se puede abrir.
- `ImagenNoCargadaError`: se intenta operar sin una imagen cargada.
- `ParametroInvalidoError`: un parametro esta fuera de rango o es de tipo incorrecto (ej. factor
  de brillo fuera de [0, 3], URL invalida).

```python
from optilens import ProcesadorImagen
from optilens.exceptions import ImagenNoEncontradaError

proc = ProcesadorImagen(verbose=False)
try:
    proc.cargar_imagen("no_existe.jpg")
except ImagenNoEncontradaError as e:
    print(f"Error: {e}")
```

---

## Pruebas

El proyecto incluye pruebas con `pytest` en `tests/`:

```bash
uv run pytest
```

- `test_core.py`: comportamiento del procesador y encadenamiento.
- `test_history.py`: deshacer, rehacer y resetear.
- `test_io.py`: carga/guardado local y validaciones.
- `test_transforms.py`: cada transformacion sobre una imagen de prueba.

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT.