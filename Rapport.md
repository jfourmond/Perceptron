# Réseaux de neurones

## Remarques

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
Pour un pourcentage d'erreur de **10.1 %**

## 2. Etude de l'algorithme

Avec la base **mnist.pkl.gz**, qui contient tous les chiffres :

-
-
-

Avec la base **mnist0-4.pkl.gz**, qui contient uniquement les chiffres de 0 à 4 :

-
-
-

Avec la base **mnist5-9.pkl.gz**, qui contient uniquement les chiffres de 5 à 9 :

- 
-
-