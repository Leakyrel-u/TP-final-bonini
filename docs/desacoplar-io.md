
# Desacoplamiento e Implementación I/O:

* Se diseña y crea la jerarquía de cargadores (CargadorImagen, CargadorLocal, CargadorUrl) y guardadores (GuardadorImagen, GuardadorLocal, GuardadorNube) en io.py.

* Implementa la descarga multiplataforma de imágenes en red y la simulación/validación de URLs y rutas en disco.
Integración y Encadenamiento en ProcesadorImagen:Se cambia core.py para utilizar los nuevos cargadores/guardadores dinámicamente según el formato de la dirección (detectando esquemas HTTP/HTTPS).
Actualiza guardar_resultado para que retorne self (permitiendo chaining completo) y registre la ubicación final en el atributo ultimo_guardado.
El archivo  init.py  para exportar las nuevas clases de forma pública.

## Pruebas y Verificación:
Se añade validación de cargas simuladas de red, guardado en nube e invalidación de formatos a nivel local/remoto en test_core.py  y test_io.py.
Se verifica la suite completa de 22 pruebas con éxito, y comprueba que los ejemplos integrales se ejecutan correctamente.