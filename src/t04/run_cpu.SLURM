#!/bin/bash
#SBATCH --job-name=pytorch_cpu                  # Job name
#SBATCH --nodes=1                               # Number of nodes
#SBATCH --cpus-per-task=10                      # CPUs per task
#SBATCH --time=02:00:00                         # Maximum runtime (HH:MM:SS)
#SBATCH --partition=cpu                         # Partition name
#SBATCH --output=HPC_tutorial/logs/cpu_%j.out   # Standard output log
#SBATCH --error=HPC_tutorial/logs/cpu_%j.err    # Standard error log

module load PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load torchvision/0.13.1-foss-2022a-CUDA-11.7.0

# Run Python script
srun  python HPC_tutorial/cpu_example.py \
    --batch_size 16 \
    --epochs 5 \
    --lr 0.001 \
