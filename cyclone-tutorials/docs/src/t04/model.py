import torch.nn as nn
import torch.functional as func
import torch
class CNN_classifier(nn.Module):
    def __init__(self, *args, **kwargs):
        super(CNN_classifier,self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels= 1, out_channels=32, kernel_size=3)
        self.conv2 = nn.Conv2d(in_channels= 32, out_channels= 64, kernel_size=3)
        
        self.fc1 = nn.Linear(in_features=9216, out_features=128)
        self.fc2 = nn.Linear(in_features=128, out_features=10)
        
    def forward(self, x)-> torch.Tensor:
        
        #First convolution block        
        x = self.conv1(x)
        x = nn.functional.relu(x)
        #seocnd convolution block
        x = self.conv2(x)
        x = nn.functional.relu(x)
        
        x = nn.functional.max_pool2d(x, kernel_size=2)
        x = torch.flatten(x, 1) #Flatten the image along the 1st dimension.
        
        x = self.fc1(x)
        x = self.fc2(x)

        out = nn.functional.log_softmax(x,dim=1)
        
        return out
