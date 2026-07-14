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
    page_title="OptiLens Studio",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: #1e1e1e;
        color: #d4d4d4;
    }
    [data-testid="stHeader"] {
        display: none;
    }
    .block-container {
        padding-top: 0.4rem;
        padding-bottom: 0.6rem;
        max-width: 1600px;
    }
    [data-testid="stSidebar"] {
        background: #252526;
        border-right: 1px solid #3c3c3c;
        width: 330px !important;
        min-width: 300px !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 0.3rem;
        padding-bottom: 0.2rem;
    }
    .topbar {
        background: linear-gradient(90deg, #2d2d30 0%, #252526 100%);
        border: 1px solid #3c3c3c;
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .topbar-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
    }
    .topbar-subtitle {
        font-size: 0.85rem;
        color: #9cdcfe;
    }
    .panel {
        background: #252526;
        border: 1px solid #3c3c3c;
        border-radius: 12px;
        padding: 0.6rem 0.75rem;
        margin-bottom: 0.55rem;
    }
    .toolbar {
        background: #2d2d30;
        border: 1px solid #3c3c3c;
        border-radius: 10px;
        padding: 0.35rem;
        margin-bottom: 0.55rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        align-items: center;
    }
    .toolbar .stButton > button {
        margin: 0;
        width: 100%;
        min-height: 2.2rem;
    }
    .preview-card {
        background: #1e1e1e;
        border: 1px solid #3c3c3c;
        border-radius: 10px;
        padding: 0.45rem 0.65rem;
        margin-bottom: 0.4rem;
        color: #d4d4d4;
        font-weight: 600;
    }
    .stButton > button {
        background: #0e639c;
        color: white;
        border: 1px solid #1177b0;
        border-radius: 8px;
        height: 2.1rem;
        padding: 0 0.7rem;
    }
    .stButton > button:hover {
        background: #1177b0;
        border-color: #1691d0;
    }
    .stDownloadButton > button {
        background: #2f6f3e;
        border-color: #3a874c;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {
        background: #3c3c3c;
        color: #ffffff;
        border: 1px solid #4f4f4f;
    }
    .stSlider > div[data-testid="stTickBarMin"] {
        color: #d4d4d4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="topbar">
        <div>
            <div class="topbar-title">OptiLens Studio</div>
            <div class="topbar-subtitle">Editor visual para procesamiento de imágenes</div>
        </div>
        <div class="topbar-subtitle">Streamlit · VS Code style</div>
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
if "last_action" not in st.session_state:
    st.session_state.last_action = "Esperando imagen..."

with st.sidebar:
    st.markdown('<div class="panel"><strong>Explorer</strong></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Abrir imagen", type=["png", "jpg", "jpeg", "webp"])

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
        st.session_state.last_action = "Imagen cargada"

    st.markdown('<div class="panel"><strong>Transformaciones</strong></div>', unsafe_allow_html=True)
    aplicar_brillo = st.checkbox("Brillo", value=True)
    aplicar_contraste = st.checkbox("Contraste", value=True)
    aplicar_saturacion = st.checkbox("Saturación", value=True)
    aplicar_umbral = st.checkbox("Binarización", value=True)
    aplicar_redimension = st.checkbox("Redimensionado", value=True)

    with st.expander("Más opciones", expanded=False):
        aplicar_marca = st.checkbox("Marca de agua", value=False)
        if aplicar_marca:
            logo_file = st.file_uploader("Logo", type=["png", "jpg", "jpeg", "webp"])
            opacidad = st.slider("Opacidad", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
            escala = st.slider("Escala", min_value=0.05, max_value=0.5, value=0.25, step=0.01)
        else:
            logo_file = None
            opacidad = 0.5
            escala = 0.25

    st.markdown('<div class="panel"><strong>Ajustes</strong></div>', unsafe_allow_html=True)
    brillo = st.slider("Brillo", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    contraste = st.slider("Contraste", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    saturacion = st.slider("Saturación", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
    ancho = st.number_input("Ancho", min_value=100, max_value=4000, value=800, step=10)
    alto = st.number_input("Alto", min_value=100, max_value=4000, value=600, step=10)
    umbral = st.slider("Umbral", min_value=0, max_value=255, value=128)

if st.session_state.processor is None:
    st.info("Carga una imagen desde la barra lateral para comenzar.")
    st.stop()

st.session_state.aplicar_brillo = aplicar_brillo
st.session_state.aplicar_contraste = aplicar_contraste
st.session_state.aplicar_saturacion = aplicar_saturacion
st.session_state.aplicar_umbral = aplicar_umbral
st.session_state.aplicar_redimension = aplicar_redimension
st.session_state.logo_file = logo_file
st.session_state.opacidad = opacidad
st.session_state.escala = escala

st.markdown('<div class="toolbar">', unsafe_allow_html=True)
toolbar_cols = st.columns([1.2, 1.0, 1.0, 1.0, 1.2], gap="small")
with toolbar_cols[0]:
    if st.button("✓ Aplicar", use_container_width=True):
        proc = st.session_state.processor
        if st.session_state.aplicar_brillo:
            proc.ajustar_brillo(brillo)
        if st.session_state.aplicar_contraste:
            proc.contraste(contraste)
        if st.session_state.aplicar_saturacion:
            proc.saturacion(saturacion)
        if st.session_state.aplicar_umbral:
            proc.umbralizacion(int(umbral))
        if st.session_state.aplicar_redimension:
            proc.redimensionar(int(ancho), int(alto))
        if aplicar_marca and st.session_state.logo_file is not None:
            logo_path = st.session_state.temp_dir / st.session_state.logo_file.name
            logo_path.write_bytes(st.session_state.logo_file.getbuffer())
            proc.aplicar_marca_agua(
                ruta_logo=logo_path,
                opacidad=float(st.session_state.opacidad),
                escala=float(st.session_state.escala),
            )

        st.session_state.current_image = proc.imagen_procesada.copy()
        st.session_state.last_action = "Transformaciones aplicadas"
with toolbar_cols[1]:
    if st.button("↺ Deshacer", use_container_width=True):
        st.session_state.processor.deshacer()
        st.session_state.current_image = st.session_state.processor.imagen_procesada.copy()
        st.session_state.last_action = "Deshacer"
with toolbar_cols[2]:
    if st.button("↻ Rehacer", use_container_width=True):
        st.session_state.processor.rehacer()
        st.session_state.current_image = st.session_state.processor.imagen_procesada.copy()
        st.session_state.last_action = "Rehacer"
with toolbar_cols[3]:
    if st.button("⟳ Reset", use_container_width=True):
        st.session_state.processor.resetear()
        st.session_state.current_image = st.session_state.processor.imagen_procesada.copy()
        st.session_state.last_action = "Restablecido"
with toolbar_cols[4]:
    if st.button("⬇ Descargar", use_container_width=True):
        st.session_state.last_action = "Descarga lista"
st.markdown('</div>', unsafe_allow_html=True)

st.caption(st.session_state.last_action)

preview_col, info_col = st.columns([2, 1])
with preview_col:
    st.markdown('<div class="preview-card"><strong>Original</strong></div>', unsafe_allow_html=True)
    st.image(st.session_state.original_image, width="stretch")
with info_col:
    st.markdown('<div class="preview-card"><strong>Vista previa actual</strong></div>', unsafe_allow_html=True)
    st.image(st.session_state.current_image, width="stretch")

buffer = BytesIO()
st.session_state.current_image.save(buffer, format="PNG")
st.download_button(
    label="Guardar PNG",
    data=buffer.getvalue(),
    file_name="imagen_procesada.png",
    mime="image/png",
)
