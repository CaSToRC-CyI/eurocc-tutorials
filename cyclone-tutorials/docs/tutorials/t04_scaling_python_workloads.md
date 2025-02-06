<!--
 t04_scaling_python_workloads.md

 CaSToRC, The Cyprus Institute

 (c) 2024 The Cyprus Institute

 Contributing Authors:
 Spiros Millas (s.millas@cyi.ac.cy)
 Simone Bacchio (s.bacchio@cyi.ac.cy)
 Andreas Athenodorou (a.athenodorou@cyi.ac.cy)
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     https://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# 4. Scaling Python Workloads
 
## 4.1. Overview

<div style="text-align: justify;">This tutorial provides a comprehensive guide on scaling Python workloads using Cyclone, covering frameworks for deep learning and hardware acceleration. The tutorial begins by executing Python scripts on CPUs, gradually progressing to single GPU, multi GPU, and multi-node distributed training using PyTorch's Distributed Data Parallel framework. Each section includes modifications to SLURM scripts for resource allocation and Python code adaptations to leverage the targeted hardware configurations. The tutorial concludes with troubleshooting tips and a recap of practices mentioned.</div>

---

## 4.2. Learning Objectives

<div style="text-align: justify;">
By the end of this tutorial, participants will be able to:
<ol>
<li>Write and execute SLURM scripts to run Python scripts on Cyclone in different configurations (CPU, single GPU, multi-GPU, multi-node).</li>
<li>Understand the resource allocation process using SLURM for Python workloads.</li>
<li>Optimize Python workflows for HPC by leveraging distributed computing frameworks like PyTorch DDP.</li>
<li>Troubleshoot common issues when running Python jobs on Cyclone.</li>
</ol>
</div>

---

## 4.3. Prerequisites

1. [T01 - Introduction to HPC Systems](t01_introduction_to_hpc_systems.md): This tutorial will give you some basic knowledge on HPC systems and basic terminologies.


2. [T02 - Accessing and Navigating Cyclone:](t02_accessing_and_navigating_cyclone.md)This tutorial will give you some basic knowledge on how to connect, copy files and navigate the HPC system. 

---

## 4.4. Why Use Cyclone for Python Workloads?
<div style="text-align: justify;">
<ol>
<li><b>Scalability:</b> Using Cyclone, workloads can be scaled across multiple CPUs and GPUs, which enables faster processing of large datasets and complex computations.</li>

<li><b>Performance Gains:</b> Utilizing advanced hardware/software such as GPUs, high-speed interconnects and SLURM, Python workflows can be executed more efficiently.</li>
</div>
</ol>

---

## 4.5. Tools and Frameworks

<div style="text-align: justify;">
<ul>
<li><b>SLURM</b> - Used for job scheduling, job monitoring and environment setup</li>
<li><b>PyTorch</b> - Open-source deep learning framework that’s known for its flexibility and ease-of-use.</li>
<li><b>CUDA</b> - Enables GPU acceleration for computational tasks through APIs to simplify GPU-based parallel processing for HPC, data science and AI.</li>
<li><b>NCCL</b> - Implements multi-GPU and multi-node communication that is optimized for NVIDIA GPUs and networking.</li>
</ul>
</div>

---

## 4.6. Training AI models on Cyclone

<div style="text-align: justify;">This section demonstrates how to run Python scripts with multiple environment configurations on Cyclone, focusing on scaling Python workloads by leveraging Pytorch, CUDA and NVIDIA's NCCL backend.</div>
<br>

### 4.6.1. Running Python Scripts on CPU

<div style="text-align: justify;">The script below demonstrates how to sructure a training pipeline for deep learning using PyTorch on a CPU. Firstly, the necessary libraries that handle tasks such as data loading and model training are imported. The main workflow includes downloading the dataset, as well as defining and training a <b>Convolutional Neural Network (CNN)</b>.</div>

```python
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
```

