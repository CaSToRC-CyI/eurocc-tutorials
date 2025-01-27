import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, DistributedSampler
from model import CNN_classifier
import time

    
parser = argparse.ArgumentParser(prog="Pytorch on HPC")

parser.add_argument("--batch_size", type=int, default=16)
parser.add_argument("--epochs", type=int, default=5)
parser.add_argument("--lr", type=float, default=0.001)

args = parser.parse_args()

MASTER_ADDR = os.environ["MASTER_ADDR"]
MASTER_PORT = os.environ["MASTER_PORT"]
WORLD_SIZE = int(os.environ["WORLD_SIZE"])

def train(model, dataloader: DataLoader, args, device,rank):
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(params=model.parameters(), lr = args.lr)

    model.train()
    if rank == 0:    
        print("Entering training loop...")

    for epoch in range(1, args.epochs + 1):
        epoch_loss: float =  0.0
       
        for batch_idx, (data,target) in enumerate(dataloader):

            data = data.to(device)
            target = target.to(device)
            
            output = model(data)
            loss = criterion(output, target)

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            epoch_loss += loss.item() #monitoring
            
            if rank == 0 and batch_idx % 100 == 0:
                    print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(dataloader.dataset)} '
                        f'({100. * batch_idx / len(dataloader):.0f}%)]\tLoss: {loss.item():.6f}')
        
        torch.distributed.barrier()
    if rank == 0:    
        print("Exiting training loop...")            
    
def worker(args): #introduce the concept of ranks, for single node its not important to state difference between local/global
    
    rank = int(os.environ["SLURM_PROCID"])    
    
    torch.distributed.init_process_group(
        backend='nccl',
        world_size=WORLD_SIZE,
        rank=rank,
        init_method='env://'
    )
    
    #set the device for the ranks
    torch.cuda.set_device(rank)
    device = torch.device(f"cuda:{rank}")
 
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
        
    #only rank 0 downloads the dataset
    if rank == 0:        
        train_dataset = datasets.MNIST('./data', 
                                       train=True, 
                                       download=True, 
                                       transform=transform)
        
    torch.distributed.barrier()  #synchronize after downloading the dataset, barrier position wrong here?
       
    #all ranks load the dataset after synchronization
    train_dataset = datasets.MNIST('./data', 
                                   train=True, 
                                   download=False, 
                                   transform=transform)

    #create a sampler for the dataset
    train_sampler = DistributedSampler(
        train_dataset,
        num_replicas=WORLD_SIZE,
        rank=rank
    )
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        drop_last=True,
        sampler=train_sampler
    )
    

    #initialize the model and send it to the gpu(s)
    model = CNN_classifier().to(device)
    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[rank])  #wrap with DDP

    #training starts
    time_start = time.time()
    train(model=model, dataloader=train_loader, args=args, device=device, rank=rank)
    time_stop = time.time()
    
    if rank == 0:
        print(f"Training time = {time_stop - time_start}")
        
    torch.distributed.destroy_process_group()#explicitly state to reader not to forget this
    
if __name__ == "__main__" :
   worker(args=args)
