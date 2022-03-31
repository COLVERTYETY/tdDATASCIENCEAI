# rapport Algorithme génétique

## 1. Quelle est la taille de l'espace de recherche ?

chaque parametre appartient à l'interval [-100, 100].
On remarque que P3 et p6 sont le déphasage des signaux et appartiennent donc à [0, 2*pi].

donc l'espace de recherche est:

    p1*p2*p3*p4*p5*p6 = 200*200*2*pi*200*200*2*pi
    = 63165468167
    = ~6.3e+10

## 2. Quelle est votre fonction de fitness?

On sépare le problème en 2 morceau: On cherche un groupe d'individu qui opptimise l'erreur en X et un autre groupe qui optimise l'erreur en Y.
On cherche donc une fitness en X (*fitnessX*) et une autre fitness en Y (*fitnessY*).

La meilleure solution du problème est donc composé du meilleur individu de X et du meilleur individu de Y.

soit *k* un individu du groupe optimisant X avec gènes *kp1*,*kp2*,*kp3*.\
soit *l* un individu du groupe optimisant Y avec gènes *lp4*,*lp5*,*lp6*.

    pour chaque point j du dataset avec jt, jx et jy ses coordonnées:

        fitnessX = abs(jx-kp1*sin(kp2*jt + kp3))
        fitnessY = abs(jy-kp4*sin(kp5*jt + kp6))
    
    fitnessX = fitnessX/Npoint
    fitnessY = fitnessY/Npoint
    fitnessX = fitnessX**4
    fitnessY = fitnessY**4

On effectue donc la moyenne de l'absolue de l'erreur en chaque coordonnées, élevé au puissance 4.

## 3. Décrivez les opérateurs mis en œuvre (mutation, croissement)?

qsdqsdqdqsdqsdqd

## 4.  Décrivez votre processus de sélection.


La sélection est effectué par un tirage sans remise de variable aléatoir où chaque individu à une probabilité de passer à l'étape suivante:

    p = 1/(fitness de l'individu)/(somme des fitness)

## 5. Quel est la taille de votre population, combien de générations sont n´ecessaires avant de converger vers une solution stable?

voici un graph de l'évolution de la fitness en fonction des générations 
pour une population de 5000 individu sur X et 5000 sur Y:

    temps total:= 50.33703351020813 s
    temps moyen par génération:= 0.010065393623316963 s

![image](./evolution%20across%20time.png)

en bleu claire l'écart entre la pire et la meilleure fitness.
en bleu foncé la fitness moyenne.
la fitness moyenne reste presque constante car les individu aléatoires ont tendance à être très mauvais.

On remarque que la stabilisation de la meilleure loss est du à la stabilisation du taux de mutation.

On remarque que la loss la plus faible est la meilleur et que elle converge après **200** generations. ce qui équivaut à 2s.

voici un autre graph interessant:

![image](./log%20of%20lof.png)

bleu foncé est meilleur.
On observe comment les meilleurs deviennent vraiment meilleur et comment les individus aléatoires et trops de mutations sont très mauvais.


## 6. Combien de temps votre programme prend en moyenne (sur plusieurs runs)?