<div style="text-align: justify;">To execute the above script, first navigate to 
your <code>$HOME</code> directory, create and enter the new directory for this tutorial.</div>

```bash
[smillas@front02 ~]$ cd $HOME
[smillas@front02 ~]$ mkdir tutorial_04
[smillas@front02 ~]$ cd tutorial_04
```

Next, create the source file <code>cnn_cpu.py</code> 

```bash
[smillas@front02 tutorial_04]$ touch cnn_cpu.py
[smillas@front02 tutorial_04]$ nano cnn_cpu.py # copy the python code above
```

<div style="text-align: justify;">and copy the code above. To execute <code>cnn_cpu.py</code> you need to create the SLUMR file <code>run_cpu.SLURM</code></div>

```bash
[smillas@front02 tutorial_04]$ touch run_cpu.SLURM
[smillas@front02 tutorial_04]$ chmod +x run_cpu.SLURM # make the file executable
[smillas@front02 tutorial_04]$ nano run_cpu.SLURM # copy the SLURM script below
```

and copy the following:

```bash
#!/bin/bash
#SBATCH --job-name=pytorch_cpu      # Job name
#SBATCH --nodes=1                   # Number of nodes
#SBATCH --cpus-per-task=10          # CPUs per task
#SBATCH --time=02:00:00             # Maximum runtime (HH:MM:SS)
#SBATCH --partition=cpu             # Partition name
#SBATCH --output=logs/cpu_%j.out    # Standard output log
#SBATCH --error=logs/cpu_%j.err     # Standard error log

module load PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load torchvision/0.13.1-foss-2022a-CUDA-11.7.0

# Run Python script
srun python cnn_cpu.py \
    --batch_size 16 \
    --epochs 5 \
    --lr 0.001
```
<div style="text-align: justify;">
The <code>run_cpu.SLURM</code> script is designed to execute the <code>cnn_cpu.py</code> on Cyclone using SLURM. In the script, the number of nodes, CPU cores, runtime and partition are specified, which instruct SLURM to allocate 10 CPU cores from a single node for 2:00:00 hours for this job. 
<br><br>
Next, the environment is setup using Cyclones available modules for Pytorch and Torchvision ensuring all necessary libraries and dependencies are available. 
<br><br>
Finally, the Python script is launched using <code>srun</code>, which executes the specified script with the allocated resources and given runtime arguments.

To run the script:
</div>

```bash
sbatch run_cpu.SLURM
```

<div style="text-align: justify;">
After executing the above script, two seperate output logs will be generated in the <code>logs/</code> directory. 
</div>

```
cpu_<jobid>.out
cpu_<jobid>.err
```

<div style="text-align: justify;">
Navigate to the <code>logs/</code> directory with the terminal interface using <code>cd logs/</code> or by using VScode's file explorer.
<br><br>
Next, view the contents of the  <code>cpu_<jobid>.out</code>. To use the terminal, first execute <code>module load nano</code> to load a Linux text editor and enter the command <code>nano cpu_<jobid>.out</code>. If navigating using VScode, simply double click the output file. 
</div>

```python
Entering training loop...
Train Epoch: 1 [0/60000 (0%)]	    Loss: 2.300653
Train Epoch: 1 [1600/60000 (3%)]	Loss: 0.546140
.
.
Train Epoch: 5 [57600/60000 (96%)]	Loss: 0.000070
Train Epoch: 5 [59200/60000 (99%)]	Loss: 0.000981
Exiting training loop...
Training time = 192.2544162273407
```

<div style="text-align: justify;">
Training this simple CNN classifier for 5 epochs on the relatively small MNIST dataset took a total of 192 seconds. This process can be made significantly more efficient by utilizing Cyclones GPU cores, rather than the CPU cores.
</div>
<br>

### 4.6.2. Running Python Scripts on Single GPU

