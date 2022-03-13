# Implémentation Python de l'algorithme Apriori
def apriori(transactions, min_occurences):
    # 1. créer la liste vide itemsets_frequent
    frequent_itemsets = []
    #    (1) pour chaque élément dans la liste des transactions
    for item in transactions:
        #    (2) pour chaque itemset dans la liste itemsets_frequent
        for itemset in frequent_itemsets:
            #    (3) si l'élément est présent dans l'itemset
            if item in itemset:
                #    (4) incrémenter le compteur de l'itemset
                itemset[1] += 1
                #    (5) arrêter la boucle
                break
        #    (6) si la boucle ne s'est pas arrêté (l'élément n'est pas présent dans l'itemset)
        else:
            #    (7) créer un nouvel itemset avec l'élément et initialiser le compteur à 1
            itemset = [item, 1]
            #    (8) ajouter l'itemset à la liste itemsets_frequent
            frequent_itemsets.append(itemset)
    # 3. trier la liste itemsets_frequent par ordre décroissant de compteur
    frequent_itemsets.sort(key=lambda x: x[1], reverse=True)
    # 4. retirer les itemsets dont le compteur est inférieur à min_occurences
    frequent_itemsets = [itemset for itemset in frequent_itemsets if itemset[1] >= min_occurences]
    # 5. retourner la liste itemsets_frequent
    return frequent_itemsets

if __name__ == "__main__":
    transactions = [1,2,5,1,3,5,1,2,1,2,3,4,5,1,2,4,5,2,3,5,1,5]
    print(apriori(transactions, 3))