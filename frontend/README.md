# UI de OptiLens con Streamlit

Esta carpeta contiene una interfaz sencilla para probar las funcionalidades de la librería OptiLens desde el navegador.

## Requisitos

- Python 3.13+
- uv instalado
- Dependencias del proyecto
- Streamlit

## Instalación con uv

Desde la raíz del proyecto, crea y activa el entorno virtual con uv:

```bash
uv venv
```

Instala las dependencias del paquete y la UI:

```bash
uv pip install -e .
uv pip install -r frontend/requirements.txt
```

> El archivo [frontend/requirements.txt](requirements.txt) se mantiene para quienes prefieran instalar dependencias con pip o con flujos tradicionales.

## Ejecución

Desde la raíz del proyecto, corre:

```bash
uv run python -m streamlit run frontend/app.py
```

Luego abre la URL que aparece en la terminal, normalmente:

```text
http://localhost:8501
```

## Qué puedes hacer en la UI

- Subir una imagen desde el disco
- Ajustar brillo, contraste y saturación
- Binarizar la imagen con un umbral
- Redimensionar a un ancho y alto deseados
- Opcionalmente aplicar una marca de agua con un logo propio
- Descargar la imagen resultante