<div style="text-align: justify;">
To train the AI model using GPUs on Cyclone, some basic modifications must be made on both the Python and SLURM scripts. Beginning with the <code>cnn_gpu.py</code> Python script, in the main function, the following code block is added.
</div>

```python
 if torch.cuda.is_available():
        print("Utilizing GPU")
        device = torch.device("cuda")
        
    else: 
        print("Utilizing CPU")
        device = torch.device('cpu')
```

<div style="text-align: justify;">
The above code initializes the device variable as the GPU, by first checking if there is one available. If not, the device defaults to CPU. 
<br><br>
The next changes to the script must be made before the model begins training using the code below 
</div>

```python
model.to(device)
```

and during training using the following 

```python
data = data.to(device)
target = target.to(device)
```

<div style="text-align: justify;">
It is important to <b>have both the data and the model on the same device</b> (CPU or GPU), otherwise a runtime error will occur. PyTorch operations require the tensors involved to be on the same device.
</div>

> ℹ️ The complete <code>cnn_gpu.py</code> can be found [here](../src/t04/gpu_example.py).

<div style="text-align: justify;">
The <code>run_gpu.SLURM</code> script is designed to execute the <code>cnn_gpu.py</code> on a single GPU. This configuration is specified by instructing SLURM to allocate a GPU on a single node using the following SLURM directives. When launching gpu jobs on Cyclone, it is important to specify the correct <code>--partition</code> as SLURM defaults to CPU, which will cause an error.
</div>

```bash
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks-per-node=1     # Tasks per node (GPUs per node)
#SBATCH --gpus-per-node=1       # GPUs per node
#SBATCH --partition=gpu         # Partition name
```

<div style="text-align: justify;">
Next, some additional GPU-related modules must be loaded from Cyclone's library. The cuDNN and CUDA modules provide the tools and drivers required to enable GPU optimized deep learning operations.
</div>

```bash
module load PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load cuDNN/8.4.1.50-CUDA-11.7.0
module load torchvision/0.13.1-foss-2022a-CUDA-11.7.0
module load CUDA/11.7.0
```

<div style="text-align: justify;">
When loading modules from Cyclone's library, it is important to load compatible versions of these modules to ensure smooth interaction between the hardware (e.g., CUDA), and the deep learning framework (e.g., PyTorch), avoiding errors or performance issues.
</div>

> ℹ️ The complete <code>run_gpu.SLURM</code> can be found [here](../src/t04/run_gpu.SLURM).

<div style="text-align: justify;">
To run this example, first we need to create the <code>cnn_gpu.py</code> and <code>run_gpu.SLURM</code> as follows:
</div>

```bash
[smillas@front02 ~]$ cd $HOME/tutorial_04
[smillas@front02 tutorial_04]$ touch cnn_gpu.py
[smillas@front02 tutorial_04]$ nano cnn_gpu.py # copy the code from source Python file
[smillas@front02 tutorial_04]$ touch run_gpu.SLURM
[smillas@front02 tutorial_04]$ chmod +x run_gpu.SLURM # make the file executable
[smillas@front02 tutorial_04]$ nano run_gpu.SLURM # copy the source SLURM script
```

<span style="text-align: justify;">where the source files can be found from</span> [cnn_gpu.py](../src/t04/gpu_example.py) and [run_gpu.SLURM](../src/t04/run_gpu.SLURM).

<div style="text-align: justify;">
Once the two files are ready, submit the job using:
</div>

```bash
[smillas@front02 tutorial_04]$ sbatch run_gpu.SLURM
```

<div style="text-align: justify;">
After the job finishes, navigate to the <code>logs/</code> directory and open the <code>gpu_&lt;job_id&gt;.out</code> file and observe the difference.
</div>

