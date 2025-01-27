# run_hello_c.slurm
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
#SBATCH --job-name=hello_c         # Name of the job
#SBATCH --output=hello_c.out       # Output file for standard output
#SBATCH --error=hello_c.err        # Output file for error messages
#SBATCH --partition=cpu            # Which partition to run the job on (CPU partition)
#SBATCH --ntasks=1                 # Number of tasks (1 task for serial)
#SBATCH --time=00:10:00            # Maximum runtime (10 minutes)
#SBATCH --account=<your_account>   # Replace with your account name

module load GCC/11.3.0            # Load the GCC compiler module

# Compile the program
gcc -o hello hello.c

# Run the program using srun
srun ./hello