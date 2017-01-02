# Réseaux de neurones

### Remarques

Au sein du programme est effectué un abus de langage. Il est considéré ici 
une *couche d'entrée*, une ou plusieurs *couches cachées* et finalement une 
*couche de sortie*.
Dans l'implémentation du problème, la *couche d'entrée* devrait contenir 
l'input, c'est à dire les pixels de l'image, mais elle fonctionne ici comme 
une *couche cachée*.
Les chiffres donnés par la suite sur le nombre de *couches cachées* pour un 
paramètrage satisfaisant devraient donc être incrémentées de **1** pour 
inclure la *fausse couche d'entrée*.

## 1. Codage de l'algorithme

Paramètrage satisfaisant :

- Nombre de neurones pour la couche d'entrée : **10**
- Nombre de neurones par couche cachées : **10**
- Nombre de neurones pour la couche de sortie : **10**
- Itérations d'apprentissage : **100000**
- Itérations de test : **1000**
- Pas d'apprentissage : **0.3**
- Nombre de couches : 1 (ou 2 en comptant la couche d'entrée)

Pour un pourcentage d'erreur de **10.1 %**

## 2. Etude de l'algorithme

### Résultats

Avec la base **mnist.pkl.gz**, qui contient tous les chiffres :

- 13.4 %
- 11.6 %
- 11.0 %

Soit une moyenne de 12 % d'erreurs.

Avec la base **mnist0-4.pkl.gz**, qui contient uniquement les chiffres de 0 à 4 :

- 2.8 %
- 2.9 %
- 2.8 %

Soit une moyenne de 3 % d'erreurs.

Avec la base **mnist5-9.pkl.gz**, qui contient uniquement les chiffres de 5 à 9 :

- 5.5 %
- 7.1 %
- 5.2 %

Soit une moyenne de 5,9 % d'erreurs.

### Discussion

Il est aisément observable que l'apprentissage des chiffres de 0 à 4 semble avoir été plus 
efficace que l'apprentissage des chiffres de 5 à 9. L'hypothèse pouvant être émise sur un 
tel écart est que la similarité entre certains chiffres entraînent des difficultés d'
apprentissage : les chiffres 6, 8 et 9, par exemple.

Mais dans l'ensemble, pour comparaison avec tous les chiffres, l'apprentissage est plus 
efficace sur une petite base. 5 chiffres sont appris plus facilement par le réseau de 
neurones que 10 chiffres.