from PIL import Image, ImageEnhance, ImageOps
import os

class ProcesadorImagen:
    def __init__(self):
        """Punto 1: El objeto nace preparado para recibir una imagen"""
        self.imagen_original = None
        self.imagen_procesada = None
        self.nombre_archivo = ""

    def cargar_imagen(self, ruta_acceso):
        """Punto 1: Entrada de datos"""
        if os.path.exists(ruta_acceso):
            self.imagen_original = Image.open(ruta_acceso)
            # Creamos una copia para no destruir la original durante el proceso
            self.imagen_procesada = self.imagen_original.copy()
            self.nombre_archivo = os.path.basename(ruta_acceso)
            print(f"✅ Imagen '{self.nombre_archivo}' cargada con éxito.")
        else:
            print("❌ Error: La ruta no existe.")

    # --- Punto 2: Técnicas de Procesamiento ---

    def redimensionar(self, ancho=400, alto=400):
        """Estandarización de dimensiones"""
        if self.imagen_procesada:
            # Usamos ImageOps.fit para que recorte y ajuste sin deformar
            self.imagen_procesada = ImageOps.fit(self.imagen_procesada, (ancho, alto), Image.Resampling.LANCZOS)
            print(f"   -> Resizing: OK ({ancho}x{alto})")

    def ajustar_brillo(self, factor=1.0):
        """Ajuste de brillo (1.0 es original, 1.1 es +10%, 0.9 es -10%)"""
        if self.imagen_procesada:
            realzador = ImageEnhance.Brightness(self.imagen_procesada)
            self.imagen_procesada = realzador.enhance(factor)
            print(f"   -> Brillo: Ajustado por factor {factor}")

    def ajustar_contraste(self, factor=1.0):
        """Ajuste de contraste (1.0 es original)"""
        if self.imagen_procesada:
            realzador = ImageEnhance.Contrast(self.imagen_procesada)
            self.imagen_procesada = realzador.enhance(factor)
            print(f"   -> Contraste: Ajustado por factor {factor}")

    def aplicar_marca_agua(self, ruta_logo, opacidad=0.5):
        """Superposición de marca de agua proporcional"""
        if self.imagen_procesada and os.path.exists(ruta_logo):
            with Image.open(ruta_logo) as logo:
                # Hacer el logo proporcional (25% del ancho de la imagen)
                ancho_logo = int(self.imagen_procesada.width * 0.25)
                alto_logo = int(logo.height * (ancho_logo / logo.width))
                logo = logo.resize((ancho_logo, alto_logo), Image.Resampling.LANCZOS)
                
                # Crear capa de transparencia
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')
                
                # Ajustar opacidad del logo
                alpha = logo.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacidad)
                logo.putalpha(alpha)

                # Pegar en esquina inferior derecha
                pos_x = self.imagen_procesada.width - ancho_logo - 20
                pos_y = self.imagen_procesada.height - alto_logo - 20
                
                # Si la imagen base no es RGBA, la convertimos para poder pegar
                if self.imagen_procesada.mode != 'RGBA':
                    self.imagen_procesada = self.imagen_procesada.convert('RGBA')
                
                self.imagen_procesada.paste(logo, (pos_x, pos_y), logo)
                print("   -> Marca de agua: Aplicada")

    def guardar_resultado(self, carpeta_salida="procesadas"):
        """Punto 3: Salida del sistema"""
        if self.imagen_procesada:
            if not os.path.exists(carpeta_salida):
                os.makedirs(carpeta_salida)
            
            nombre_final = os.path.splitext(self.nombre_archivo)[0] + "_editada.webp"
            ruta_final = os.path.join(carpeta_salida, nombre_final)
            
            # Convertir a RGB antes de guardar como WebP (quita canal alpha si existiera)
            final_rgb = self.imagen_procesada.convert("RGB")
            final_rgb.save(ruta_final, "WEBP", quality=90)
            print(f"💾 Guardado en: {ruta_final}")

# --- Punto 4: Uso claro y ejecutable ---

if __name__ == "__main__":
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
