# This is a simple neural network model for classifying species based on input features.
# It uses PyTorch and consists of three fully connected layers with ReLU activations.
# The model takes an input dimension of 4 (for example, features like sepal length, 
# sepal width, petal length, and petal width) and outputs a classification for 3 species 
# (e.g., Iris Setosa, Iris Versicolor, and Iris Virginica).


import torch.nn as nn

class SpeciesClassifierNN(nn.Module):
    def __init__(self, input_dim=11, num_classes=3):
        super(SpeciesClassifierNN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        return self.net(x)