```python
Utilizing GPU
Entering training loop...
Train Epoch: 1 [0/60000 (0%)]	    Loss: 2.332518
Train Epoch: 1 [1600/60000 (3%)]	Loss: 0.376552
Train Epoch: 1 [3200/60000 (5%)]	Loss: 0.127207
.
.
.
Train Epoch: 5 [59200/60000 (99%)]	Loss: 0.082046
Exiting training loop...
Training time = 73.48071932792664
```

<div style="text-align: justify;">
Already there is a <b>substantial decrease in training time by utilizing a GPU over a CPU</b>. However, Cyclone offers much more GPU resources per node, meaning that there are further gains to training efficiency left on the table by utilizing only a single GPU.
</div>
<br>

### 4.6.3. Running Python Scripts on Multi-GPU (Single Node) using DDP

<div style="text-align: justify;">
To leverage multiple GPUs per node on Cyclone, workloads must be scaled using parallelization techniques. While there are many times of parallelism, <b>Data parallelism</b> will be used to scale model training in this tutorial. 
</div>

![Data Parallelism diagram](../images/DD.png)

<div style="text-align: justify;">
When optimizing AI training using data parallelism, a <b>copy of the model</b> is loaded on all GPUs available, and <b>the dataset is split amongst them</b>. Each GPU processes a different subset of the data in parallel. During the forward pass, each GPU processes a different batch of the data and the <b>gradients are communicated between the devices</b> so as to ensure the model parameters are appropriately updated during backpropagation. To implement this efficiently, PyTorch provides the <b>Distributed Data Parallel (DDP)</b> module, which automates the process of distributing data, synchronizing gradients, and ensuring consistent parameter updates across GPUs. DDP leverages NCCL (NVIDIA Collective Communications Library) as its backend to optimize GPU communication, enabling seamless gradient sharing and synchronization with minimal overhead.
</div>

![Ranks diagram](../images/singlenoderanks.png)

<div style="text-align: justify;">
To train our AI model using DDP, some changes must be made to the Python and SLURM scripts. Firstly, the concepts of <b>Ranks</b>, <b>Processes</b> and the <b>World</b> are introduced to the workflow. A <b>rank is the unique id given to a process</b>, and is used for communication purposes. One GPU corresponds to one process. The <b>World is a group that contains all the processes</b>, thus the size of the World is equal to the number of GPUs. 
<br><br>

Firstly, in the <code>run_multigpu.SLURM</code> script, changes are being made to the directives to instruct SLURM to allocate more GPUs per node. For this section of the tutorial, <b>2 GPUs on a single node</b> are utilized.   
</div>

```bash
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks-per-node=2     # Tasks per node (GPUs per node)
#SBATCH --gpus-per-node=2       # GPUs per node
```

<div style="text-align: justify;"> 
Further changes to the SLURM script include lines to retrieve environment variables set by the SLURM scheduler to define the nodes' address and a random port which are <b>used to establish communication between processes during training</b>. This communication will be done using the NCCL backend, which must be also loaded. World size can be directly calculated in the SLURM script using the environment variables, which as stated before is the total number of GPUs available. Finally to the <code>srun</code> command, add <code>--export=ALL</code> to ensure the environment variables are passed to the <code>srun</code> job. A snapshot of these changes is shown below.
</div> 

> ℹ️ The full <code>run_multigpu.SLURM</code> can be found [here](../src/t04/run_multigpu.SLURM).

```bash
module load CUDA/11.7.0
module load NCCL/2.12.12-GCCcore-11.3.0-CUDA-11.7.0
module load PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load cuDNN/8.4.1.50-CUDA-11.7.0
module load torchvision/0.13.1-foss-2022a-CUDA-11.7.0

export MASTER_ADDR=$(scontrol show hostname $SLURM_NODELIST | head -n 1)
export MASTER_PORT=$(shuf -i 29500-65535 -n 1)
export WORLD_SIZE=$(($SLURM_NNODES * $SLURM_NTASKS_PER_NODE)) 

srun --export=ALL python HPC_tutorial/multigpu_example.py \
    --batch_size 16 \
    --epochs 5 \
    --lr 0.001
```

