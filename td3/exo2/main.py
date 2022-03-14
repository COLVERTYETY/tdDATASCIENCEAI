# Apprentissage supervisé - k plus proches voisins
from cgi import test
import csv

# Fonction de deepcopy de listes imbriquées de niveau k
def deepcopy(l: list, k:int):
    if k == 0:
        return l
    else:
        return [deepcopy(elem, k-1) for elem in l]

# Le dataset contient une liste de donnée d'apprentissage
# chaque donnée y est représenté par une liste de spécifications:
# [Sepal length, Sepal width, Petal length, Petal width, Species]
# On cherche à identifier la plante dont les spécifications sont données par
# [Sepal length, Sepal width, Petal length, Petal width]
def findFlower(specs: list, dataset:list[list], k:int):
    # liste ordonnée des distances entre les données d'apprentissage et la donnée
    # à identifier
    distances = []
    # On parcours le dataset
    for data in dataset:
        # On calcule la distance entre la donnée à identifier et la donnée d'apprentissage
        distance = 0
        for i in range(len(specs)):
            distance += (specs[i] - data[i]) ** 2
        # On ajoute la distance et la donnée dont elle est issue à la liste des distances
        distances.append((distance, data[-1]))
    # On trie les distances par ordre croissant
    distances.sort(key= lambda x: x[0])
    # On récupère les k plus proches voisins
    k_neighbors = distances[:k]
    # On récupère les espèces des k plus proches voisins
    species = {}
    for neighbor in k_neighbors:
        specie = neighbor[1]
        if specie in species:
            species[specie] += 1
        else:
            species[specie] = 1
    # On récupère l'espèce la plus représenté
    max_specie = None
    max_count = 0
    for specie in species:
        if species[specie] > max_count:
            max_specie = specie
            max_count = species[specie]
    # On retourne l'espèce la plus représenté
    return max_specie
    
    



if __name__ == '__main__':
    ## Importer les données au format CSV depuis IA3-ml_data_iris.txt
    raw_data = []
    with open('IA3-ml_data_iris.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            raw_data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3]), row[4]])
    # On place la moitié des données dans le dataset d'apprentissage
    training_data = []
    testing_data = []
    for i in range(len(raw_data)):
        if i % 2 == 0:
            training_data.append(raw_data[i])
        else:
            testing_data.append(raw_data[i])
    verification_dataset = deepcopy(training_data, 2)
    # On retire le nom de l'espèce des données de test
    for data in testing_data:
        data.pop()

    wrong_ones = 0
    print('k = ', end="")
    k=int(input())
    for i in range(len(testing_data)):
        true_specie = verification_dataset[i][-1]
        predicted_specie = findFlower(testing_data[i], training_data, k)
        if true_specie != predicted_specie:
            wrong_ones += 1
            print("Erreur: la donnée de test", testing_data[i], "est de l'espèce", true_specie, "mais elle à été prédit comme", predicted_specie)

    print("Taux d'erreur: ", (wrong_ones / len(testing_data))*100, '%')
