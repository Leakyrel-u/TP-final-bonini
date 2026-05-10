## Instalar uv

En Windows:

version 1
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

version 2
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.11.12/install.ps1 | iex"
```

# 📸 OptiLens - Librería de Procesamiento de Imágenes

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)

**OptiLens** es una librería Python simple y optimizada para el procesamiento de imágenes, diseñada para optimizar y editar imágenes de forma programática con una interfaz intuitiva.

---

## Características

- ✅ Redimensionamiento inteligente con preservación de proporciones
- ✅ Ajuste de brillo y contraste
- ✅ Aplicación de marcas de agua transparentes
- ✅ Conversión automática a formatos optimizados (WebP, JPEG, PNG)
- ✅ Interfaz fluida para encadenar operaciones
- ✅ Manejo robusto de errores
- ✅ Logging integrado

---

## 📦 Instalación

### Desde el repositorio (desarrollo)

```bash
# Clonar el repositorio
git clone https://github.com/Leakyrel-u/TP-final-bonini.git
cd optilens

# Instalar en modo desarrollo
pip install -e .