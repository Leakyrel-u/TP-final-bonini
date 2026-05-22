import unittest
from pathlib import Path
import tempfile
import shutil
from PIL import Image
from optilens.io import ImageIO
from optilens.exceptions import ImagenNoEncontradaError

class TestImageIO(unittest.TestCase):
    
    def setUp(self):
        # Crear directorio temporal para pruebas físicas de guardado/cargado
        self.test_dir = Path(tempfile.mkdtemp())
        self.sample_img_path = self.test_dir / "test_sample.png"
        
        # Crear una imagen en memoria simple para guardar
        self.sample_image = Image.new("RGBA", (100, 100), color="blue")
        self.sample_image.save(self.sample_img_path, format="PNG")
        
    def tearDown(self):
        # Eliminar el directorio temporal y sus archivos
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            
    def test_cargar_exito(self):
        """Verifica que se pueda cargar una imagen existente correctamente en memoria."""
        img = ImageIO.cargar(self.sample_img_path)
        self.assertIsNotNone(img)
        self.assertEqual(img.size, (100, 100))
        self.assertEqual(img.mode, "RGBA")
        
    def test_cargar_inexistente_lanza_excepcion(self):
        """Verifica que cargar una ruta inexistente lance ImagenNoEncontradaError."""
        ruta_inexistente = self.test_dir / "no_existe.png"
        with self.assertRaises(ImagenNoEncontradaError):
            ImageIO.cargar(ruta_inexistente)
            
    def test_guardar_png_exito(self):
        """Verifica que se pueda guardar una imagen en formato PNG."""
        carpeta_salida = self.test_dir / "salida"
        nombre_guardado = "imagen_guardada.png"
        
        ruta_resultado = ImageIO.guardar(
            self.sample_image,
            carpeta_salida=carpeta_salida,
            nombre=nombre_guardado,
            formato="PNG"
        )
        
        self.assertTrue(ruta_resultado.exists())
        self.assertEqual(ruta_resultado.name, nombre_guardado)
        
        # Cargar y verificar
        with Image.open(ruta_resultado) as img_cargada:
            self.assertEqual(img_cargada.size, (100, 100))
            self.assertEqual(img_cargada.format, "PNG")
        
    def test_guardar_jpeg_conversion_rgba_a_rgb(self):
        """Verifica que al guardar una imagen RGBA como JPEG se convierta automáticamente a RGB."""
        carpeta_salida = self.test_dir / "salida_jpeg"
        nombre_guardado = "imagen_jpeg.jpg"
        
        ruta_resultado = ImageIO.guardar(
            self.sample_image,  # Es RGBA (tiene canal alfa)
            carpeta_salida=carpeta_salida,
            nombre=nombre_guardado,
            formato="JPEG"
        )
        
        self.assertTrue(ruta_resultado.exists())
        
        # Verificar que la imagen guardada se lea como RGB (JPEG no soporta alfa)
        with Image.open(ruta_resultado) as img:
            self.assertEqual(img.mode, "RGB")

if __name__ == '__main__':
    unittest.main()
