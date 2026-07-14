from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optilens import ProcesadorImagen

st.set_page_config(page_title="OptiLens UI", page_icon="🖼️", layout="wide")

st.title("OptiLens - Interfaz web con Streamlit")
st.write("Sube una imagen y aplica transformaciones con la librería de procesamiento de imágenes.")

uploaded_file = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg", "webp"])
logo_file = st.file_uploader("Logo opcional para marca de agua", type=["png", "jpg", "jpeg", "webp"])

col1, col2 = st.columns(2)
with col1:
    brillo = st.slider("Brillo", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    contraste = st.slider("Contraste", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    saturacion = st.slider("Saturación", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
with col2:
    ancho = st.number_input("Ancho", min_value=100, max_value=4000, value=800, step=10)
    alto = st.number_input("Alto", min_value=100, max_value=4000, value=600, step=10)
    umbral = st.slider("Umbral (binarización)", min_value=0, max_value=255, value=128)

watermark_enabled = st.checkbox("Aplicar marca de agua")
if watermark_enabled:
    opacidad = st.slider("Opacidad de la marca", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
    escala = st.slider("Escala de la marca", min_value=0.05, max_value=0.5, value=0.25, step=0.01)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    st.subheader("Vista previa original")
    st.image(original_image, use_column_width=True)

    if st.button("Procesar imagen"):
        with tempfile.TemporaryDirectory(dir=ROOT / "frontend") as tmp_dir:
            temp_dir = Path(tmp_dir)
            input_path = temp_dir / uploaded_file.name
            input_path.write_bytes(uploaded_file.getbuffer())

            proc = ProcesadorImagen(verbose=False)
            proc.cargar_imagen(input_path)
            proc.ajustar_brillo(brillo)
            proc.contraste(contraste)
            proc.saturacion(saturacion)
            proc.umbralizacion(int(umbral))
            proc.redimensionar(int(ancho), int(alto))

            if watermark_enabled and logo_file is not None:
                logo_path = temp_dir / logo_file.name
                logo_path.write_bytes(logo_file.getbuffer())
                proc.aplicar_marca_agua(
                    ruta_logo=logo_path,
                    opacidad=float(opacidad),
                    escala=float(escala),
                )

            output_path = temp_dir / "imagen_procesada.png"
            proc.guardar_resultado(
                nombre=output_path.name,
                carpeta_salida=temp_dir,
                formato="PNG",
            )

            processed_image = Image.open(output_path)
            st.success("Imagen procesada correctamente")
            st.subheader("Resultado")
            st.image(processed_image, use_column_width=True)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="Descargar imagen procesada",
                    data=f.read(),
                    file_name="imagen_procesada.png",
                    mime="image/png",
                )

            if st.button("Restaurar original"):
                st.rerun()
else:
    st.info("Carga una imagen para comenzar.")
