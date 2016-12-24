# coding: utf8
# !/usr/bin/env python

import gzip # pour décompresser les données
import cPickle # pour désérialiser les données
import numpy # pour pouvoir utiliser des matrices
import matplotlib.pyplot as plt # pour l'affichage
import math

# Nombre d'inputs
INPUT = 784
# Nombre de neurones pour la couche d'entrée
INPUT_NEURONS = 10
# Nombre de couches cachés (sachant que les couches "visibles" sont au nombre de deux : couche d'entrée et couche de sortie)
HIDDEN_LAYERS = 1
# Nombre de neurones par couche cachée
HIDDEN_NEURONS = 10
# Nombre de neurones pour la couche de sortie
OUTPUT_NEURONS = 10
# Pas d'apprentissage
LEARNING_STEP = 0.1
# Nombre d'itérations
ITERATIONS = 1

class Perceptron:
	# Le Perceptrion multi-couches, c'est :
	#	- Un nombre de neurones dans la couche d'entrée
	#	- Un nombre de couches cachés
    #   - Un nombre de neurones par couche cachée
    #   - Un nombre de neurones dans la couche de sortie 
    #   - Un tableau de matrice de poids
    def __init__(self, input_neurons, hidden_layers, hidden_neurons, output_neurons):
        self.input_neurons = input_neurons
        self.hidden_layers = hidden_layers
        self.hidden_neurons = hidden_neurons
        self.output_neurons = output_neurons

    # Construction du réseau
    def build(self):
        self.couches = []
        # Couche d'input (+1 pour le poids du biais)
        self.couches.append(numpy.random.rand(self.nb_neurones, INPUT+1))
        # Autres couches : cachées et de sortie (+1 pour le poids du biais)
        for i in range(1, self.nb_couches):
            self.couches.append(numpy.random.rand(self.nb_neurones, self.nb_neurones+1))

    # Algorithme apprentissage
    def learn(self, index):
        self.errors = []
        self.outputs = []
        # Dans la base d'apprentissage (premier [0]), dans la base d'image (deuxième [0]), on récupère l'image à [index]
        image = data[0][0][index]
        # Redimensionnement de l'image en 28x28
        # image = image.reshape(28,28)
        # image = image.flatten()
        
        # Dans la base d'apprentissage ([0]), dans la base des labels ([1]), on récupère le label à [index]
        label = data[0][1][index]
        # on récupère à quel chiffre cela correspond (position du 1 dans label)
        label = numpy.argmax(label)
        print "LECTURE CHIFFRE", label

        input = image
        # 1. Calcul de la sortie de chaque neurone i de chaque couche l du réseau par propagation couche par couche de l'activité
        for l in range(self.nb_couches):
            output_precedent = []
            for i in range(self.nb_neurones):
                output_precedent.append(self.sigmoid(l, i, input))
            input = numpy.array(output_precedent)   # L'input devient l'output de la couche précédente
            self.outputs.append(input)

        output_final = self.outputs[self.nb_couches-1]

        print "Sortie :", output_final;

        # 2. Pour chaque neurone i de la couche n de sortie, calculer l'erreur
        error = []
        for i in range(len(self.couches[self.nb_couches-1])):
            error.append(self.error(i, label, output_final))
        self.errors.insert(0, error)

        # 3. Rétro-propager couche par couche l'erreur à travers chaque neurone i de chaque couche l du réseau
        for i in range(self.nb_couches-2, -1, -1):
            error = self.propagate(i, self.errors[0])
            self.errors.insert(0, error)
        print "ERRORS", self.errors

        # 4. Modifier chaque poids
        for l in range(self.nb_couches):
            for i in range(self.nb_neurones):
                for j in range(len(self.couches[l][i])):
                    # Calcul de la variation
                    print "VARIATION POIDS", j, "DE LA COUCHE", l, "NEURONE", i, ":", self.variation(l, i, j);
        

    def sigmoid(self, couche, neurone, input):
        output = self.sumInput(couche, neurone, input)
        output = math.exp(-1. * output)
        output = 1. / (1. + output)
        # print "OUTPUT NEURONE", neurone, "DE LA COUCHE", couche, ":", output
        return output

    def sumInput(self, couche, neurone, input):
        input = numpy.append(input, 1) # Ajout du biais
        # Produit Matriciel
        return numpy.dot(self.couches[couche][neurone], input)

    # Calcul de l'erreur du neurone "neurone", de la couche de sortie
    def error(self, neurone, target, output):
        y = output[neurone]
        error = y * (1 - y) * (target - y)
        return error

    # Propagation de l'erreur de la couche d'au-dessus "previous_error" sur la couche "couche"
    def propagate(self, couche, previous_error):
        error = []
        for i in range(self.nb_neurones): # Pour chaque neurone i de la couche, rétropropagation de l'erreur
            y = self.outputs[couche][i] # Récupération de la sortie
            somme = self.sumError(couche, i, previous_error) # Calcul de la somme
            delta = y*(1-y)*(somme)
            error.append(delta)
        return error

    def sumError(self, couche, neurone, previous_error):
        weights = self.couches[couche][neurone]
        weights = weights[0:len(previous_error)]
        # Produit Matriciel
        return numpy.dot(previous_error, weights)

    # Calcul de la variation du poids "poids", du neurone "neurone", de la couche "couche"
    def variation(self, couche, neurone, poids):
        # p = self.couches[couche][neurone][poids]  POIDS
        return LEARNING_STEP * self.errors[couche][poids] * self.outputs[couche][neurone]

if __name__ == '__main__':
    p = Perceptron(COUCHES_CACHES+2, NEURONES)
    p.build()
    print "Couche(s) du Perceptron : ", p.nb_couches, " - Neurone(s) par couche : ", p.nb_neurones

    data = cPickle.load(gzip.open('mnist.pkl.gz'))
    # n = nombre d'images dans le tableau d'apprentissage
    n = numpy.shape(data[0][0])[0]
    # on créé un vecteur de (ITERATIONS,) valeurs entières prises aléatoirement entre 0 et n-1
    indices = numpy.random.randint(n,size=(ITERATIONS,))
    print indices
    # i va valoir itérativement les valeurs dans indices / NB on aurait aussi pu écrire "for j in xrange(10): i = indices[j]"
    for i in indices:
        # appel de la fonction d'affichage
        p.learn(i)