<div style="text-align: justify;"> 
Moving on to the Python script, the environment variables (<code>MASTER_ADDR</code>, <code>MASTER_PORT</code> and <code>WORLD_SIZE</code>) are exported from the SLURM scheduler to be used by DDP, and are placed as global variables at the start of the script, after the import statements.
</div>

```python
import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, DistributedSampler
from model import CNN_classifier
import time

MASTER_ADDR = os.environ["MASTER_ADDR"]
MASTER_PORT = os.environ["MASTER_PORT"]
WORLD_SIZE = int(os.environ["WORLD_SIZE"])
```

<div style="text-align: justify;"> 
The next adjustment to the script happens to the main function (which has been renamed to the worker function). Since SLURM will launch as many processes as there are GPUs, the rank of the process can be defined as the process ID. Next, the process group must be initialized with some key parameters. <code>nccl</code> is chosen as the backend, the <code>world_size</code> and <code>rank</code> parameters are added, and lastly specify the <code>init_method = 'env://'</code> to indicate the <code>MASTER_ADDR</code> and <code>MASTER_PORT</code> environment variables should be used to configure the communication. Finally, the current process is assigned to its corresponding GPU based on its <code>rank</code>. The device object is created with the following syntax <code>cuda:&lt;rank&gt;</code>, which is used send the model and data to the approprate GPU. 
</div>

```python
def worker(args): 
   
    rank = int(os.environ["SLURM_PROCID"])    
    
    torch.distributed.init_process_group(
        backend='nccl',
        world_size=WORLD_SIZE,
        rank=rank,
        init_method='env://'

    torch.cuda.set_device(rank)
    device = torch.device(f"cuda:{rank}")

    )
```

<div style="text-align: justify;"> 
When implementing data parallelism, it is unnecessary to download the entire dataset on all devices. One device can download the dataset and share it with the rest of the GPUs. To do this, the dataset download command is changed to only execute on <code>rank 0</code>. To ensure device synchronization, <code>torch.distributed.barrier()</code> is called, which instructs the GPUs to wait until all other devices reach that same point in the script before continuing. Next the dataset is loaded on all other GPUs
</div>

```python
    if rank == 0:        
        train_dataset = datasets.MNIST('./data', 
                                       train=True, 
                                       download=True, 
                                       transform=transform)
    torch.distributed.barrier()
    
    train_dataset = datasets.MNIST('./data', 
                                   train=True, 
                                   download=False, 
                                   transform=transform)
```

<div style="text-align: justify;"> 
Next, a <code>DistributedSampler</code> object is defined, which ensures that workload is distributed across all GPUs that are apart of the world. To ensure the dataset is split into manageable batches, the sampler is combined with the <code>Dataloader</code> object.
</div>

```python
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
```

<div style="text-align: justify;"> 
The model is then wrapped with <code>DistributedDataParallel</code>, which will handle the multi-GPU training, ensuring the gradients will be synchronized across all processes after the forward pass. Next, the <code>device_ids = [rank]</code> is specified to define the GPU on which the model will run for the current process.
</div>

```python 
    model = CNN_classifier().to(device)
    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[rank])
```

<div style="text-align: justify;"> 
Stepping into the <code>train()</code> function,  <code>torch.distributed.barrier()</code> is called at the end of the epoch to ensure synchronization during training and to avoid runtime errors. Optionally, rank parameter is added to the function call to avoid duplicate printing in the output call by specifying one GPU to be the logging device. 
</div>

```python
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
    
```

<div style="text-align: justify;"> 
Last and most importantly, at the end of the worker function, <code>torch.distributed.destroy_process_group()</code> is called. This ensures all resources tied to distributed training are properly released.
</div>

```python
    if rank == 0:
        print(f"Training time = {time_stop - time_start}")
        
    torch.distributed.destroy_process_group()
    
if __name__ == "__main__" :
   worker(args=args)
```

