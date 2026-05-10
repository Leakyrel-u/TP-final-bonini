from optilens import ProcesadorImagen

# Método tradicional
proc = ProcesadorImagen()
proc.cargar_imagen("foto.jpg")
proc.redimensionar(800, 600)
proc.ajustar_brillo(1.2)
proc.guardar_resultado()

# Método encadenado (fluent interface)
ProcesadorImagen() \
    .cargar_imagen("foto.jpg") \
    .redimensionar(800, 600) \
    .ajustar_brillo(1.2) \
    .ajustar_contraste(1.1) \
    .guardar_resultado()