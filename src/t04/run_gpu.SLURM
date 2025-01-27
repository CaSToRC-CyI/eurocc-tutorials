#!/bin/bash
#SBATCH --job-name=pytorch_gpu                  # Job name
#SBATCH --nodes=1                               # Number of nodes
#SBATCH --ntasks-per-node=1                     # Tasks per node (GPUs per node)
#SBATCH --gpus-per-node=1                       # GPUs per node
#SBATCH --cpus-per-task=6                       # CPUs per task
#SBATCH --time=02:00:00                         # Maximum runtime (HH:MM:SS)
#SBATCH --partition=gpu                         # Partition name
#SBATCH --output=HPC_tutorial/logs/gpu_%j.out   # Standard output log
#SBATCH --error=HPC_tutorial/logs/gpu_%j.err    # Standard error log

module load PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load cuDNN/8.4.1.50-CUDA-11.7.0
module load torchvision/0.13.1-foss-2022a-CUDA-11.7.0
module load CUDA/11.7.0

# Run Python script
srun  python HPC_tutorial/gpu_example.py \
    --batch_size 16 \
    --epochs 5 \
    --lr 0.001 \
