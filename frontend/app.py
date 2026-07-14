from __future__ import annotations

import sys
import tempfile
from io import BytesIO
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
st.write("Sube una imagen y selecciona las transformaciones que quieras aplicar.")

if "processor" not in st.session_state:
    st.session_state.processor = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "original_image" not in st.session_state:
    st.session_state.original_image = None
if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None

uploaded_file = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg", "webp"])
logo_file = st.file_uploader("Logo opcional para marca de agua", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_name:
    temp_dir = Path(tempfile.mkdtemp(dir=str(ROOT / "frontend")))
    input_path = temp_dir / uploaded_file.name
    input_path.write_bytes(uploaded_file.getbuffer())

    proc = ProcesadorImagen(verbose=False)
    proc.cargar_imagen(input_path)

    st.session_state.processor = proc
    st.session_state.current_image = proc.imagen_procesada.copy()
    st.session_state.original_image = proc.imagen_original.copy()
    st.session_state.uploaded_name = uploaded_file.name
    st.session_state.temp_dir = temp_dir

if st.session_state.processor is not None:
    st.subheader("Transformaciones")
    col1, col2 = st.columns(2)
    with col1:
        aplicar_brillo = st.checkbox("Aplicar brillo", value=True)
        aplicar_contraste = st.checkbox("Aplicar contraste", value=True)
        aplicar_saturacion = st.checkbox("Aplicar saturación", value=True)
    with col2:
        aplicar_umbral = st.checkbox("Aplicar binarización", value=True)
        aplicar_redimension = st.checkbox("Aplicar redimensionado", value=True)
        aplicar_marca = st.checkbox("Aplicar marca de agua", value=False)

    col3, col4 = st.columns(2)
    with col3:
        brillo = st.slider("Brillo", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        contraste = st.slider("Contraste", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        saturacion = st.slider("Saturación", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    with col4:
        ancho = st.number_input("Ancho", min_value=100, max_value=4000, value=800, step=10)
        alto = st.number_input("Alto", min_value=100, max_value=4000, value=600, step=10)
        umbral = st.slider("Umbral (binarización)", min_value=0, max_value=255, value=128)

    if aplicar_marca:
        opacidad = st.slider("Opacidad de la marca", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
        escala = st.slider("Escala de la marca", min_value=0.05, max_value=0.5, value=0.25, step=0.01)

    hist_col1, hist_col2, hist_col3 = st.columns(3)
    with hist_col1:
        if st.button("Aplicar transformaciones"):
            proc = st.session_state.processor
            if aplicar_brillo:
                proc.ajustar_brillo(brillo)
            if aplicar_contraste:
                proc.contraste(contraste)
            if aplicar_saturacion:
                proc.saturacion(saturacion)
            if aplicar_umbral:
                proc.umbralizacion(int(umbral))
            if aplicar_redimension:
                proc.redimensionar(int(ancho), int(alto))
            if aplicar_marca and logo_file is not None:
                logo_path = st.session_state.temp_dir / logo_file.name
                logo_path.write_bytes(logo_file.getbuffer())
                proc.aplicar_marca_agua(
                    ruta_logo=logo_path,
                    opacidad=float(opacidad),
                    escala=float(escala),
                )
            st.session_state.current_image = proc.imagen_procesada.copy()
            st.success("Transformaciones aplicadas y añadidas al historial")
    with hist_col2:
        if st.button("Deshacer"):
            proc = st.session_state.processor
            proc.deshacer()
            st.session_state.current_image = proc.imagen_procesada.copy()
    with hist_col3:
        if st.button("Rehacer"):
            proc = st.session_state.processor
            proc.rehacer()
            st.session_state.current_image = proc.imagen_procesada.copy()

    if st.button("Restablecer imagen original"):
        proc = st.session_state.processor
        proc.resetear()
        st.session_state.current_image = proc.imagen_procesada.copy()

    st.subheader("Vista previa")
    st.image(st.session_state.current_image, use_column_width=True)

    buffer = BytesIO()
    st.session_state.current_image.save(buffer, format="PNG")
    st.download_button(
        label="Descargar imagen procesada",
        data=buffer.getvalue(),
        file_name="imagen_procesada.png",
        mime="image/png",
    )
else:
    st.info("Carga una imagen para comenzar.")
