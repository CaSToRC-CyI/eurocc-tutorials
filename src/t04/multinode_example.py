import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, DistributedSampler
from model import CNN_classifier
import time

# Argument parsing
parser = argparse.ArgumentParser(prog="Pytorch on HPC")

parser.add_argument("--batch_size", type=int, default=16)
parser.add_argument("--epochs", type=int, default=5)
parser.add_argument("--lr", type=float, default=0.001)

args = parser.parse_args()

MASTER_ADDR = os.environ["MASTER_ADDR"]
MASTER_PORT = os.environ["MASTER_PORT"]
WORLD_SIZE = int(os.environ["WORLD_SIZE"])
NODE_RANK = int(os.environ["NODE_RANK"])

def train(model, dataloader, args, device, rank):
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(params=model.parameters(), lr=args.lr)

    model.train()
    if rank == 0:
        print("Entering training loop...")

    for epoch in range(1, args.epochs + 1):
        epoch_loss = 0.0

        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            if rank == 0 and batch_idx % 100 == 0:
                print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(dataloader.dataset)} '
                      f'({100. * batch_idx / len(dataloader):.0f}%)]\tLoss: {loss.item():.6f}')

        torch.distributed.barrier()
    if rank == 0:
        print("Exiting training loop...")

def worker(args):
    
    global_rank = int(os.environ["SLURM_PROCID"])    
    local_rank = int(os.environ["SLURM_LOCALID"])

    print(f"Rank {global_rank} on Node {os.environ['SLURM_NODEID']}: Initializing process group.")
    
    torch.distributed.init_process_group(
        backend='nccl', 
        world_size=WORLD_SIZE, 
        rank=global_rank,
        init_method='env://'
    )

    torch.cuda.set_device(local_rank)
    device = torch.device(f"cuda:{local_rank}")

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    if local_rank == 0:
        
        train_dataset = datasets.MNIST('./data',
                       train=True, 
                       download=True, 
                       transform=transform)
    
    torch.distributed.barrier()  

    train_dataset = datasets.MNIST('./data', 
                                   train=True, 
                                   download=False, 
                                   transform=transform)
    
    train_sampler = DistributedSampler(train_dataset, 
                                       num_replicas=WORLD_SIZE, 
                                       rank=global_rank)
    
    train_loader = DataLoader(train_dataset,
                              batch_size=args.batch_size,
                              sampler=train_sampler,
                              drop_last=True)

    # Model setup
    model = CNN_classifier().to(device)
    model = nn.parallel.DistributedDataParallel(model, device_ids=[local_rank])

    # Training loop
    time_start = time.time()
    train(model=model, dataloader=train_loader, args=args, device=device, rank=global_rank)
    time_stop = time.time()

    if global_rank == 0:
        print(f"Training time = {time_stop - time_start}")

    torch.distributed.destroy_process_group()

if __name__ == "__main__":
    # Spawn processes for each GPU on this node using SLURM
    worker(args=args)
