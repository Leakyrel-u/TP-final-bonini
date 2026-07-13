from optilens import ProcesadorImagen, GuardadorNube

# Método tradicional

proc = ProcesadorImagen()
proc.cargar_imagen("pajaro.jpg")
proc.redimensionar(800, 600)
proc.ajustar_brillo(1.5)
ruta = r"marca.png"
proc.aplicar_marca_agua(ruta_logo=ruta)
proc.contraste(.5).guardar_resultado(nombre="pajaro_contraste.jpg")

proc = ProcesadorImagen()
proc.cargar_imagen("pajaro.jpg")

proc.ajustar_brillo(1.5) \
        .contraste(1.2) \
        .saturacion(0.8) \
        .redimensionar(200, 200)
    
proc.guardar_resultado(nombre="pajaro_binarizado_y_procesado.png", formato="PNG")

# --- Ejemplos de uso de GuardadorNube ---
print("\n--- Ejemplos de Guardado en la Nube (Simulado) ---")

# Opción 1: Guardado implícito en la nube al pasar una URL HTTP/HTTPS como destino
url_destino_1 = "https://mi-nube-simulada.com/imagenes/pajaro_nube.jpg"
print("1. Guardando implícitamente en la nube al pasar una URL de destino a guardar_resultado:")
proc.guardar_resultado(destino=url_destino_1, formato="JPEG")

# Opción 2: Especificar explícitamente una instancia de GuardadorNube
url_destino_2 = "https://mi-nube-simulada.com/imagenes/pajaro_nube_explicito.png"
guardador_nube = GuardadorNube()
print("\n2. Guardando al pasar explícitamente la instancia de GuardadorNube a guardar_resultado:")
proc.guardar_resultado(
    destino=url_destino_2,
    guardador=guardador_nube,
    formato="PNG"
)

# Opción 3: Uso directo (standalone) de GuardadorNube sin ProcesadorImagen
if proc.imagen_procesada:
    print("\n3. Guardando directamente una imagen PIL usando GuardadorNube (standalone):")
    url_destino_3 = "https://mi-nube-simulada.com/imagenes/pajaro_directo.jpg"
    guardador_nube.guardar(
        imagen=proc.imagen_procesada,
        destino=url_destino_3,
        formato="JPEG"
    )