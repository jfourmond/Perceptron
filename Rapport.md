# Réseaux de neurones

### *Remarques*

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

### a. En utilisant le paramètrage trouvé, entraînement d'un réseau différent avec chacune des bases d'apprentissage. Pour chaque réseau, test sur les 3 bases de tests

#### i. Résultats

Apprentissage sur la base **mnist.pkl.gz**, qui contient tous les chiffres, sur la base de test :

- **mnist.pkl.gz** : 11.1 %
- **mnist0-4.pkl.gz** : 10.9 %
- **mnist5-9.pkl.gz** : 14.7 %

Avec la base **mnist0-4.pkl.gz**, qui contient uniquement les chiffres de 0 à 4, sur la base de test :

- **mnist.pkl.gz** : 49.5 %
- **mnist0-4.pkl.gz** : 3.5 %
- **mnist5-9.pkl.gz** : 100.0 %

Avec la base **mnist5-9.pkl.gz**, qui contient uniquement les chiffres de 5 à 9 :

- **mnist.pkl.gz** : 53.7 %
- **mnist0-4.pkl.gz** : 100.0 %
- **mnist5-9.pkl.gz** : 6.1 %

#### ii. Discussion

Les résultats suite à l'apprentissage sur la base **mnist.pkl.gz**, sont globalement semblables.

Tandis que sur la base **mnist0-4.pkl.gz**, les résultats sont disparates. Sur cette base, le réseau 
de neurones a appris uniquement les chiffres de 0 à 4. Le pourcentage de 50 % d'erreurs ressort 
lorsque le réseau de neurone est testé sur tous les chiffres. Il est possible d'admettre que la majorité 
de ses erreurs s'effectue sur les chiffres de 5 à 9. D'où, lors du troisième test sur la base 
**mnist5-9.pkl.gz**, le pourcentage d'erreur de 100 %. 

Récripoquement, la même observation peut se faire sur la base **mnist5-9.pkl.gz**. Les erreurs sur la base 
de test **mnist.pkl.gz** seraient majoritairement sur les chiffres de 0 à 4. Ainsi, le pourcentage d'erreur 
est de 100 % sur la base **mnist0-4.pkl.gz**.

### b. Etude de l'évolution des performance du réseau appris sur la base **mnist0-4.pkl.gz** sur les bases tests **mnist0-4.pkl.gz** et **mnist5-9.pkl.gz** lorsque le réseau apprend les chiffres de 5 à 9

Les performances des réseaux ayant appris sur **mnist0-4.pkl.gz** ou **mnist5-9.pkl.gz** et testés sur 
leurs propres bases sont bien plus élevées que les performances du réseau de neurones ayant appris et 
étant testé sur **mnist.pkl.gz**.