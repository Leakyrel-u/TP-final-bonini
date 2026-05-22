from optilens import ProcesadorImagen

def test_pipeline_completo():
    print("Iniciando prueba integral de todas las funcionalidades...")
    
    proc = ProcesadorImagen(verbose=True)
    
    # 1. Cargar imagen original
    proc.cargar_imagen("pajaro.jpg")
    
    # 2. Aplicar todas las transformaciones en cadena (Pipeline fluido)
    proc.redimensionar(400, 400) \
        .ajustar_brillo(1.2) \
        .ajustar_contraste(1.1) \
        .saturacion(1.3) \
        .aplicar_marca_agua("marca.png", opacidad=0.3, escala=0.2)
        
    # 3. Guardar el primer resultado intermedio
    proc.guardar_resultado(nombre="pajaro_procesado_completo.png", formato="PNG")
    
    # 4. Probar umbralización/binarización desde la misma imagen procesada
    proc.umbralizacion(127)
    proc.guardar_resultado(nombre="pajaro_binarizado.png", formato="PNG")
    
    # 5. Probar resetear y volver al original
    proc.resetear()
    proc.redimensionar(200, 200).guardar_resultado(nombre="pajaro_reseteado_chico.webp", formato="WEBP")
    
    print("\n¡Prueba integral completada exitosamente!")

if __name__ == "__main__":
    test_pipeline_completo()
