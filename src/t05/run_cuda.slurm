# run_cuda.slurm
#
# CaSToRC, The Cyprus Institute
#
# (c) 2024 The Cyprus Institute
#
# Contributing Authors:
# Christodoulos Stylianou (c.stylianou@cyi.ac.cy)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
#SBATCH --job-name=hello_gpu
#SBATCH --output=hello_gpu.out
#SBATCH --error=hello_gpu.err
#SBATCH --partition=gpu            # Use GPU partition
#SBATCH --ntasks=1                 # Single task
#SBATCH --gres=gpu:1               # Request one GPU
#SBATCH --time=00:10:00            # Maximum runtime (10 minutes)
#SBATCH --account=<your_account>   # Replace with your account

module load CUDA/12.1.1            # Load CUDA module

# Compile the program
nvcc -o hello_gpu hello_gpu.cu

# Run the program
srun ./hello_gpu