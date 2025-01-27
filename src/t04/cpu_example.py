import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import CNN_classifier
import time

def train(model, dataloader: DataLoader, args):

    print("Entering training loop...")
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(params=model.parameters(), lr = args.lr)

    model.train()
    for epoch in range(1, args.epochs + 1):
        epoch_loss: float =  0.0
       
        for batch_idx, (data,target) in enumerate(dataloader):
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            if batch_idx % 100 == 0:
                    print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(dataloader.dataset)} '
                        f'({100. * batch_idx / len(dataloader):.0f}%)]\tLoss: {loss.item():.6f}')
    print("Exiting training loop...")            
    
def main():
    
    parser = argparse.ArgumentParser(prog="Pytorch on HPC")
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--lr", type=float, default=0.001)
    
    args = parser.parse_args()
    
    transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
    ])
        
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    train_loader = DataLoader(
        train_dataset,
        batch_size = args.batch_size,
        shuffle=False,
    )
    model = CNN_classifier()
    
    time_start = time.time()
    train(model=model, dataloader= train_loader, args=args)
    time_stop = time.time()
    
    print(f"Training time = {time_stop-time_start}" )
        
if __name__ == "__main__" :
    main()