from optilens import ProcesadorImagen
from optilens.transforms.base import BaseTransform
from PIL import Image

class InvertColorsTransform(BaseTransform):
    """Transformación personalizada de ejemplo para verificar aplicar_transformacion"""
    def apply(self, imagen: Image.Image) -> Image.Image:
        if imagen.mode == "RGB":
            r, g, b = imagen.split()
            return Image.merge("RGB", (b, g, r))
        elif imagen.mode == "L":
            return imagen.point(lambda x: 255 - x)
        return imagen

def test_pipeline_completo():
    print("=== Iniciando prueba integral de todas las funcionalidades ===")
    
    # Instanciar el procesador con un historial máximo personalizado (ej. 3 cambios)
    proc = ProcesadorImagen(verbose=True, max_cambios=3)
    
    # 1. Cargar imagen original
    proc.cargar_imagen("pajaro.jpg")
    
    # 2. Aplicar transformaciones básicas en cadena (Pipeline fluido)
    print("\n--- 2. Aplicando transformaciones básicas ---")
    proc.redimensionar(400, 400) \
        .ajustar_brillo(1.2) \
        .ajustar_contraste(1.1) \
        .saturacion(1.3) \
        .aplicar_marca_agua("marca.png", opacidad=0.3, escala=0.2)
        
    proc.guardar_resultado(nombre="pajaro_procesado_completo.png", formato="PNG")
    
    # 3. Probar historial de cambios: Deshacer y Rehacer
    print("\n--- 3. Probando Historial de Cambios (Deshacer/Rehacer) ---")
    # Actualmente tenemos 5 cambios aplicados en el paso 2
    # El tamaño de la imagen procesada es 400x400. Vamos a deshacer la marca de agua:
    proc.deshacer()
    proc.guardar_resultado(nombre="pajaro_sin_marca_agua.png", formato="PNG")
    
    # Volvemos a aplicar la marca de agua usando rehacer:
    proc.rehacer()
    proc.guardar_resultado(nombre="pajaro_con_marca_agua_rehecha.png", formato="PNG")
    
    # 4. Probar alias de contraste
    print("\n--- 4. Probando alias de contraste ---")
    proc.contraste(1.5)
    
    # 5. Probar transformaciones personalizadas mediante aplicar_transformacion
    print("\n--- 5. Probando transformación personalizada ---")
    proc.aplicar_transformacion(InvertColorsTransform())
    proc.guardar_resultado(nombre="pajaro_invertido.png", formato="PNG")
    
    # 6. Verificar encadenamientos especiales (doble contraste, doble umbralización, combinaciones)
    print("\n--- 6. Probando encadenamiento de múltiples operaciones del mismo filtro ---")
    # Dos contraste uno seguido del otro
    proc.contraste(1.2).contraste(0.9)
    print("Doble contraste secuencial: OK")
    
    # Dos umbralizaciones una seguida de la otra
    proc.umbralizacion(127).umbralizacion(100)
    print("Doble umbralización secuencial: OK")
    
    # 7. Combinación de funcionalidades después de umbralización sin error
    # (El resultado de umbralizacion es modo "1". Aplicamos brillo, contraste, saturación y redimensionado)
    print("\n--- 7. Probando combinaciones de filtros sobre imagen binarizada (Modo 1) ---")
    proc.ajustar_brillo(1.5) \
        .contraste(1.2) \
        .saturacion(0.8) \
        .redimensionar(200, 200)
    print("Filtros combinados sobre modo 1: OK")
    
    proc.guardar_resultado(nombre="pajaro_binarizado_y_procesado.png", formato="PNG")
    
    # 8. Probar resetear y volver al original
    print("\n--- 8. Probando reseteo general ---")
    proc.resetear()
    proc.redimensionar(250, 250).guardar_resultado(nombre="pajaro_reseteado_chico.webp", formato="WEBP")
    
    print("\n=======================================================")
    print("¡Prueba integral completada exitosamente sin errores!")
    print("=======================================================")

if __name__ == "__main__":
    test_pipeline_completo()
