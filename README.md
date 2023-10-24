# Recomendador basado en filtrado colaborativo por usuario

Este es un programa escrito enteramente en `Python` que simula un recomendador basado en filtrado colaborativo. Recibe como entrada una matriz incompleta con un formato específico, y la rellena con las predicciones basadas en el filtrado colaborativo por usuario.

## Instrucciones

Para el correcto funcionamiento del programa solo es necesario tener instalado `Python 3`. Esto se puede hacer en sistemas Linux con el siguiente comando:
```bash
sudo apt install python3
```

La ejecución se efectúa con este comando:
```bash
python3 main.py [argumentos]
```

Para el correcto funcionamiento del programa se le deben pasar varios argumentos. Éstos se pueden ver con el comando:
```bash
python3 main.py -h
```

## Descripción del código

El programa está dividido en 2 partes. Los módulos, dentro de la carpeta `modules`, y el `main`. El programa tiene 2 módulos fundamentales, el primero llamado `functions` contiene las funciones que hacen que el programa ejecute correctamente. Éstas hacen los cálculos correspondientes. Desde el main solo se llama a la funcion `calculatePredictions`, que es la que rellena la matriz haciendo uso de la función `similarNeighbours`, la cual es la encargada de seleccionar los vecinos más próximos según el método de correlación que estemos usando. 

La función `similarNeighbours` llama a una de las 3 funciones:
- **`pearsonArray`**
- **`cosineArray`**
- **`euclideanArray`**

Estas funciones son las encargadas de calcular todas los índices de similitud de un usuario concreto con respecto a los demás. En ellas se comprueba y se filtra a los usuarios que no son compatibles para el cálculo, y devuelve un array de tuplas. El primer elemento de cada tupla es el array del usuario que dio lugar al cálculo, y el segundo elemento es el valor de la correlación. 

Esta lista de tuplas se ordena de mayor a menor y se cogen los `n` primeros miembros de ésta, siendo `n` el número de vecinos estipulado en la ejecución. Dando lugar a una lista con los usuarios más similares al que estamos evaluando.

Ésta lista se crea para cada uno de los usuarios que tienen valores vacíos que vamos a predecir, y se usa para calcular los valores que vamos a predecir. Se calcula para cada usuario una lista de los índices que no tienen valoración, y éstos índices se utilizan en un bucle para hacer el calculo de cada uno.

El segundo módulo, llamado `myParser`, es el parser de los argumentos que entran por línea de comandos. Siguiendo los convenios del estilo POSIX.

## Ejemplo de uso

La salida del programa consiste en un archivo de texto (por defecto *output.txt*, aunque se puede especificar con -o), y una salida por terminal de lo estipulado en el enunciado. Para este ejemplo, usaremos la matriz proporcionada en el enunciado, que en nuestro caso está en el archivo de texto `matriz.txt` dentro del directorio `data`. La ejecución para este caso podría ser la siguiente, utilizando **Pearson** y tipo de predicción **Distancia con la media**:
```bash
python3 main.py -pm -f matriz.txt -n 2
```

Los argumentos son intercambiables y agrupables según los convenios de estilo POSIX proporcionados en el enunciado.