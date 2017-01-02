# coding: utf8
# !/usr/bin/env python
# ------------------------------------------------------------------------
# Multi-Layer Perceptron
# By FOURMOND Jérôme
#
# Distribué sous licence BSD.
# ------------------------------------------------------------------------
from __future__ import division

import gzip # pour décompresser les données
import cPickle # pour désérialiser les données
import numpy # pour pouvoir utiliser des matrices
import math

# Base d'apprentissage
LEARNING_BASE = 'mnist0-4.pkl.gz'
# Bases de test
TESTING_BASES = ['mnist0-4.pkl.gz', 'mnist5-9.pkl.gz']
# Nombre d'inputs
INPUT = 784
# Nombre de neurones pour la couche d'entrée
INPUT_NEURONS = 10
# Nombre de couches cachées (sachant que les couches "visibles" sont au nombre de deux : couche d'entrée et couche de sortie)
HIDDEN_LAYERS = 1
# Nombre de neurones par couche cachée
HIDDEN_NEURONS = 10
# Nombre de neurones pour la couche de sortie
OUTPUT_NEURONS = 10
# Pas d'apprentissage
LEARNING_STEP = 0.3
# Nombre d'itérations d'apprentissage
LEARNING_ITERATIONS = 100000
# Nombre d'itérations de tests
TEST_ITERATIONS = 1000

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
        self.learning_iteration = 0
        self.build()
    # FIN METHODE __init__

    # Construction du réseau
    def build(self):
        l = 0
        self.layers = []
        # Couche d'input (+1 pour le poids du biais)
        self.layers.append(numpy.random.randn(self.input_neurons, INPUT+1))
        # Couche(s) cachée(s) (+1 pour le poids du biais)
        for i in range (0, self.hidden_layers):
            self.layers.append(numpy.random.randn(self.hidden_neurons, len(self.layers[l])+1))
            l += 1
        # Couche de sortie (+1 pour le poids du biais)
        self.layers.append(numpy.random.randn(self.output_neurons, self.hidden_neurons+1))
        print "RESEAU", self.layers

        self.nb_read = 0
        self.nb_wrong = 0
        self.nb_right = 0
    # FIN METHODE build

    # Algorithme apprentissage
    def learn(self, index):
        self.learning_iteration += 1
        if (self.learning_iteration % 100) == 0:
            print "Itération", self.learning_iteration
        self.errors = []
        self.outputs = []
        target = numpy.zeros(10)
        # Dans la base d'apprentissage (premier [0]), dans la base d'image (deuxième [0]), on récupère l'image à [index]
        image = data[0][0][index]
        # Dans la base d'apprentissage ([0]), dans la base des labels ([1]), on récupère le label à [index]
        target = data[0][1][index]
        # on récupère à quel chiffre cela correspond (position du 1 dans label)
        label = numpy.argmax(target)
        # 1. Calcul de la sortie de chaque neurone i de chaque couche l du réseau par propagation couche par couche de l'activité
        final_output = self.computeOutput(image)
        self.current_input = numpy.append(image, 1)
        # 2. Pour chaque neurone i de la couche n de sortie, calculer l'erreur
        self.computeOutputError(target, final_output)
        # 3. Rétro-propager couche par couche l'erreur à travers chaque neurone i de chaque couche l du réseau
        self.retroPropagate()
        # 4. Modifier chaque poids
        self.updateWeight()
    # FIN METHODE learn

    # Test du réseau
    def test(self, index):
        target = numpy.zeros(10)
        # Dans la base de test (premier [1]), dans la base d'image (deuxième [0]), on récupère l'image à [index]
        image = data[1][0][index]
        # Dans la base de test ([1]), dans la base des labels ([1]), on récupère le label à [index]
        target = data[1][1][index]
        # on récupère à quel chiffre cela correspond (position du 1 dans label)
        label = numpy.argmax(target)

        final_output = self.computeOutput(image)
        # print "SORTIE FINALE :", final_output
        # print "TARGET :", target
        value = self.anylisis(final_output)
        print "ANALYSIS :", value, ", TARGET :", label
        if value == label :
            self.nb_right += 1
        else:
            self.nb_wrong += 1
        self.nb_read += 1
    # FIN METHODE test

    # Calcul de la sortie de chaque neurone i de chaque couche l du réseau par propagation couche par couche de l'activité par l'entrée "input"
    def computeOutput(self, input):
        # Ajout du biais à l'input
        input = numpy.append(input, 1)
        self.outputs = []
        last_output = []

        # 1. Calcul de la sortie de chaque neurone i de la couche d'entrée
        for i in range(self.input_neurons):
            last_output.append(self.sigmoid(0, i, input))
        last_output.append(1) # Ajout du biais
        last_output = numpy.array(last_output)
        input = last_output   # L'input devient l'output de la couche précédente
        self.outputs.append(last_output)

        # 2. Calcul de la sortie de chaque neurone i de chaque couche l cachée
        for l in range(self.hidden_layers):
            last_output = []
            for i in range(self.hidden_neurons):
                last_output.append(self.sigmoid(l+1, i, input))
            last_output.append(1) # Ajout du biais
            last_output = numpy.array(last_output)
            input = last_output # L'input devient l'output de la couche précédente
            self.outputs.append(last_output)

        # 3. Calcul de la sortie de chaque neurone i de la couche de sortie
        last_output = []
        for i in range(self.output_neurons):
            last_output.append(self.sigmoid(self.nb_layers-1, i, input))
        last_output = numpy.array(last_output)
        self.outputs.append(last_output)
        # Retourne la sortie de la couche de sortie
        return last_output
    # FIN METHODE computeOutput

    # Calcul de la sortie du neurone "neuron" de la couche "layer" par l'entrée "input"
    def sigmoid(self, layer, neuron, input):
        output = numpy.dot(self.layers[layer][neuron], input)
        output = math.exp(-1. * output)
        output = 1 / (1  + output)
        return output
    # FIN METHODE sigmoid

    # Calcul de l'erreur des neurones de la couche de sortie
    def computeOutputError(self, target, output_final):
        error = []
        for i in range(len(self.layers[self.nb_layers-1])):
            y = output_final[i] # Sortie du neurone i
            e =  y * (1 - y) * (target[i] - y) # Calcul de l'erreur du neurone i
            error.append(e)
        self.errors.insert(0, error)
    # FIN METHODE computeOutputError

    # Rétro-propagation couche par couche l'erreur à travers chaque neurone i de chaque couche l du réseau
    def retroPropagate(self):
        for l in range(self.nb_layers-2, -1, -1):
            error = []
            for i in range(len(self.layers[l])):
                weights = self.weights(l+1, i)  # Récupération des poids i des neurones de la couche d'au-dessus
                y = self.outputs[l][i]          # Sortie du neurone courant
                delta = y*(1-y)*numpy.dot(self.errors[0], weights)
                error.append(delta)
            self.errors.insert(0, error)
    # FIN METHODE retroPropagate

    # Mise à jour de tous les poids du réseau
    def updateWeight(self):
        # Mise à jour de la couche d'entrée
        for i in range(len(self.layers[0])):
            for j in range(len(self.layers[0][i])):
                # La variation du poids j, du neurone i, de la couche 0 
                variation = self.variationInput(i, j)   # V_poids = poids' - poids '' -> poids'' = poids - V_poids
                self.layers[0][i][j] = self.layers[0][i][j] + variation

        # Mise à jour des autres couches
        for l in range(1, self.nb_layers):
            for i in range(len(self.layers[l])):
                for j in range(len(self.layers[l][i])):
                    # La variation du poids j, du neurone i, de la couche l 
                    variation = self.variation(l, i, j) # V_poids = poids' - poids '' -> poids'' = poids - V_poids
                    self.layers[l][i][j] = self.layers[l][i][j] + variation
    # FIN METHODE updateWeight

    # Calcul de la variation du poids "weight", du neurone "neuron", de la couche "layer"
    def variation(self, layer, neuron, weight):
        return LEARNING_STEP * self.errors[layer][neuron] * self.outputs[layer-1][weight]
    # FIN METHODE variation

    # Calcul de la variation du poids "weight", du neurone "neuron", de la couche d'entrée
    def variationInput(self, neuron, weight):
        return LEARNING_STEP * self.errors[0][neuron] * self.current_input[weight]
    # FIN METHODE variationInput

    # Récupération d'une liste des poids "weight" des neurones de la couche "layer"
    def weights(self, layer, weight):
        weights = []
        for i in range(len(self.layers[layer])):
            weights.append(self.layers[layer][i][weight])
        return weights
    # FIN METHODE weights

    def anylisis(self, final_output):
        return (numpy.argmax(final_output))
    # FIN METHODE anylisis

    def resetStats(self):
        self.nb_read = 0
        self.nb_right = 0
        self.nb_wrong = 0
    # FIN METHODE resetStats

    def __str__(self):
        return "" + str(self.input_neurons) + " neurones d'entrée, " + str(self.hidden_layers) + " couche(s) cachée(s) avec " \
            + str(self.hidden_neurons) + " neurones par couche, " + str(self.output_neurons) + " neurones de sortie."
    # FIN METHODE __str__
    
    def __repr__(self):
        return self.__str__()
    # FIN METHODE __repr__