> ℹ️ The full <code>cnn_multigpu.py</code> can be found [here](../src/t04/multigpu_example.py).

<div style="text-align: justify;">
To run this example, first we need to create the <code>cnn_multigpu.py</code> and <code>run_multigpu.SLURM</code> as follows:
</div>

```bash
[smillas@front02 ~]$ cd $HOME/tutorial_04
[smillas@front02 tutorial_04]$ touch cnn_multigpu.py
[smillas@front02 tutorial_04]$ nano cnn_multigpu.py # copy the code from source Python file
[smillas@front02 tutorial_04]$ touch run_multigpu.SLURM
[smillas@front02 tutorial_04]$ chmod +x run_multigpu.SLURM # make the file executable
[smillas@front02 tutorial_04]$ nano run_multigpu.SLURM # copy the source SLURM script
```

<span style="text-align: justify;">where the source files can be found from</span> [cnn_multigpu.py](../src/t04/multigpu_example.py) and [run_multigpu.SLURM](../src/t04/run_multigpu.SLURM).

<div style="text-align: justify;">
Once the two files are ready, submit the job using:
</div>

```bash
[smillas@front02 tutorial_04]$ sbatch run_multigpu.SLURM
```

<div style="text-align: justify;">
After the job finishes, navigate to the <code>logs/</code> directory and open the <code>multigpu_&lt;job_id&gt;.out</code> file and observe the difference.
</div>

```python
MASTER_ADDR: gpu06
MASTER_PORT: 31315
WORLD_SIZE: 2
Entering training loop...
Train Epoch: 1 [0/60000 (0%)]	    Loss: 2.319880
.
.
.
Train Epoch: 5 [27200/60000 (91%)]	Loss: 0.000118
Train Epoch: 5 [28800/60000 (96%)]	Loss: 0.000066
Exiting training loop...
Training time = 42.064579248428345
```

<div style="text-align: justify;">
By utilizing <b>multiple GPUs, we achieve a much faster training time</b>. Cyclone offers <b>4 GPUs per node</b>. But multiple nodes can be used to further speed up training with minimal changes to the code base.
</div>
<br>

### 4.6.4. Running Python Scripts on Multi-GPU (Multi-Node) with DDP

<div style="text-align: justify;"> 
Using the same parallelization technique and some simple changes to the previous SLURM and Python scripts, <b>more compute resources can be leveraged</b> to further speed up the AI models' training by utilizing multiple nodes.
<br><br>
To do this, some changes must first be made to the SLURM script. These changes <b>instruct the SLURM scheduler to allocate two GPUs on two nodes</b>, for a total of four GPUs.
</div>

```python
#SBATCH --nodes=2               # Number of nodes
#SBATCH --ntasks-per-node=2     # Tasks per node (GPUs per node)
#SBATCH --gpus-per-node=2       # Number of GPUs per node
```

<div style="text-align: justify;"> 
Next change is the addition of the <code>NODE_RANK</code> environment variable which will equal the unique identifier of the current node in the distributed setup. This can be obtained through the <code>$SLURM_NODEID</code> environment variable, provided by SLURM.
</div>

```python
export MASTER_ADDR=$(scontrol show hostname $SLURM_NODELIST | head -n 1)
export MASTER_PORT=$(shuf -i 29500-65535 -n 1)

export WORLD_SIZE=$(($SLURM_NNODES * $SLURM_NTASKS_PER_NODE))
export NODE_RANK=$SLURM_NODEID
```

> ℹ️ The full <code>run_multinode.SLURM</code> can be found [here](../src/t04/run_multinode.SLURM).

<div style="text-align: justify;"> 
In the Python script, the first change that must be made is the addition of the <code>NODE_RANK</code> global variable, which will be used in the worker function for logging purposes. 
</div>

