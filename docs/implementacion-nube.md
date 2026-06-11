1. ¿Qué pasa si se encadenan dos llamadas de umbralización una seguida de la otra?
Resultado: Corre perfectamente y no falla.
Explicación: La primera llamada convierte la imagen a escala de grises (L) y luego a modo de 1 bit (1). La segunda llamada convierte la imagen del modo 1 a L (cuyos píxeles ahora son únicamente 0 o 255), evalúa la condición del nuevo umbral y vuelve a retornar una imagen en modo 1. Funciona sin errores.

2. ¿Qué pasa si se encadenan dos llamadas de contraste una seguida de la otra?
Se aplica el ajuste de contraste secuencial sobre los píxeles de la imagen resultante del paso anterior de forma acumulativa y lineal.

3. Aplicar el mismo filtro múltiples veces y combinaciones sin generar error.
Para garantizar que se puedan realizar cualquier tipo de combinaciones (como aplicar contraste, ajustar_brillo o saturacion después de una binarización umbralizacion), se modificaron las transformaciones para que conviertan temporalmente la imagen de modo 1 a L antes de la operación de realce, y la regresen a modo 1 al finalizar. De esta manera, ninguna combinación de filtros genera errores de modo de imagen.

* Para implementar estos cambios y que no afecte el proceso se implementa los siguientes métodos

Historial de Cambios en Memoria (Deshacer/Rehacer):
Se añadió el parámetro max_cambios: int = 5 al inicializador de 
ProcesadorImagen

* Se implementaron los métodos deshacer()  y r ehacer(): El historial se borra al cargar una nueva imagen (cargar_imagen) o reiniciar la imagen (resetear).
Compatibilidad en Transformaciones: Modificación de contrast.py / brightness.py  y saturation.py para tolerar y preservar el modo 1.

## Pruebas y Ejemplos:
Se agregaron pruebas unitarias específicas en test_history.py y se agrega el archivo  test_all_features.py para que cubra todas las funcionalidades (incluyendo deshacer, rehacer, doble contraste, doble umbralización y combinaciones en modo 1).

