# This is a simple neural network model for biomass regression.
# It uses PyTorch and consists of three linear layers with ReLU activations.
# The input dimension is set to 4, which corresponds to the four bands of the Sentinel-2 images.
# This model is designed to predict biomass based on the input features extracted from the images.

import torch.nn as nn

class BiomassRegressionNN(nn.Module):
    def __init__(self, input_dim=11):
        super(BiomassRegressionNN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x)
