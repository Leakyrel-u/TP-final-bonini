from optilens import ProcesadorImagen

# Método tradicional

proc = ProcesadorImagen()
proc.cargar_imagen("pajaro.jpg")
proc.redimensionar(800, 600)
proc.ajustar_brillo(1.5)
ruta = r"marca.png"
proc.aplicar_marca_agua(ruta_logo=ruta)
proc.contraste(.5).guardar_resultado(nombre="pajaro_contraste.jpg")
proc.umbralizacion(2).guardar_resultado(nombre="pajaro_umbralizacion.jpg")
proc.guardar_resultado()