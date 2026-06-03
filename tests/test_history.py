import unittest
from pathlib import Path
import tempfile
import shutil
from PIL import Image
from optilens.core import ProcesadorImagen

class TestHistorialProcesador(unittest.TestCase):

    def setUp(self):
        # Crear entorno temporal para pruebas
        self.test_dir = Path(tempfile.mkdtemp())
        self.img_path = self.test_dir / "pajaro_prueba.jpg"
        
        # Guardar imagen física de prueba mínima
        self.original_img = Image.new("RGB", (100, 100), color=(120, 120, 120))
        self.original_img.save(self.img_path, format="JPEG")
        
        # Desactivamos verbose para no llenar la consola de pruebas
        self.procesador = ProcesadorImagen(verbose=False, max_cambios=3)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_deshacer_y_rehacer_basico(self):
        """Verifica que se puedan deshacer y rehacer cambios básicos."""
        self.procesador.cargar_imagen(self.img_path)
        
        # Estado inicial (100, 100)
        self.assertEqual(self.procesador.imagen_procesada.size, (100, 100))
        
        # Aplicar redimensionado
        self.procesador.redimensionar(50, 50)
        self.assertEqual(self.procesador.imagen_procesada.size, (50, 50))
        
        # Deshacer -> Volver a (100, 100)
        self.procesador.deshacer()
        self.assertEqual(self.procesador.imagen_procesada.size, (100, 100))
        
        # Rehacer -> Volver a (50, 50)
        self.procesador.rehacer()
        self.assertEqual(self.procesador.imagen_procesada.size, (50, 50))

    def test_max_cambios_historial(self):
        """Verifica que el historial no supere el límite de max_cambios."""
        # Creamos procesador con límite de 2 cambios
        procesador = ProcesadorImagen(verbose=False, max_cambios=2)
        procesador.cargar_imagen(self.img_path)
        
        # Aplicar 3 transformaciones secuenciales
        procesador.redimensionar(80, 80)    # Cambio 1
        procesador.redimensionar(60, 60)    # Cambio 2
        procesador.redimensionar(40, 40)    # Cambio 3
        
        self.assertEqual(procesador.imagen_procesada.size, (40, 40))
        
        # Deshacer 1 -> (60, 60)
        procesador.deshacer()
        self.assertEqual(procesador.imagen_procesada.size, (60, 60))
        
        # Deshacer 2 -> (80, 80)
        procesador.deshacer()
        self.assertEqual(procesador.imagen_procesada.size, (80, 80))
        
        # Deshacer 3 -> No debería poder deshacer más (límite superado)
        procesador.deshacer()
        self.assertEqual(procesador.imagen_procesada.size, (80, 80))

    def test_cargar_imagen_resetea_historial(self):
        """Verifica que cargar una nueva imagen limpia los historiales."""
        self.procesador.cargar_imagen(self.img_path)
        self.procesador.redimensionar(50, 50)
        
        # Hay 1 cambio en el historial de deshacer
        self.assertEqual(len(self.procesador._historial_deshacer), 1)
        
        # Cargar la misma imagen limpia el historial
        self.procesador.cargar_imagen(self.img_path)
        self.assertEqual(len(self.procesador._historial_deshacer), 0)
        self.assertEqual(len(self.procesador._historial_rehacer), 0)

    def test_resetear_resetea_historial(self):
        """Verifica que el método resetear limpie los historiales."""
        self.procesador.cargar_imagen(self.img_path)
        self.procesador.redimensionar(50, 50)
        self.procesador.deshacer()
        
        # Tenemos estados en los historiales
        self.assertEqual(len(self.procesador._historial_deshacer), 0)
        self.assertEqual(len(self.procesador._historial_rehacer), 1)
        
        self.procesador.resetear()
        self.assertEqual(len(self.procesador._historial_deshacer), 0)
        self.assertEqual(len(self.procesador._historial_rehacer), 0)

    def test_cambio_nuevo_limpia_rehacer(self):
        """Verifica que aplicar una nueva transformación limpie el historial de rehacer."""
        self.procesador.cargar_imagen(self.img_path)
        self.procesador.redimensionar(80, 80)
        self.procesador.deshacer()
        
        self.assertEqual(len(self.procesador._historial_rehacer), 1)
        
        # Aplicar nueva transformación
        self.procesador.redimensionar(70, 70)
        self.assertEqual(len(self.procesador._historial_rehacer), 0)

if __name__ == '__main__':
    unittest.main()