```python
MASTER_ADDR = os.environ["MASTER_ADDR"]
MASTER_PORT = os.environ["MASTER_PORT"]
WORLD_SIZE = int(os.environ["WORLD_SIZE"])
NODE_RANK = int(os.environ["NODE_RANK"])
```

<div style="text-align: justify;"> 
In the <code>worker</code> function, the concepts of <code>local_rank</code> and <code>global_rank</code> are introduced and defined using the SLURM scheduler environment variables.
</div>

```python
global_rank = int(os.environ["SLURM_PROCID"])    
local_rank = int(os.environ["SLURM_LOCALID"])
```

<div style="text-align: justify;"> 
The  <code>global_rank</code> is the unique identity assigned to each process (or GPU) as part of the general <code>world</code> and is <b>used for inter-process communication and coordination across the entire cluster</b>. The <code>local_rank</code> is the unique identifier assigned to a process as part of a node and is <b>used to assign and manage GPU usage within a specific node in DDP</b>.
</div>
<br>

![Ranks diagram](../images/multinode.png)

<div style="text-align: justify;"> 
Moving on, a few changes must be made to the rank assignment on the various function calls. In the <code>torch.distributed.init_process_group()</code> the <code>global_rank</code> is used to uniquely identify each process in the distributed training across all nodes. It ensures proper coordination and communication in the entire distributed world.
</div>

```python
torch.distributed.init_process_group(
    backend='nccl', 
    world_size=WORLD_SIZE, 
    rank=global_rank,
    init_method='env://'
)
```

<div style="text-align: justify;"> 
Next, when setting the device, the <code>local_rank</code> is used to specify which GPU on the current node the process will use. <b>Each process must operate on a separate GPU within the same node.</b>
</div>

```python
torch.cuda.set_device(local_rank)
device = torch.device(f"cuda:{local_rank}")
```

<div style="text-align: justify;"> 
Afterwards, when downloading the dataset, <code>local_rank</code> is used to share the dataset with all other GPUs <b>on the same node</b>.
</div>

```python
 if local_rank == 0:
        train_dataset = datasets.MNIST('./data',
                       train=True, 
                       download=True, 
                       transform=transform)
```

<div style="text-align: justify;"> 
Furthermore, when wrapping the model with DDP, The <code>local_rank</code> is used to bind the DDP instance to the specific GPU that the process is operating on, ensuring the process handles only its assigned device.
</div>

```python
model = nn.parallel.DistributedDataParallel(model, device_ids=[local_rank])
```

<div style="text-align: justify;"> 
Lastly, when logging during training, the <code>global_rank</code> is used to avoid redundant log statements in the output.
</div>

```python
train(model=model, dataloader=train_loader, args=args, device=device, rank=global_rank)
```

> ℹ️ The full <code>cnn_multinode.py</code> can be found [here](../src/t04/multigpu_example.py).

<div style="text-align: justify;">
To run this example, first we need to create the <code>cnn_multinode.py</code> and <code>run_multinode.SLURM</code> as follows:
</div>

```bash
[smillas@front02 ~]$ cd $HOME/tutorial_04
[smillas@front02 tutorial_04]$ touch cnn_multinode.py
[smillas@front02 tutorial_04]$ nano cnn_multinode.py # copy the code from source Python file
[smillas@front02 tutorial_04]$ touch run_multinode.SLURM
[smillas@front02 tutorial_04]$ chmod +x run_multinode.SLURM # make the file executable
[smillas@front02 tutorial_04]$ nano run_multinode.SLURM # copy the source SLURM script
```

<span style="text-align: justify;">where the source files can be found from</span> [cnn_multinode.py](../src/t04/multigpu_example.py) and [run_multinode.SLURM](../src/t04/run_multinode.SLURM).

<div style="text-align: justify;">
Once the two files are ready, submit the job using:
</div>

```bash
[smillas@front02 tutorial_04]$ sbatch run_multigpu.SLURM
```

