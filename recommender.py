def readMatrix(filename):
    with open(filename, "r") as matriz:
        file = matriz.read()

    lineas = file.split("\n")
    valorMin, valorMax, *valoraciones = (linea.split() for linea in lineas)

    return valoraciones, valorMin, valorMax

ratings, min_val, max_val = readMatrix("matriz.txt")

print(ratings)
print(max_val)
print(min_val)