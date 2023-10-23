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


def pearsonCorelation(user1, user2): # Devuelve la correlacion de Pearson entre dos usuarios
    user1Ratings, user2Ratings = commonItemArrays(user1, user2)

    sumNumerador = 0
    sumDenominador1 = 0
    sumDenominador2 = 0

    for i in range(len(user1Ratings)):
        sumNumerador += ((user1Ratings[i] - userAverage(user1)) * (user2Ratings[i] - userAverage(user2)))
        sumDenominador1 += ((user1Ratings[i] - userAverage(user1)) ** 2)
        sumDenominador2 += ((user2Ratings[i] - userAverage(user2)) ** 2)

    return (sumNumerador / ((sumDenominador1 ** 0.5) * (sumDenominador2 ** 0.5)))


def pearsonArray(user, matrix): # Devuelve un array de tuplas de correlaciones de Pearson junto con el usuario correspondiente con el resto de usuarios de la matriz proporcionada, falta comprobacion de que el usuario esta en la matriz

    pearsonRatings = []

    for otherUser in matrix:
        if user == otherUser:
            continue

        correlation = pearsonCorelation(user, otherUser)
        pearsonRatings.append((otherUser, correlation))

    return pearsonRatings


def similarNeighbours(user, matrix, metrica, numeroVecinos): # Devuelve un array de los vecinos más similares segun la metrica elegida y el numero de vecinos estipulado
    neighbours = []

    missing_indexes = [(i) for i in range(len(user)) if user[i] == '-']

    matrizSinIncompatibles = []

    for otherUser in matrix: # Quitamos de la matriz los otros usuarios que no tengan valorados los items que intentamos predecir del usuario
        for index in missing_indexes:
            if otherUser[index] != '-':
                matrizSinIncompatibles.append(otherUser)


    if metrica == 'pearson':
        corrArray = sorted(pearsonArray(user, matrizSinIncompatibles), key=lambda x: x[1], reverse=True)
        for i in range(numeroVecinos):
            neighbours.append(corrArray[i])
    
    return neighbours


def calculatePredictions(matrix, metrica, numeroVecinos, tipoPrediccion, min_val, max_val): # Funcion final que devolverá la matriz rellena con las predicciones dependiendo del método usado

    for user in matrix:
        if '-' not in user:
            continue

        missing_indexes = [(i) for i in range(len(user)) if user[i] == '-']

        if tipoPrediccion == 'simple':
            sumNumerador = 0
            sumDenominador = 0
            
            for index in missing_indexes:
                for otherUser in similarNeighbours(user, matrix, metrica, numeroVecinos):
                    sumNumerador += (otherUser[1] * float(otherUser[0][index]))
                    sumDenominador += abs(otherUser[1])
                
                prediction = sumNumerador / sumDenominador

                user[index] = round(prediction, 2)

    return matrix

ratings, min_val, max_val = readMatrix("matriz.txt")

print(calculatePredictions(ratings, 'pearson', 2, 'simple', min_val, max_val))