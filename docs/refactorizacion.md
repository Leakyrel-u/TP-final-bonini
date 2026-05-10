 Lo removí del archivo main.py 
 ```
  # 1. Instanciar nuestro mini-pipeline


    pipeline = ProcesadorImagen()
    
    # 2. Cargar una imagen (Punto 1)
    pipeline.cargar_imagen("producto.jfif") 
    
    # 3. Aplicar transformaciones (Punto 2)
    pipeline.redimensionar(400 , 400)
    pipeline.ajustar_brillo(1.10)     # +10% de brillo
    pipeline.ajustar_contraste(0.90)  # -10% de contraste
    pipeline.aplicar_marca_agua("logo.png", opacidad=0.3)
    
    # 4. Obtener salida (Punto 3)
    pipeline.guardar_resultado()

from PIL import Image
from IPython.display import display

# Ruta de la imagen procesada
ruta_imagen_procesada = "procesadas/producto_editada.webp"

# Cargar la imagen en una variable
imagen_final = Image.open(ruta_imagen_procesada)

# Mostrar la imagen
print(f"Mostrando la imagen: {ruta_imagen_procesada}")
display(imagen_final)
 ```