<div style="text-align: justify;">
After the job finishes, navigate to the <code>logs/</code> directory and open the <code>multinode_&lt;job_id&gt;.out</code> file and observe the difference.
</div>

```python
MASTER_ADDR: gpu06
MASTER_PORT: 57049
WORLD_SIZE: 4
NODE_RANK: 0
Rank 1 on Node 0: Initializing process group.
Rank 3 on Node 1: Initializing process group.
Rank 2 on Node 1: Initializing process group.
Rank 0 on Node 0: Initializing process group.
Entering training loop...
.
.
.
Train Epoch: 5 [12800/60000 (85%)]	Loss: 0.000021
Train Epoch: 5 [14400/60000 (96%)]	Loss: 0.000576
Exiting training loop...
Training time = 25.612423181533813
```

### 4.6.5. Runtime Results

<div style="text-align: justify;">
A comparison of each version with respect to a baseline setup. The baseline here is selected to be the single GPU version.
</div>

| **Version**     | **Number of GPUs** | **Runtime (s)** | **SpeedUp (times)**    |
| --------------- | ------------------ | --------------- | ---------------------- |
| CPU-only        | 0                  | 192.25          | 0.38 (or 2.63x slower) |
| Single GPU      | 1                  | 73.48           | 1                      |
| Single-node GPU | 2                  | 42.06           | **1.75**               |
| Multi-node GPU  | 4                  | 25.61           | **2.86**               |

---

## 4.7. Recap and Troubleshooting

<div style="text-align: justify;">
In this tutorial, we covered the process of scaling Python workloads on Cyclone, focusing on the following key concepts:

<ol>
<li><b>Resource Allocation with SLURM</b>
    <ul>
    <li>Setting up SLURM directives for various configurations, from single CPU to multi-node GPU training.</li>
    <li>Using environment variables such as MASTER_ADDR, MASTER_PORT, and WORLD_SIZE for distributed computing.</li>
    </ul>
</li>
<li><b>Python Script Modifications</b>
    <ul>
    <li>Adapting scripts for different hardware configurations (CPU, single GPU, multi-GPU, and multi-node setups).</li>
    <li>Leveraging DistributedDataParallel to automate data parallelism across GPUs.</li>
    </ul>
</ol>

While Using Cyclone for distributed training and complex computations, some issues may be encountered with regards to job submission or <code>RuntimeErrors</code>

<ol>
<li><b>SLURM job fails to launch</b>
    <ul>
    <li><b>Problem:</b> SLURM job fails with an error indicating incorrect directives.
        <ul>
        <li><b>Solution:</b> Double-check SLURM script parameters (<code>--nodes</code>, <code>--gpus-per-node</code>, <code>--partition</code>). Ensure they match the resources available in the partition.</li>
        </ul>
    </li>
    </ul>
</li>
<li><b>Runtime errors</b>
    <ul>
    <li><b>Problem:</b> Tensor or model mismatch errors during training.
        <ul>
        <li><b>Solution:</b> Ensure both the model and data tensors are moved to the correct device using <code>model.to(device)</code> and <code>data.to(device)</code>.</li>
        </ul>
    </li>
    </ul>
    <ul>
    <li><b>Problem:</b> Processes fail to communicate due to incorrect master address or port.
        <ul>
        <li><b>Solution:</b> Verify that <code>MASTER_ADDR</code> and <code>MASTER_PORT</code> are correctly set in the SLURM script and ensure network connectivity between nodes.</li>
        </ul>
    </li>
    </ul>
    <ul>
    <li><b>Problem:</b> Training does not scale as expected.
        <ul>
        <li><b>Solution:</b> Ensure efficient resource utilization by setting appropriate batch sizes and verifying GPU utilization using monitoring tools (e.g., <code>nvidia-smi</code>).</li>
        </ul>
    </li>
    </ul>
</li>
</ol>
</div>

---
