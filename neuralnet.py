from turtle import clone
import numpy as np
import random
import copy
import Player

class NeuralNetwork():

    def __init__(self, in_nodes, hid_nodes, out_nodes):
        
        self.input_nodes = in_nodes
        self.hidden_nodes = hid_nodes
        self.output_nodes = out_nodes
        self.weights1 = np.random.normal(0,1,(self.input_nodes, self.hidden_nodes))
        self.weights2 = np.random.normal(0,1,(self.hidden_nodes,self.output_nodes))
        self.bias1 = np.random.normal(0,1,(self.hidden_nodes))
        self.bias2 = np.random.normal(0,1,(self.output_nodes))
        # origin code below #
        # self.weights1 = 2* np.random.random((self.input_nodes, self.hidden_nodes)) -1
        # self.weights2 = 2* np.random.random((self.hidden_nodes,self.output_nodes)) -1
        # self.bias1 = 2* np.random.random((self.hidden_nodes)) -1
        # self.bias2 = 2* np.random.random((self.output_nodes)) -1

    def changeelement(self, elem:str, size:list, coor:list, value=None):
        if(value==None):
            if(len(size)==1):
                at = None
                at = eval("self." + elem + "[" + str(coor[0]) +"]")
                # print(at)
                value =np.random.normal(at, 10)
            elif len(size)==2:
                at = None
                at = eval("self." + elem + "[" + str(coor[0]) +"]" + "[" + str(coor[1]) +"]")
                # print(at)
                value =np.random.normal(at, 10)
        if(elem == "weights1"):
            self.weights1[coor[0]][coor[1]] = value
        elif(elem == "weights2"):
            self.weights2[coor[0]][coor[1]] = value
        elif(elem == "bias1"):
            self.bias1[coor[0]] = value
        elif(elem == "bias2"):
            self.bias2[coor[0]] = value
        else:
            pass
        return self


    def normalchange(self, elem:str, mat=None):
        tempdict = {"weights1":self.weights1,"weights2":self.weights2,"bias1":self.bias1,"bias2":self.bias2}
        if mat == None:
            newbrain = self.copy()
            newdict={"weights1":newbrain.weights1,"weights2":newbrain.weights2,"bias1":newbrain.bias1,"bias2":newbrain.bias2}
            if elem in ["weights1", "weights2"]:
                newdict[elem]+=(np.random.normal(0,100,np.shape(newdict[elem])))
            elif elem in ["bias1", "bias2"]:
                for i in newdict[elem]:
                    i+=np.random.normal(0,100)
            else:
                pass
            return newbrain
        else:
            if np.shape(tempdict[elem]) != np.shape(mat):
                return self
            else:
                pass
            return self
        

    def copy(self):
        newbrain = NeuralNetwork(Player.INPUT_SIZE,Player.HIDDEN_SIZE,Player.OUTPUT_SIZE)
        newbrain.bias1 = copy.deepcopy(self.bias1)
        newbrain.bias2 = copy.deepcopy(self.bias2)
        newbrain.weights1 = copy.deepcopy(self.weights1)
        newbrain.weights2 = copy.deepcopy(self.weights2)
        return newbrain

    # Activation functions
    def sigmoid(self, x):
        #applying the sigmoid function
        return 1 / (1 + np.exp(-x))
    
    def tanh(self,x):
        return (2 / (1 + np.exp(-2*x))) - 1
    
    def feedForward(self, inputs):
        inputs = np.asarray(inputs)
        hidden = self.sigmoid(np.dot(inputs, self.weights1)+ self.bias1)
        output = self.sigmoid(np.dot(hidden, self.weights2)+ self.bias2)
        return output
        
    def mutate(self, rate):   
        def mutation (val):
            if (np.random.random(1) < rate):
                rand = random.gauss(0, 0.1) + val
                if (rand > 1):
                    rand = rand - int(rand)
                elif (rand < -1):
                    rand = rand - int(rand)

                return rand
            else:
                return val
        vmutate = np.vectorize(mutation)
        self.weights1 = vmutate(self.weights1)
        self.weights2 = vmutate(self.weights2)
        self.bias1 = vmutate(self.bias1)
        self.bias2 = vmutate(self.bias2)
    
    def clone(self):
        cloneBrain = NeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)
        cloneBrain.weights1 = self.weights1
        cloneBrain.weights2 = self.weights2
        cloneBrain.bias1 = self.bias1
        cloneBrain.bias2 = self.bias2
        cloneBrain.saveBrain()
        return cloneBrain
    
    def saveBrain(self):
        # savBrain = open("brain.txt","a+")
        # savBrain.write(str([self.weights1,self.weights2,self.bias1,self.bias2])+'\n')
        # savBrain.close()
        latest = open("latestbrain.txt","w")
        latest.write(str([self.weights1,self.weights2,self.bias1,self.bias2])+'\n')
        latest.close()



    