# FIN DE LA CLASSE PERCEPTRON

def learningStage(p):
    global data
    data = cPickle.load(gzip.open(LEARNING_BASE))
    # n = nombre d'images dans le tableau d'apprentissage
    n = numpy.shape(data[0][0])[0]
    indices = numpy.random.randint(n,size=(LEARNING_ITERATIONS,))
    print "DEBUT DE LA PHASE D'APPRENTISSAGE SUR", LEARNING_ITERATIONS, "ITERATIONS"
    for i in indices:
        p.learn(i)
    print "FIN DE LA PHASE D'APPRENTISSAGE"
# FIN FONCTION learningStage

def testStage(p):
    print "DEBUT DE LA PHASE DE TEST SUR", TEST_ITERATIONS, "ITERATIONS"
    for i in range(len(TESTING_BASES)):
        base = TESTING_BASES[i]
        data = cPickle.load(gzip.open(base))
        # n = nombre d'images dans le tableau de test
        n = numpy.shape(data[1][0])[0]
        indices = numpy.random.randint(n,size=(TEST_ITERATIONS,))
        for i in indices:
            p.test(i)
        print "DANS LA BASE :", base, "LUS :", p.nb_read, "BONS :", p.nb_right, "FAUX :", p.nb_wrong
        e = (p.nb_wrong / p.nb_read) * 100
        print "POURCENTAGE D'ERREUR :", e
        p.resetStats()
    print "FIN DE LA PHASE DE TEST"
    print p
# FIN FONCTION testStage

if __name__ == '__main__':
    p = Perceptron(INPUT_NEURONS, HIDDEN_LAYERS, HIDDEN_NEURONS, OUTPUT_NEURONS)
    print p
    # Etape d'apprentissage
    learningStage(p)
    # Etape de test
    testStage(p)