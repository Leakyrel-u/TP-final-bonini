import unittest
from pathlib import Path
import tempfile
import shutil
from PIL import Image
from optilens.core import ProcesadorImagen
from optilens.exceptions import ImagenNoCargadaError
from optilens.transforms.base import BaseTransform

# Una clase de transformación personalizada ficticia para validar el OCP
class InvertColorsTransform(BaseTransform):
    def apply(self, imagen: Image.Image) -> Image.Image:
        # Invierte los canales de color
        if imagen.mode == "RGB":
            r, g, b = imagen.split()
            return Image.merge("RGB", (b, g, r))
        return imagen

class TestProcesadorImagen(unittest.TestCase):

    def setUp(self):
        # Crear entorno temporal para pruebas
        self.test_dir = Path(tempfile.mkdtemp())
        self.img_path = self.test_dir / "pajaro_prueba.jpg"
        self.logo_path = self.test_dir / "logo_prueba.png"
        
        # Guardar imágenes físicas de prueba mínimas
        self.original_img = Image.new("RGB", (100, 100), color=(120, 120, 120))
        self.original_img.save(self.img_path, format="JPEG")
        
        self.logo_img = Image.new("RGBA", (20, 20), color=(255, 0, 0, 100))
        self.logo_img.save(self.logo_path, format="PNG")
        
        # Desactivamos verbose para no llenar la consola de pruebas
        self.procesador = ProcesadorImagen(verbose=False)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_operar_sin_cargar_lanza_excepcion(self):
        """Verifica que intentar procesar o guardar sin haber cargado una imagen lance ImagenNoCargadaError."""
        with self.assertRaises(ImagenNoCargadaError):
            self.procesador.redimensionar(50, 50)
            
        with self.assertRaises(ImagenNoCargadaError):
            self.procesador.guardar_resultado(self.test_dir)

    def test_pipeline_fluido_y_guardado(self):
        """Verifica el encadenamiento fluido completo y el guardado de la imagen final."""
        salida_dir = self.test_dir / "salida_final"
        
        # Ejecutar pipeline encadenado
        ruta_salida = (
            self.procesador
            .cargar_imagen(self.img_path)
            .redimensionar(50, 50)
            .ajustar_brillo(1.2)
            .ajustar_contraste(0.9)
            .saturacion(1.1)
            .aplicar_marca_agua(self.logo_path, opacidad=0.4, escala=0.1)
            .guardar_resultado(carpeta_salida=salida_dir, nombre="pajaro_editado.webp", formato="WEBP")
        )
        
        self.assertTrue(Path(ruta_salida).exists())
        self.assertEqual(self.procesador.imagen_procesada.size, (50, 50))
        
    def test_alias_contraste(self):
        """Verifica que el método alias contraste funcione idénticamente a ajustar_contraste."""
        self.procesador.cargar_imagen(self.img_path)
        self.procesador.contraste(1.5)
        self.assertEqual(self.procesador.imagen_procesada.size, (100, 100))

    def test_resetear(self):
        """Verifica que el método resetear restaure la imagen al estado original cargado."""
        self.procesador.cargar_imagen(self.img_path)
        
        # Modificar imagen
        self.procesador.redimensionar(20, 20)
        self.assertEqual(self.procesador.imagen_procesada.size, (20, 20))
        
        # Resetear
        self.procesador.resetear()
        self.assertEqual(self.procesador.imagen_procesada.size, (100, 100))
        
    def test_aplicar_transformacion_personalizada_ocp(self):
        """Verifica que se pueda aplicar una transformación externa sin modificar la librería (OCP)."""
        self.procesador.cargar_imagen(self.img_path)
        
        # Obtener pixel central original
        pixel_original = self.procesador.imagen_procesada.getpixel((50, 50))
        
        # Aplicar inversión de color externa
        self.procesador.aplicar_transformacion(InvertColorsTransform())
        
        # Obtener pixel central procesado
        pixel_procesado = self.procesador.imagen_procesada.getpixel((50, 50))
        
        # Verificar que el canal R y B se hayan invertido
        self.assertEqual(pixel_procesado[0], pixel_original[2])
        self.assertEqual(pixel_procesado[2], pixel_original[0])

if __name__ == '__main__':
    unittest.main()
