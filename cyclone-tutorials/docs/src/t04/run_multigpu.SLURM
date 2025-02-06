#!/bin/bash
#SBATCH --job-name=pytorch_distributed_multigpu         # Job name
#SBATCH --nodes=1                                       # Number of nodes
#SBATCH --ntasks-per-node=2                             # Tasks per node (GPUs per node)
#SBATCH --gpus-per-node=2                               # GPUs per node
#SBATCH --cpus-per-task=6                               # CPUs per task
#SBATCH --time=02:00:00                                 # Maximum runtime (HH:MM:SS)
#SBATCH --partition=gpu                                 # Partition name
#SBATCH --output=logs/multigpu_%j.out      # Standard output log
#SBATCH --error=logs/multigpu_%j.err       # Standard error log

module load CUDA/11.7.0
module load NCCL/2.12.12-GCCcore-11.3.0-CUDA-11.7.0
module load PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load cuDNN/8.4.1.50-CUDA-11.7.0
module load torchvision/0.13.1-foss-2022a-CUDA-11.7.0

# Get master node and port
export MASTER_ADDR=$(scontrol show hostname $SLURM_NODELIST | head -n 1)
export MASTER_PORT=$(shuf -i 29500-65535 -n 1)

# Set WORLD_SIZE and NODE_RANK
export WORLD_SIZE=$(($SLURM_NNODES * $SLURM_NTASKS_PER_NODE))

# Debugging info
echo "MASTER_ADDR: $MASTER_ADDR"
echo "MASTER_PORT: $MASTER_PORT"
echo "WORLD_SIZE: $WORLD_SIZE"

# Run Python script
srun --export=ALL python multigpu_example.py \
    --batch_size 16 \
    --epochs 5 \
    --lr 0.001
