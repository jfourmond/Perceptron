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
        self.nb_layers = hidden_layers + 2
        self.build()

    # Construction du réseau
    def build(self):
        l = 0
        self.layers = []
        # Couche d'input (+1 pour le poids du biais)
        self.layers.append(numpy.zeros((self.input_neurons, INPUT+1)))
        # Couche(s) cachée(s) (+1 pour le poids du biais)
        for i in range (0, self.hidden_layers):
            self.layers.append(numpy.zeros((self.hidden_neurons, len(self.layers[l])+1)))
            l += 1
        # Couche de sortie (+1 pour le poids du biais)
        self.layers.append(numpy.zeros((self.output_neurons, len(self.layers[l])+1)))
        print "RESEAU", self.layers

        self.nb_wrong = 0
        self.nb_right = 0

    # Algorithme apprentissage
    def learn(self, index):
        self.errors = []
        self.outputs = []
        target = numpy.zeros(10)
        # Dans la base d'apprentissage (premier [0]), dans la base d'image (deuxième [0]), on récupère l'image à [index]
        image = data[0][0][index]
        # Dans la base d'apprentissage ([0]), dans la base des labels ([1]), on récupère le label à [index]
        label = data[0][1][index]
        # on récupère à quel chiffre cela correspond (position du 1 dans label)
        label = numpy.argmax(label)
        print "LECTURE CHIFFRE", label
        target[label] = 1

        # 1. Calcul de la sortie de chaque neurone i de chaque couche l du réseau par propagation couche par couche de l'activité
        final_output = self.computeOutput(image)
        print "SORTIE FINALE :", final_output
        print "TARGET :", target
        value = self.anylisis(final_output)
        if value == label :
            self.nb_right += 1
        else:
            self.nb_wrong += 1
        # 2. Pour chaque neurone i de la couche n de sortie, calculer l'erreur
        self.computeOutputError(target, final_output)
        # 3. Rétro-propager couche par couche l'erreur à travers chaque neurone i de chaque couche l du réseau
        self.retroPropagate()
        print "ERRORS", self.errors
        # 4. Modifier chaque poids
        self.updateWeight()
    
    # Calcul de la sortie de chaque neurone i de chaque couche l du réseau par propagation couche par couche de l'activité par l'entrée "input"
    def computeOutput(self, input):
        self.outputs = []
        # 1. Calcul de la sortie de chaque neurone i de la couche d'entrée
        last_output = []
        for i in range(self.input_neurons):
            last_output.append(self.sigmoid(0, i, input))
        input = numpy.array(last_output)    # L'input devient l'output de la couche précédente
        self.outputs.append(last_output)
        # 2. Calcul de la sortie de chaque neurone i de chaque couche l cachée
        for l in range(self.hidden_layers):
            last_output = []
            for i in range(self.hidden_neurons):
                last_output.append(self.sigmoid(l+1, i, input))
            input = numpy.array(last_output) # L'input devient l'output de la couche précédente
            self.outputs.append(last_output)
        # 3. Calcul de la sortie de chaque neurone i de la couche de sortie
        last_output = []
        for i in range(self.output_neurons):
            last_output.append(self.sigmoid(self.nb_layers-1, i, input))
        self.outputs.append(last_output)
        print "OUTPUTS", self.outputs
        # Retourne la sortie de la couche de sortie
        return last_output

    # Calcul de la sortie du neurone "neuron" de la couche "layer" par l'entrée "input"
    def sigmoid(self, layer, neuron, input):
        input = numpy.append(input, 1) # Ajout du biais
        output = numpy.dot(self.layers[layer][neuron], input)
        output = math.exp(-1. * output)
        output = 1. / (1. + output)
        return output

    # Calcul de l'erreur des neurones de la couche de sortie
    def computeOutputError(self, target, output_final):
        error = []
        for i in range(len(self.layers[self.nb_layers-1])):
            y = output_final[i] # Sortie du neurone i
            e =  y * (1 - y) * (target[i] - y) # Calcul de l'erreur du neurone i
            error.append(e)
        self.errors.insert(0, error)

    # Rétro-propagation couche par couche l'erreur à travers chaque neurone i de chaque couche l du réseau
    def retroPropagate(self):
        for l in range(self.nb_layers-2, -1, -1):
            error = []
            for i in range(len(self.layers[l])):
                y = self.outputs[l][i]          # Sortie du neurone courant
                weights = self.layers[l+1][i]   # Poids du neurone i de la couche d'au-dessus
                weights = weights[0:(len(weights)-1)] # Suppression du biais ?
                delta = y*(1-y)*numpy.dot(self.errors[0], weights)
                error.append(delta)
            self.errors.insert(0, error)

    def updateWeight(self):
        for l in range(self.nb_layers):
            for i in range(len(self.layers[l])):
                for j in range(len(self.layers[l][i])):
                    # TODO
                    sum = 0
                    # print "POIDS", j, "DE LA COUCHE", l, "NEURONE", i, ":", self.layers[l][i][j];
                    # Calcul de la variation
                    # print "VARIATION POIDS", j, "DE LA COUCHE", l, "NEURONE", i, ":", self.variation(l, i, j);

    # Calcul de la variation du poids "poids", du neurone "neurone", de la couche "couche"
    def variation(self, couche, neurone, poids):
        # p = self.couches[couche][neurone][poids]  POIDS
        return LEARNING_STEP * self.errors[couche][poids] * self.outputs[couche][neurone]

    def anylisis(self, final_output):
        return (numpy.argmax(final_output))

    def __str__(self):
        return "" + str(self.input_neurons) + " neurones d'entrée, " + str(self.hidden_layers) + " couche(s) cachée(s) avec " \
            + str(self.hidden_neurons) + " neurones par couche, " + str(self.output_neurons) + " neurones de sortie."
    
    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    p = Perceptron(INPUT_NEURONS, HIDDEN_LAYERS, HIDDEN_NEURONS, OUTPUT_NEURONS)
    print p
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