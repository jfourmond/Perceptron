# Perceptron
Projet d'Intelligence Bio-Inspirée sous la direction de :
- [Dr. LEFORT Mathieu](http://liris.cnrs.fr/mathieu.lefort/)

Par : 
- [FOURMOND Jérôme](https://github.com/jfourmond/)

Dans le cadre de l'Unité d'Enseignement **Intelligence Bio-Inspirée** du [Master 2 Informatique - Parcours Intelligence Artificielle](http://master-info.univ-lyon1.fr/IA/) de l'[Université Claude Bernard Lyon 1](http://www.univ-lyon1.fr/).

---

## Objectif

L'objectif de ce projet est d'implémenter l'algorithme de perceptron multi-couches vu en cours, de comprendre son fonctionnement et ses limites.

## Sujet

[Sujet 2016](https://github.com/jfourmond/Perceptron/blob/master/projet.pdf)

## Compilation & Exécution

Le programme s'exécute sans arguments, en ligne de commande :

	python neural_network.py

## Pourcentage d'erreurs en fonction de différents paramètres

[Tableur regroupant les résultats](https://docs.google.com/spreadsheets/d/1DXshHQmfKDHbYvKog93c83oNjd8v94TPZoVbogYacHA/edit?usp=sharing)

## Explications & Détails

Dans le cas du programme, 6 paramètres sont ajustables :

- ***INPUT_NEURONS*** : nombre de neurones pour la couche d'entrée
- ***HIDDEN_LAYERS*** : nombre de couches cachées (sachant que les couches "visibles" sont au nombre de deux : couche d'entrée et couche de sortie)
- ***HIDDEN_NEURONS*** : nombre de neurones par couche cachée
- ***LEARNING_STEP*** : pas d'apprentissage
- ***LEARNING_ITERATIONS*** : nombre d'itérations d'apprentissage
- ***TEST_ITERATIONS*** : nombre d'itérations de test

Deux autres paramètres ne doivent pas être modifiés pour le bon fonctionnement de l'algorithme :

- ***INPUT*** : nombre d'inputs (le nombre de pixel de l'image, ici **784**)
- ***OUTPUT_NEURONS*** : nombre de neurones pour la couche de sortie (ici 10)

Il est possible de remarquer un abus de langage avec la variable globale ***INPUT_NEURONS*** : la couche d'entrée devrait contenir l'entrée (c'est à dire les **pixels**).
Dans le cas présent, on a une entrée (les pixels), une *couche d'entrée*, aucune, une ou plusieurs *couches cachées*, et enfin une *couche de sortie*.
Ce détail peut être à corriger.