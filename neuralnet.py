import numpy as np
import random


class NeuralNetwork():

    def __init__(self, in_nodes, hid_nodes, hid_nodes2, out_nodes):
        
        self.input_nodes = in_nodes
        self.hidden_nodes = hid_nodes
        self.hidden_nodes2 = hid_nodes2
        self.output_nodes = out_nodes
        self.weights1 = 2* np.random.random((self.input_nodes, self.hidden_nodes)) -1
        self.weights2 = 2* np.random.random((self.hidden_nodes,self.hidden_nodes2)) -1
        self.weights3 = 2* np.random.random((self.hidden_nodes2,self.output_nodes)) -1
        self.bias1 = 2* np.random.random((self.hidden_nodes)) -1
        self.bias2 = 2* np.random.random((self.hidden_nodes2)) -1
        self.bias3 = 2* np.random.random((self.output_nodes)) -1

    # Activation functions
    def sigmoid(self, x):
        #applying the sigmoid function
        return 1 / (1 + np.exp(-x))
    
    def tanh(self,x):
        return (2 / (1 + np.exp(-2*x))) - 1
    
    def feedForward(self, inputs):
        inputs = np.asarray(inputs)
        hidden = self.sigmoid(np.dot(inputs, self.weights1)+ self.bias1)
        hidden2 = self.sigmoid(np.dot(hidden, self.weights2)+ self.bias2)
        output = self.sigmoid(np.dot(hidden2, self.weights3)+ self.bias3)
        return output
        
    def mutate(self, rate):   
        def mutation (val):
            if (np.random.random(1) < rate):
                rand = random.gauss(0, 0.1) + val
                if (rand > 1):
                    rand = 1
                elif (rand < -1):
                    rand =-1

                return rand
            else:
                return val
        vmutate = np.vectorize(mutation)
        self.weights1 = vmutate(self.weights1)
        self.weights2 = vmutate(self.weights2)
        self.weights3 = vmutate(self.weights3)
        self.bias1 = vmutate(self.bias1)
        self.bias2 = vmutate(self.bias2)
        self.bias3 = vmutate(self.bias3)
    
    def clone(self):
        cloneBrain = NeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)
        cloneBrain.weights1 = self.weights1
        cloneBrain.weights2 = self.weights2
        cloneBrain.weights3 = self.weights3
        cloneBrain.bias1 = self.bias1
        cloneBrain.bias2 = self.bias2
        cloneBrain.bias3 = self.bias3
        
        return cloneBrain
    
