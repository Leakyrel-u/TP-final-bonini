import unittest
from pathlib import Path
import tempfile
import shutil
from PIL import Image
from optilens.exceptions import ParametroInvalidoError, ImagenNoEncontradaError
from optilens.transforms import (
    ResizeTransform,
    BrightnessTransform,
    ContrastTransform,
    SaturationTransform,
    WatermarkTransform,
    ThresholdTransform,
)

class TestTransforms(unittest.TestCase):

    def setUp(self):
        # Crear directorio temporal para el logo de marca de agua
        self.test_dir = Path(tempfile.mkdtemp())
        self.logo_path = self.test_dir / "logo.png"
        
        # Generar un logo de prueba simple en RGBA
        logo = Image.new("RGBA", (40, 40), color=(255, 0, 0, 128))
        logo.save(self.logo_path, format="PNG")
        
        # Imagen base de prueba 200x200 RGB
        self.base_img = Image.new("RGB", (200, 200), color=(100, 100, 100))

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_resize_transform(self):
        """Verifica que ResizeTransform redimensione correctamente a las dimensiones objetivo."""
        transform = ResizeTransform(ancho=100, alto=80)
        img_res = transform.apply(self.base_img)
        
        self.assertEqual(img_res.size, (100, 80))
        
        # Verificar validación de parámetros
        with self.assertRaises(ValueError):
            ResizeTransform(ancho=0, alto=100)

    def test_brightness_transform(self):
        """Verifica que BrightnessTransform modifique los valores de píxeles sin cambiar dimensiones."""
        transform = BrightnessTransform(factor=1.5)
        img_res = transform.apply(self.base_img)
        
        self.assertEqual(img_res.size, self.base_img.size)
        self.assertEqual(img_res.mode, self.base_img.mode)
        
        # Verificar que el brillo haya incrementado de alguna manera en promedio
        original_pixel = self.base_img.getpixel((10, 10))[0]
        bright_pixel = img_res.getpixel((10, 10))[0]
        self.assertGreater(bright_pixel, original_pixel)
        
        # Validar factor fuera de rango
        with self.assertRaises(ParametroInvalidoError):
            BrightnessTransform(factor=4.0)

    def test_contrast_transform(self):
        """Verifica que ContrastTransform aplique el ajuste sin cambiar dimensiones."""
        transform = ContrastTransform(factor=0.8)
        img_res = transform.apply(self.base_img)
        
        self.assertEqual(img_res.size, self.base_img.size)
        
        with self.assertRaises(ParametroInvalidoError):
            ContrastTransform(factor=-0.1)

    def test_saturation_transform(self):
        """Verifica que SaturationTransform funcione adecuadamente."""
        # Imagen colorida
        color_img = Image.new("RGB", (10, 10), color=(200, 50, 50))
        transform = SaturationTransform(factor=0.0)  # Convertir a escala de grises
        img_res = transform.apply(color_img)
        
        # En saturación 0, los canales R, G, B de un píxel deben ser iguales (gris)
        pix = img_res.getpixel((0, 0))
        self.assertEqual(pix[0], pix[1])
        self.assertEqual(pix[1], pix[2])

    def test_watermark_transform_exito(self):
        """Verifica que WatermarkTransform aplique el logotipo sin cambiar las dimensiones de la imagen original."""
        transform = WatermarkTransform(ruta_logo=self.logo_path, opacidad=0.5, escala=0.20)
        img_res = transform.apply(self.base_img)
        
        self.assertEqual(img_res.size, self.base_img.size)
        self.assertEqual(img_res.mode, self.base_img.mode)  # Debe preservar el modo original (RGB)

    def test_watermark_transform_errores(self):
        """Verifica excepciones de WatermarkTransform con rutas o factores erróneos."""
        # Ruta incorrecta
        with self.assertRaises(ImagenNoEncontradaError):
            WatermarkTransform(ruta_logo=self.test_dir / "inexistente.png")
            
        # Factores fuera de rango
        with self.assertRaises(ParametroInvalidoError):
            WatermarkTransform(ruta_logo=self.logo_path, opacidad=1.5)
        with self.assertRaises(ParametroInvalidoError):
            WatermarkTransform(ruta_logo=self.logo_path, escala=0.6)

    def test_threshold_transform(self):
        """Verifica que ThresholdTransform binarice la imagen a 1-bit con blanco y negro puros."""
        transform = ThresholdTransform(valor_umbral=127)
        img_res = transform.apply(self.base_img)
        
        self.assertEqual(img_res.mode, "1")
        self.assertEqual(img_res.size, self.base_img.size)
        
        # Pixeles deben ser 0 (negro) o 255 (blanco) en su valor binario (0 o 1 en modo 1)
        pix_val = img_res.getpixel((5, 5))
        self.assertIn(pix_val, (0, 255, 1))  # Depende de cómo PIL exponga el bit en getpixel

if __name__ == '__main__':
    unittest.main()
