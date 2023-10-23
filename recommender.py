def readMatrix(filename):
    with open(filename, "r") as matriz:
        file = matriz.read()

    lineas = file.split("\n")
    valorMin, valorMax, *valoraciones = (linea.split() for linea in lineas)

    return valoraciones, valorMin, valorMax

def sameRatedItems(user1, user2):
    commonItemsIndex = []

    for i in range(len(user1)):
        if user1[i] == '-' or user2[i] == '-':
            continue
        else:
            commonItemsIndex.append(i)
    
    return commonItemsIndex

def userAverage(user):
    intRatings = []

    for rating in user:
        if rating != '-':
            intRatings.append(float(rating))
        else:
            continue
    
    return sum(intRatings)/len(intRatings)

def commonItemArrays(user1, user2):
    commonIndex = sameRatedItems(user1, user2)
    user1Float = []
    user2Float = []

    for i in commonIndex:
        user1Float.append(float(user1[i]))
        user2Float.append(float(user2[i]))

    return user1Float, user2Float

def pearsonCorelation(user1, user2):
    user1Ratings, user2Ratings = commonItemArrays(user1, user2)

    sumNumerador = 0
    sumDenominador1 = 0
    sumDenominador2 = 0

    for i in range(len(user1Ratings)):
        sumNumerador += ((user1Ratings[i] - userAverage(user1)) * (user2Ratings[i] - userAverage(user2)))
        sumDenominador1 += ((user1Ratings[i] - userAverage(user1)) ** 2)
        sumDenominador2 += ((user2Ratings[i] - userAverage(user2)) ** 2)

    return (sumNumerador / ((sumDenominador1 ** 0.5) * (sumDenominador2 ** 0.5)))

def pearsonArray(user, matrix):

    pearsonRatings = []

    for otherUser in matrix:
        if user == otherUser:
            continue
        
        pearsonRatings.append(pearsonCorelation(user, otherUser))

    return pearsonRatings


def calculatePredictions(matrix, metrica, numeroVecinos, tipoPrediccion, min_val, max_val):

    for user in matrix:
        if '-' not in user:
            continue

        


    similarity = 0
    return similarity

ratings, min_val, max_val = readMatrix("matriz.txt")

print(pearsonArray(ratings[0], ratings))