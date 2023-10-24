import argparse

def Parser():
  parser = argparse.ArgumentParser(description="Parser para el sistema de recomendación")

  parser.add_argument('-f', '--file', nargs='?',required=True, type=str, help='Ruta del archivo de matriz de entrada')

  parser.add_argument('-o', '--output', type=str, default="output.txt",help='Nombre archivo de salida (opcional)', required=False)

  parser.add_argument('-n', '--neighbours', type=int, help='Numero de vecinos a considerar', required=True)

  grupoMetrica = parser.add_mutually_exclusive_group(required=True)
  grupoMetrica.add_argument('-p','--pearson', action='store_true', help='Correlacion de Pearson')
  grupoMetrica.add_argument('-c','--cosine',action='store_true', help='Distancia coseno')
  grupoMetrica.add_argument('-e', '--euclidean', action='store_true', help='Distancia euclídea')


  grupoPrediccion = parser.add_mutually_exclusive_group(required=True)
  grupoPrediccion.add_argument('-s', '--simple', action='store_true', help='Tipo de predicción simple')
  grupoPrediccion.add_argument('-m', '--media', action='store_true', help='Tipo de predicción distancia con la media')

  return parser.parse_args()