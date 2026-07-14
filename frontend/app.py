from __future__ import annotations

import sys
import tempfile
from io import BytesIO
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optilens import ProcesadorImagen

st.set_page_config(
    page_title="OptiLens UI",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1.5rem;
        max-width: 1500px;
    }
    .hero {
        background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 48%, #dbeafe 100%);
        color: #0f172a;
        padding: 1rem 1.2rem;
        border-radius: 16px;
        margin-bottom: 0.8rem;
        border: 1px solid #bfdbfe;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    }
    .hero h1 {
        margin: 0 0 0.25rem 0;
        font-size: 1.7rem;
    }
    .hero p {
        margin: 0;
        opacity: 0.9;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
        width: 380px !important;
        min-width: 320px !important;
    }
    .status-card {
        background: #f8fafc;
        color: #0f172a;
        border: 1px solid #dbeafe;
        border-radius: 12px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.7rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>OptiLens Studio</h1>
        <p>Aplica transformaciones a tus imágenes de forma visual, ordenada y con historial de cambios.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "processor" not in st.session_state:
    st.session_state.processor = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "original_image" not in st.session_state:
    st.session_state.original_image = None
if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None
if "temp_dir" not in st.session_state:
    st.session_state.temp_dir = None

with st.sidebar:
    st.header("Controles")
    st.caption("Sube una imagen y elige qué transformaciones aplicar.")

    uploaded_file = st.file_uploader(
        "1. Selecciona una imagen",
        type=["png", "jpg", "jpeg", "webp"],
    )

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

    if st.session_state.processor is None:
        st.info("Carga una imagen para comenzar.")
        st.stop()

    st.divider()
    st.subheader("2. Transformaciones")

    aplicar_brillo = st.checkbox("Brillo", value=True)
    aplicar_contraste = st.checkbox("Contraste", value=True)
    aplicar_saturacion = st.checkbox("Saturación", value=True)
    aplicar_umbral = st.checkbox("Binarización", value=True)
    aplicar_redimension = st.checkbox("Redimensionado", value=True)

    with st.expander("Opciones adicionales", expanded=False):
        aplicar_marca = st.checkbox("Marca de agua", value=False)
        if aplicar_marca:
            logo_file = st.file_uploader(
                "Logo para marca de agua",
                type=["png", "jpg", "jpeg", "webp"],
            )
            opacidad = st.slider("Opacidad", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
            escala = st.slider("Escala", min_value=0.05, max_value=0.5, value=0.25, step=0.01)
        else:
            logo_file = None
            opacidad = 0.5
            escala = 0.25

    st.divider()
    st.subheader("3. Ajustes")
    brillo = st.slider("Brillo", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    contraste = st.slider("Contraste", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    saturacion = st.slider("Saturación", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    ancho = st.number_input("Ancho", min_value=100, max_value=4000, value=800, step=10)
    alto = st.number_input("Alto", min_value=100, max_value=4000, value=600, step=10)
    umbral = st.slider("Umbral", min_value=0, max_value=255, value=128)

    st.divider()
    st.subheader("4. Historial")
    col_hist_1, col_hist_2, col_hist_3 = st.columns(3)
    with col_hist_1:
        if st.button("Aplicar", use_container_width=True):
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
            st.success("Transformaciones aplicadas")
    with col_hist_2:
        if st.button("Deshacer", use_container_width=True):
            proc = st.session_state.processor
            proc.deshacer()
            st.session_state.current_image = proc.imagen_procesada.copy()
    with col_hist_3:
        if st.button("Rehacer", use_container_width=True):
            proc = st.session_state.processor
            proc.rehacer()
            st.session_state.current_image = proc.imagen_procesada.copy()

    if st.button("Restablecer", use_container_width=True):
        proc = st.session_state.processor
        proc.resetear()
        st.session_state.current_image = proc.imagen_procesada.copy()

main_col_left, main_col_right = st.columns(2)
with main_col_left:
    st.markdown('<div class="status-card"><strong>Original</strong></div>', unsafe_allow_html=True)
    st.image(st.session_state.original_image, width="stretch")
with main_col_right:
    st.markdown('<div class="status-card"><strong>Vista previa actual</strong></div>', unsafe_allow_html=True)
    st.image(st.session_state.current_image, width="stretch")

buffer = BytesIO()
st.session_state.current_image.save(buffer, format="PNG")
st.download_button(
    label="Descargar imagen procesada",
    data=buffer.getvalue(),
    file_name="imagen_procesada.png",
    mime="image/png",
)
