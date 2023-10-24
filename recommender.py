import math


def readMatrix(filename): # Lee la matriz con el formato adecuado, la primera linea como valor minimo, la segunda como valor maximo y el resto de lineas como usuarios individuales
    with open(filename, "r") as matriz:
        file = matriz.read()

    lineas = file.split("\n")
    valorMin, valorMax, *valoraciones = (linea.split() for linea in lineas)

    return valoraciones, valorMin, valorMax


def sameRatedItems(user1, user2): # Devuelve un array con los indices de los items que ambos usuarios han valorado
    commonItemsIndex = []

    for i in range(len(user1)):
        if (user1[i] == '-') or (user2[i] == '-'):
            continue
        else:
            commonItemsIndex.append(i)
    
    return commonItemsIndex


def userAverage(user): # Devuelve la media del usuario sin contar los valores vacios con '-'
    intRatings = []

    for rating in user:
        if rating != '-':
            intRatings.append(float(rating))
        else:
            continue
    
    return sum(intRatings)/len(intRatings)


def commonItemArrays(user1, user2): # Devuelve los arrays de los items valorados por ambos usuarios como floats para calcular con ellos
    commonIndex = sameRatedItems(user1, user2)
    user1Float = []
    user2Float = []

    for i in commonIndex:
        user1Float.append(float(user1[i]))
        user2Float.append(float(user2[i]))

    return user1Float, user2Float


def pearsonCorelation(user1, user2): # Devuelve la correlacion de Pearson entre dos usuarios, hagan funciones similares para las otras dos con la formula de las diapos
    user1Ratings, user2Ratings = commonItemArrays(user1, user2)

    sumNumerador = 0
    sumDenominador1 = 0
    sumDenominador2 = 0

    for i in range(len(user1Ratings)):
        sumNumerador += ((user1Ratings[i] - userAverage(user1)) * (user2Ratings[i] - userAverage(user2)))
        sumDenominador1 += ((user1Ratings[i] - userAverage(user1)) ** 2)
        sumDenominador2 += ((user2Ratings[i] - userAverage(user2)) ** 2)

    return (sumNumerador / ((sumDenominador1 ** 0.5) * (sumDenominador2 ** 0.5)))

# Función para calcular la distancia del coseno entre dos usuarios
def cosineDistance(user1, user2):
    user1Ratings, user2Ratings = commonItemArrays(user1, user2)

    dotProduct = sum(user1Ratings[i] * user2Ratings[i] for i in range(len(user1Ratings)))
    magnitudeUser1 = math.sqrt(sum(user1Ratings[i] ** 2 for i in range(len(user1Ratings))))
    magnitudeUser2 = math.sqrt(sum(user2Ratings[i] ** 2 for i in range(len(user2Ratings))))

    if magnitudeUser1 == 0 or magnitudeUser2 == 0:
        return 0.0

    return dotProduct / (magnitudeUser1 * magnitudeUser2)


# Función para calcular la distancia euclidiana entre dos usuarios
def euclideanDistance(user1, user2):
    user1Ratings, user2Ratings = commonItemArrays(user1, user2)

    squaredDifferences = [(user1Ratings[i] - user2Ratings[i]) ** 2 for i in range(len(user1Ratings))]
    euclidean = math.sqrt(sum(squaredDifferences))

    return euclidean


def cosineArray(user, matrix):
    cosineRatings = []

    for otherUser in matrix:
        if user == otherUser:
            continue

        distance = cosineDistance(user, otherUser)
        cosineRatings.append((otherUser, distance))

    return cosineRatings


def euclideanArray(user, matrix):
    euclideanRatings = []

    for otherUser in matrix:
        if user == otherUser:
            continue

        distance = euclideanDistance(user, otherUser)
        euclideanRatings.append((otherUser, distance))

    return euclideanRatings


def pearsonArray(user, matrix): # Devuelve un array de tuplas de correlaciones de Pearson junto con el usuario correspondiente con el resto de usuarios de la matriz proporcionada, falta comprobacion de que el usuario esta en la matriz

    pearsonRatings = []

    for otherUser in matrix:
        if user == otherUser:
            continue

        correlation = pearsonCorelation(user, otherUser)
        pearsonRatings.append((otherUser, correlation))

    return pearsonRatings # Cada elemento del array es la lista de valoraciones del usuario como primer elemento y el segundo elemento la correlacion con el usuario original


def similarNeighbours(user, matrix, metrica, numeroVecinos):
    neighbours = []

    missing_indexes = [(i) for i in range(len(user)) if user[i] == '-']

    matrizSinIncompatibles = []

    for otherUser in matrix:
        for index in missing_indexes:
            if otherUser[index] != '-':
                matrizSinIncompatibles.append(otherUser)

    if metrica == 'pearson':
        corrArray = sorted(pearsonArray(user, matrizSinIncompatibles), key=lambda x: x[1], reverse=True)
        for i in range(numeroVecinos):
            neighbours.append(corrArray[i])
    elif metrica == 'cosine':  
        cosArray = sorted(cosineArray(user, matrizSinIncompatibles), key=lambda x: x[1], reverse=True)
        for i in range(numeroVecinos):
            neighbours.append(cosArray[i])
    elif metrica == 'euclidean':
        eucliArray = sorted(euclideanArray(user, matrizSinIncompatibles), key=lambda x: x[1])
        for i in range(numeroVecinos):
            neighbours.append(eucliArray[i])
    return neighbours



def calculatePredictions(matrix, metrica, numeroVecinos, tipoPrediccion, min_val, max_val):
    for user in matrix:
        if '-' not in user:
            continue

        missing_indexes = [(i) for i in range(len(user)) if user[i] == '-']

        if tipoPrediccion == 'simple':
            sumNumerador = 0
            sumDenominador = 0

            for index in missing_indexes:
                neighbors = similarNeighbours(user, matrix, metrica, numeroVecinos)
                for otherUser in neighbors:
                    sumNumerador += (otherUser[1] * float(otherUser[0][index]))
                    sumDenominador += abs(otherUser[1])

            prediction = sumNumerador / sumDenominador
            user[index] = round(prediction, 2)

        elif tipoPrediccion == 'media':
            sumNumerador = 0
            sumDenominador = 0

            for index in missing_indexes:
                neighbors = similarNeighbours(user, matrix, metrica, numeroVecinos)
                for otherUser in neighbors:
                    sumNumerador += (otherUser[1] * (float(otherUser[0][index]) - userAverage(otherUser[0])))
                    sumDenominador += abs(otherUser[1])

            prediction = userAverage(user) + (sumNumerador / sumDenominador)
            user[index] = round(prediction, 2)

    return matrix

# Main para testear, comprueben con el otro archivo de matriz2.txt también que seguro lo pedirá en clase y en la corrección

ratings, min_val, max_val = readMatrix("matriz2.txt")

print(calculatePredictions(ratings, 'cosine', 2, 'media', min_val, max_val))
