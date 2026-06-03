from PIL import Image
import numpy as np
from .base import BaseTransform
from typing import Literal


class WienerRestorationTransform(BaseTransform):
    """Restauración de imágenes usando filtro de Wiener"""

    def apply(
        self,
        imagen: Image.Image,
        degradation_type: Literal["gaussian", "motion"] = "gaussian",
        gaussian_sigma: float = 3.0,
        motion_size: int = 15,
        motion_angle: float = 0,
        K: float = 0.01,
    ) -> Image.Image:
        """
        Restaura una imagen degradada usando deconvolución de Wiener.

        Args:
            image: Imagen PIL degradada
            degradation_type: 'gaussian' o 'motion'
            gaussian_sigma: Sigma para blur Gaussiano
            motion_size: Longitud del motion blur
            motion_angle: Ángulo del motion blur en grados
            K: Parámetro de regularización (relación ruido/señal inversa)

        Returns:
            Imagen PIL restaurada
        """
        # Convertir a escala de grises y a float
        gray = imagen.convert("L")
        img_array = np.array(gray, dtype=np.float32) / 255.0

        rows, cols = img_array.shape

        # Crear PSF (Point Spread Function) en el dominio de frecuencia
        if degradation_type == "gaussian":
            h = self._create_gaussian_psf(rows, cols, gaussian_sigma)
        elif degradation_type == "motion":
            h = self._create_motion_psf(rows, cols, motion_size, motion_angle)
        else:
            raise ValueError(f"Tipo de degradación '{degradation_type}' no soportado")

        # Transformada de Fourier de la imagen y la PSF
        G = np.fft.fft2(img_array)
        H = np.fft.fft2(h)

        # Aplicar filtro de Wiener
        H_conj = np.conj(H)
        H_abs_sq = np.abs(H) ** 2

        # Fórmula de Wiener: F = (H* / (|H|^2 + K)) * G
        F_hat = (H_conj / (H_abs_sq + K)) * G

        # Transformada inversa
        f_restored = np.fft.ifft2(F_hat)
        f_restored = np.abs(f_restored)

        # Normalizar
        f_restored = (
            (f_restored - f_restored.min())
            / (f_restored.max() - f_restored.min())
            * 255
        )

        return self.numpy_to_pil(f_restored.astype(np.uint8))

    def _create_gaussian_psf(self, rows: int, cols: int, sigma: float) -> np.ndarray:
        """Crea PSF Gaussiana normalizada"""
        y, x = np.ogrid[:rows, :cols]
        center_y, center_x = rows // 2, cols // 2

        psf = np.exp(-((x - center_x) ** 2 + (y - center_y) ** 2) / (2 * sigma**2))
        return psf / psf.sum()

    def _create_motion_psf(
        self, rows: int, cols: int, size: int, angle: float
    ) -> np.ndarray:
        """Crea PSF de movimiento lineal"""
        psf = np.zeros((rows, cols))
        center_y, center_x = rows // 2, cols // 2

        # Convertir ángulo a radianes
        angle_rad = np.deg2rad(angle)

        # Crear línea
        for i in range(size):
            x_offset = int(center_x + i * np.cos(angle_rad))
            y_offset = int(center_y + i * np.sin(angle_rad))

            if 0 <= x_offset < cols and 0 <= y_offset < rows:
                psf[y_offset, x_offset] = 1

        # Normalizar
        return psf / psf.sum()
