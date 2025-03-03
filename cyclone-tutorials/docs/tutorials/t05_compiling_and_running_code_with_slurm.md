<!--
 t05_compiling_and_running_code_with_slurm.md

 CaSToRC, The Cyprus Institute

 (c) 2024 The Cyprus Institute

 Contributing Authors:
 Simone Bacchio (s.bacchio@cyi.ac.cy)
 Christodoulos Stylianou (c.stylianou@cyi.ac.cy)
 Spyroulla Mavrommati (s.mavrommati@cyi.ac.cy)
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
# 5. Compiling and Running C/C++ Code on Cyclone with SLURM

## 5.1. Overview
<div style="text-align: justify; margin-bottom: 15px;">
This tutorial teaches participants how to <b>compile and run C/C++ programs on Cyclone using SLURM</b> in various configurations. Participants will start with simple <b>"Hello, World" programs</b> and progress through advanced setups such as <b>multi-threaded</b>, <b>GPU-accelerated</b>, and <b>distributed (MPI)</b> programs. Note that the purpose of this tutorial is <b>not</b> to teach how to write parallel application, rather to demonstrate how SLURM enables effective resource utilization for C/C++ applications in HPC.
</div>

---

## 5.2. Learning Objectives
<div style="text-align: justify; margin-bottom: 15px;">
By the end of this tutorial, participants will be able to:
<ol>
    <li>Compile and execute C/C++ programs on Cyclone in various configurations (serial, multi-threaded, GPU, and distributed).</li>
    <li>Write SLURM scripts to run C/C++ programs using appropriate resource allocations.</li>
    <li>Understand how to utilize MPI, OpenMP, and CUDA for scaling C/C++ workloads.</li>
    <li>Identify and address common errors when compiling and running C/C++ code on Cyclone.</li>
</ol>
</div>

---

## 5.3. Prerequisites

1. [T01 - Introduction to HPC Systems](t01_introduction_to_hpc_systems.md): This tutorial will give you some basic knowledge on HPC systems and basic terminologies.


2. [T02 - Accessing and Navigating Cyclone:](t02_accessing_and_navigating_cyclone.md)This tutorial will give you some basic knowledge on how to connect, copy files and navigate the HPC system. 


3. [T03 - Setting Up and Using Development Tools:](t03_setting_up_and_using_development_tools.md) This tutorial will give you some basic knowledge on how to connect, copy files and navigate the HPC system. 
   
---

## 5.4. Introduction to Compiling and Running C/C++ on Cyclone
<div style="text-align: justify; margin-bottom: 15px;">
The tutorial begins by introducing Cyclone’s compiler environment. Participants will gain an understanding of the available compilers, such as gcc for general C/C++ compilation, nvcc for GPU programming, and mpicc for distributed MPI applications. This section provides a high-level overview of the workflow, preparing participants for hands-on implementation.
</div>

### 5.4.1. High-Level Overview of the Workflow for Compiling and Running C/C++ Code on Cyclone
<div style="text-align: justify; margin-bottom: 15px;">
The process of compiling and running C/C++ programs on Cyclone involves several key steps to ensure efficient execution on the HPC system. Both compilation and code execution should take place on the compute nodes of Cyclone. However, for small compilation times (e.g., a few seconds) the compilation can also take place on the login nodes. Here’s an overview of the workflow that assumes compilation on the login nodes:
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<ol>
<li><b>Write Your C/C++ Code:</b> First, you will write your C or C++ source code using your preferred text editor or integrated development environment (IDE). This code could range from simple serial programs to complex multi-threaded or GPU-accelerated applications.</li>

<li><b>Select the Appropriate Compiler:</b> Depending on your application’s needs, choose the appropriate compiler. Cyclone offers a variety of compilers, including <b>gcc</b> (GNU Compiler Collection), <b>Intel compilers</b>, <b>LLVM</b> (Clang), and <b>nvcc</b> for CUDA-based programs. You can use <b>modules</b> to load the desired compiler version based on your program's requirements.</li>

<li><b>Compile the Code:</b> Using the selected compiler, you will compile your C/C++ code. This step converts the source code into an executable program. If necessary, you can add flags to enable optimizations (please see <a href="#546-using-optimisation-flags">here</a>) or link with external libraries (e.g., for parallel processing or GPU computation). Note that for lightweight compilation (i.e., few files), this can take place on the login nodes. Otherwise if a library (or a big codebase) is compiled, this must be done in the compute nodes and by submiting a job via SLURM.</li>

<li><b>Write a SLURM Job Script:</b> To run your code on Cyclone, you will write a <b>SLURM job script</b>. This script specifies how many CPU cores, how much memory, and which partition to use for your job. It also includes the commands to run your C/C++ compiled program. SLURM helps manage the allocation of resources and ensures fair access to the system. <b>Note</b> that if you are compiling on the compute nodes through SLURM, you can create two different scripts -one for compiling the code, and one for running it- to avoid recompiling the code every time.</li>

<li><b>Submit the Job to SLURM:</b> After compiling the program, you will submit your job to SLURM using the <code>sbatch</code> command. SLURM will handle resource allocation and job execution based on your job script’s configuration.</li>

<li><b>Monitor and Debug:</b> While your job is running, you can monitor its status using commands like <code>squeue</code> (to see running jobs) or <code>sacct</code> (to check completed jobs). If issues arise, you can debug your program by adjusting the SLURM script, compiling with different flags, or checking for errors in the job's output.</li>

<li><b>Post-Execution:</b> Once the job finishes, you can review the output and results. If there are issues or further optimization is needed, you may need to modify your code, recompile, and adjust your SLURM job script accordingly.</li>
</ol>
This workflow ensures that your C/C++ applications are compiled, run, and optimized efficiently on the Cyclone HPC system, leveraging SLURM for resource management and scalability.
</div>

### 5.4.2. Available Compilers on Cyclone

<div style="text-align: justify; margin-bottom: 15px;">
Cyclone offers several compilers, each suited for different types of C/C++ workloads. The table below summarizes the compilers available and their corresponding C and C++ compilers:
</div>

| **Compiler Collection**     | **Description**                                                                                                      | **C Compiler** | **C++ Compiler** | **Compiling Example**                      |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------- | ---------------- | ------------------------------------------ |
| **GNU Compiler Collection** | The standard compiler for general-purpose C/C++ programs. Optimized for general tasks.                               | `gcc`          | `g++`            | `gcc -o my_program my_program.c`           |
| **Intel C/C++ Compilers**   | High-performance compilers optimized for Intel CPUs. Offers better optimization for Intel hardware.                  | `icc`          | `icpc`           | `icc -o my_program my_program.c`           |
| **NVIDIA CUDA Compiler**    | NVIDIA’s compiler for CUDA, used for compiling GPU-accelerated programs. Specifically for GPU workloads.             | `nvcc`         | `nvcc`           | `nvcc -o my_gpu_program my_gpu_program.cu` |
| **MPI Compiler**            | Compiler for distributed programs using MPI, which enables communication across multiple nodes.                      | `mpicc`        | `mpicxx`         | `mpicc -o my_mpi_program my_mpi_program.c` |
| **LLVM**                    | A compiler infrastructure that supports various programming languages. Known for advanced optimization capabilities. | `clang`        | `clang++`        | `clang -o my_program my_program.c`         |

### 5.4.3. How to Change Compilers Using Modules

<div style="text-align: justify; margin-bottom: 15px;">
To view the available compilers on Cyclone, use the following command:
</div>

```bash
module avail $COMPILER_NAME
```

<div style="text-align: justify; margin-bottom: 15px;">
where <code>$COMPILER_NAME</code> can be <code>GCC</code>, <code>intel-compilers</code>, <code>LLVM</code>, <code>CUDA</code> or <code>OpenMPI</code>, representing all available versions for each compiler vendor.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
An example output at the time of writing this tutorial can be:
</div>

```bash
[cstyl@front02 ~]$ module spider GCC

----------------------------------------------------------------------------
  GCC:
----------------------------------------------------------------------------
    Description:
      The GNU Compiler Collection includes front ends for C, C++,
      Objective-C, Fortran, Java, and Ada, as well as libraries for these
      languages (libstdc++, libgcj,...).

     Versions:
        GCC/8.3.0
        GCC/10.2.0
        GCC/11.2.0
        GCC/11.3.0
        GCC/12.2.0
        GCC/12.3.0
        GCC/13.2.0
     Other possible modules matches:
        GCCcore
```

<div style="text-align: justify; margin-bottom: 15px;">
To use a specific compiler, you need to load the corresponding module. Following the previous example, to load <code>v11.2.0</code> of <code>GCC</code>:
</div>

```bash
[cstyl@front02 ~]$ gcc --version
gcc (GCC) 8.5.0 20210514 (Red Hat 8.5.0-10)
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

[cstyl@front02 ~]$ module load GCC/11.2.0
[cstyl@front02 ~]$ gcc --version
gcc (GCC) 11.2.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

<div style="text-align: justify; margin-bottom: 15px;">
This command will load <code>GCC</code> version <code>11.2.0</code>, and all subsequent compilation commands will use this version.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
If you want to switch to a different compiler version, use:
</div>

```bash
[cstyl@front02 ~]$ module swap GCC GCC/12.3.0 

The following have been reloaded with a version change:
  1) GCC/11.2.0 => GCC/12.3.0
  2) GCCcore/11.2.0 => GCCcore/12.3.0
  3) binutils/2.37-GCCcore-11.2.0 => binutils/2.40-GCCcore-12.3.0
  4) zlib/1.2.11-GCCcore-11.2.0 => zlib/1.2.13-GCCcore-12.3.0

[cstyl@front02 ~]$ gcc --version
gcc (GCC) 12.3.0
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```
<div style="text-align: justify; margin-bottom: 15px;">
Similar process can be followed for all other available compilers.
</div>

---

## 5.5. Serial C/C++ Programs

<div style="text-align: justify; margin-bottom: 15px;">
In this section, we will start with a basic "<i>Hello, World</i>" C program to understand the workflow for compiling and running serial programs on Cyclone. You will learn how to compile a C program using the <b>gcc</b> compiler, write a simple <b>SLURM</b> job script to run the program on a single CPU core, and submit the job for execution.
</div>

### 5.5.1. Write the "Hello, World" C Program

<div style="text-align: justify; margin-bottom: 15px;">
First, create a <b><i>simple C program</i></b> that prints "<i>Hello, World from Cyclone!</i>" to the console. This program will serve as our example for compiling and running a serial C program.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>hello.c</code> 
</div>

```bash
[cstyl@front02 ~]$ cd $HOME
[cstyl@front02 ~]$ mkdir tutorial_05
[cstyl@front02 ~]$ cd tutorial_05
[cstyl@front02 tutorial_05]$ touch hello.c
[cstyl@front02 tutorial_05]$ nano hello.c # copy the C code below
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following code:
</div>

```c
#include <stdio.h>

int main() {
    printf("Hello, World from Cyclone!\n");
    return 0;
}
```

### 5.5.2. Write the SLURM Job Script

<div style="text-align: justify; margin-bottom: 15px;">
Next, you will create a <b><i>simple SLURM job script</i></b> to compile and run your program on Cyclone. This script will request the necessary resources (a single CPU core in this case) and manage the execution of the program.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>run_hello_c.slurm</code> 
</div>

```bash
[cstyl@front02 tutorial_05]$ touch run_hello_c.slurm
[cstyl@front02 tutorial_05]$ nano run_hello_c.slurm # copy the SLUMR contents below
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following contents:
</div>

```bash 
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
```

<div style="text-align: justify; margin-bottom: 15px;">
In this script:
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<ul>
<li><code>#SBATCH</code> directives are used to specify job settings such as the job name, output and error file locations, partition (CPU), and the amount of time allowed for the job to run.</li>
<li>The module load command loads the required GCC compiler module for compiling the program.</li>
<li><code>gcc -o hello hello.c</code> compiles the C program using the gcc compiler and generates an executable called hello.</li>
<li><code>srun ./hello</code> runs the compiled program using srun, which ensures that the job is executed according to SLURM’s resource management system.</li>
</ul>
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<blockquote>
<i>ℹ️ It is worth pointing out that the compilation of such a small code could have been done directly on the login node, or on a separate SLURM script so that we avoid recompiling every time we want to run the example.</i>
</blockquote>
</div>

### 5.5.3. Submit the Job
<div style="text-align: justify; margin-bottom: 15px;">
Now that you’ve written both the C program and the SLURM job script, you can submit your job to SLURM using the sbatch command:
</div>

```bash
[cstyl@front02 tutorial_05]$ sbatch run_hello_c.slurm
```

<div style="text-align: justify; margin-bottom: 15px;">
This command submits your job script to SLURM, which will allocate the requested resources (in this case, one CPU core) and execute the program. SLURM will place the job in the queue, and once resources are available, it will run your program.
</div>

### 5.5.4. Monitor the Job
<div style="text-align: justify; margin-bottom: 15px;">
After submitting the job, you can monitor its status using the squeue command:
</div>

```bash
squeue -u <your_username>
```

<div style="text-align: justify; margin-bottom: 15px;">
This will show the status of your job in the queue. Once the job is completed, you can check the output and error files to see the results and any messages generated during execution.
</div>

```bash
[cstyl@front02 tutorial_05]$ cat hello_c.out    # Check the output
Hello, World from Cyclone!
[cstyl@front02 tutorial_05]$ cat hello_c.err    # Check for any error messages (if any)
```

### 5.5.5. Using Alternative Compilers

<div style="text-align: justify; margin-bottom: 15px;">
Sometimes any of the alternative compilers available on Cyclone are desired to be used, such as Intel Compilers which can sometimes offer performance optimizations on Intel CPUs. If you wish to use the Intel compiler instead of GCC, you can modify your job script by replacing the GCC module with the Intel module and using the Intel compiler commands:
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Modify the job script to load the Intel module:
</div>

```bash
[cstyl@front02 tutorial_05]$ module load intel-compilers/2022.2.1    # Load the Intel compiler module
[cstyl@front02 tutorial_05]$ icc -o hello hello.c                    # Compile using Intel compiler (icc)
```

<div style="text-align: justify; margin-bottom: 15px;">
The rest of the process remains the same. You can submit and monitor the job as you did before, using the Intel compiler for potential performance improvements.
</div>

### 5.5.6. Using Optimisation Flags

#### General Optimization Levels
<div style="text-align: justify; margin-bottom: 15px;">
<ul>
<li><b><code>-O0</code></b>: No optimization (default).</li>
<li><b><code>-O1</code></b>: Basic optimizations.</li>
<li><b><code>-O2</code></b>: Moderate optimizations without impacting debugging.</li>
<li><b><code>-O3</code></b>: Aggressive optimizations, often enabling vectorization and loop unrolling.</li>
</ul>
</div>

#### Advanced Flags
<div style="text-align: justify; margin-bottom: 15px;">
<ul>
<li><b><code>-ffast-math</code></b>: Enables faster floating-point calculations (may reduce precision).</li>
<li><b><code>-funroll-loops</code></b>: Unrolls loops to reduce overhead.</li>
<li><b><code>-march=native</code></b>: Optimizes code for the architecture of the system being used.</li>
<li><b><code>-flto</code></b>: Enables link-time optimization.</li>
<li><b><code>-fopenmp</code></b>: Enables OpenMP for parallel programming.</li>
</ul>
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<blockquote>
<i>ℹ️ Each compiler has its specific flags. Refer to its documentation for more options.</i>
</blockquote>
</div>

#### Compile with Optimization
```bash
[cstyl@front02 tutorial_05]$ gcc -O3 -march=native -funroll-loops hello.c -o hello
```

<div style="text-align: justify; margin-bottom: 15px;">
Compiling code with <code>-O3 -march=native -funroll-loops</code> will result in faster execution runtimes.
</div>

---

## 5.6. Multi-Threaded (OpenMP) C/C++ Programs
<div style="text-align: justify; margin-bottom: 15px;">
Modern HPC systems, such as Cyclone, provide multiple cores and threads, making parallelism an essential aspect of achieving high performance. <a href="https://www.openmp.org">OpenMP (Open Multi-Processing)</a> is a widely used API for parallel programming in C, C++, and Fortran. It enables shared-memory parallelism by allowing programs to split tasks across multiple threads.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
OpenMP uses compiler directives (pragmas) to parallelize code without major modifications. By adding <code>#pragma</code> statements, loops or sections of code can be executed concurrently within a single node and on multiple cores.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
To compile programs with OpenMP support, you need to use the following flags:
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<ul>
<li><b>GCC</b>: <code>-fopenmp</code></li>
<li><b>Intel Compiler</b>: <code>-qopenmp</code></li>
<li><b>Clang</b>: <code>-fopenmp</code> (requires linking to the <code>libomp</code> library)</li>
</ul>
</div>

<div style="text-align: justify; margin-bottom: 15px;">
For example, assuming we are compiling the source file <code>hello_openmp.c</code> that contains OpenMP code. Then the compilation step, if <b>compiling with GNU compilers</b>, would look like:
</div>

```bash
[cstyl@front02 tutorial_05]$ gcc -O3 -fopenmp hello_openmp.c -o hello_openmp
```

<div style="text-align: justify; margin-bottom: 15px;">
or, if <b>compiling with Intel Compilers</b>:
</div>

```bash
[cstyl@front02 tutorial_05]$ icc -O3 -qopenmp hello_openmp.c -o hello_openmp
```

### 5.6.1. Write the OpenMP "Hello, World" C Program

<div style="text-align: justify; margin-bottom: 15px;">
First, create a <b><i>simple OpenMP program</i></b> that prints "<i>Hello, World from thread $THREAD_ID out of $TOTAL_THREADS!</i>" to the console.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>hello_openmp.c</code> 
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ touch hello_openmp.c
[cstyl@front02 tutorial_05]$ nano hello_openmp.c # copy the C code below
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following code:
</div>

```c
#include <stdio.h>
#include <omp.h>
int main() {
    #pragma omp parallel
    {
        printf("Hello from thread %d out of %d\n", omp_get_thread_num(), omp_get_num_threads());
    }
    return 0;
}
```

<div style="text-align: justify; margin-bottom: 15px;">
<blockquote>
<i>⚠️ <b>Notice</b> the addition of <code>#pragma omp parallel</code> and the curly brackets, indicating that the enclosed code is code running in parallel across multiple threads.</i> 
</blockquote>
</div>

### 5.6.2. Write the SLURM Job Script

<div style="text-align: justify; margin-bottom: 15px;">
Next, you will create a SLURM job script to run your program on Cyclone. This script will request the necessary resources (a single CPU core in this case) and manage the execution of the program.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>run_openmp.slurm</code> 
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ touch run_openmp.slurm
[cstyl@front02 tutorial_05]$ chmod +x run_openmp.slurm # make the file executable
[cstyl@front02 tutorial_05]$ nano run_openmp.slurm
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following code:
</div>

```bash 
#!/bin/bash
#SBATCH --job-name=openmp
#SBATCH --output=openmp.out
#SBATCH --error=openmp.err
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8       # Runs on 8 threads
#SBATCH --time=00:15:00
#SBATCH --account=<your_account>

module load GCC/11.3.0

export OMP_NUM_THREADS=8
srun ./hello_openmp
```

<div style="text-align: justify; margin-bottom: 15px;">
In this script, the main differences from the Serial case are:
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<ul>
<li><code>#SBATCH --cpus-per-task=8</code> launches a task that runs on 8 threads (CPU cores). In practise, this number can go up to <code>40</code> (i.e., the maximum number of CPU cores available on each node).</li>
<li><code>export OMP_NUM_THREADS=8</code> sets the <code>OMP_NUM_THREADS</code> environment variable. This ensures that OpenMP's runtime will be correctly set to operate with 8 threads, where needed.</li>
</ul>
</div>

### 5.6.3. Submit the Job

<div style="text-align: justify; margin-bottom: 15px;">
Now that you’ve written both the OpenMP program and the SLURM job script, the last step is to compile your code. You can compile the code from the login node by:
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ module load GCC/11.3.0
[cstyl@front02 tutorial_05]$ gcc -O3 -fopenmp hello_openmp.c -o hello_openmp
```

<div style="text-align: justify; margin-bottom: 15px;">
Now, you are ready to submit your job to SLURM using the sbatch command:
</div>

```bash
[cstyl@front02 tutorial_05]$ sbatch run_openmp.slurm
```

<div style="text-align: justify; margin-bottom: 15px;">
This command submits your job script to SLURM, which will allocate the requested resources (in this case, one CPU core) and execute the program. SLURM will place the job in the queue, and once resources are available, it will run your program.
</div>

### 5.6.4. Monitor the Job
<div style="text-align: justify; margin-bottom: 15px;">
After submitting the job, you can monitor its status using the squeue command:
</div>

```bash
squeue -u <your_username>
```

<div style="text-align: justify; margin-bottom: 15px;">
This will show the status of your job in the queue. Once the job is completed, you can check the output and error files to see the results and any messages generated during execution.
</div>

```bash
[cstyl@front02 tutorial_05]$ cat openmp.out    # Check the output
Hello from thread 5 out of 8
Hello from thread 6 out of 8
Hello from thread 2 out of 8
Hello from thread 3 out of 8
Hello from thread 1 out of 8
Hello from thread 0 out of 8
Hello from thread 7 out of 8
Hello from thread 4 out of 8
[cstyl@front02 tutorial_05]$ cat openmp.err    # Check for any error messages
```

---

## 5.7. GPU-Accelerated C/C++ Programs

<div style="text-align: justify; margin-bottom: 15px;">
In this section, the objective is to learn how to extend C/C++ programs to leverage the power of GPU acceleration using CUDA. The section begins with a basic "Hello, World" example, demonstrating how to write a CUDA kernel, compile and run it on the GPU. We will also learn how to write SLURM job scripts to request GPU resources, compile their programs using the <code>nvcc</code> compiler, and execute them on the available GPUs in Cyclone. This section serves as an introduction to CUDA programming, providing a foundation for more complex GPU-accelerated applications.
</div>

### 5.7.1. Write the GPU-Accelerated Program

<div style="text-align: justify; margin-bottom: 15px;">
First, create a <b><i>simple CUDA program</i></b> that prints "<i>Hello, World from GPU thread $THREAD_ID!</i>" to the console. 
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>hello_cuda.cu</code> 
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ touch hello_cuda.cu
[cstyl@front02 tutorial_05]$ nano hello_cuda.cu
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following code:
</div>

```c
#include <stdio.h>
#include <cuda_runtime.h>

__global__ void helloFromGPU() {
    printf("Hello, World from GPU thread %d\n", threadIdx.x);
}

int main() {
    helloFromGPU<<<1, 10>>>();
    cudaDeviceSynchronize();
    return 0;
}
```

<div style="text-align: justify; margin-bottom: 15px;">
This CUDA program demonstrates how to leverage the GPU for parallel execution. The <code>helloFromGPU</code> function is marked with the <code>__global__</code> keyword, indicating that it will run on the GPU-this function is also known as the kernel. The program <b><i>launches 10 threads in a single block</i></b> using the syntax <code>helloFromGPU<<<1, 10>>>();</code>, where the first parameter specifies the number of blocks (1 in this case) and the second parameter specifies the number of threads per block (10 threads). Each thread runs the same function, but since each thread has a unique <code>threadIdx.x</code>, it prints a message with its own thread index (e.g., "Hello, World from GPU thread 0", "Hello, World from GPU thread 1", etc.). The program uses <code>cudaDeviceSynchronize();</code> to ensure that the CPU waits for all GPU threads to finish before the program exits, which is important for ensuring that all output is printed correctly.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
The key GPU-specific concepts in this program include <b>thread management</b> and <b>parallel execution</b>. CUDA allows for running thousands of threads in parallel, and in this case, 10 threads run concurrently in one block. Each thread executes the <code>helloFromGPU</code> function and prints its thread index. This program serves as a basic example of how to use CUDA for GPU-accelerated tasks, illustrating how thread indices can be used to manage parallel work. The <code>__global__</code> function is executed on the GPU, and the threads work in parallel to output their unique results, making this an effective demonstration of how to perform parallel processing on the GPU in high-performance computing environments.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
A detailed explanation on the CUDA programming model can be found on NVIDIA's <a href="https://docs.nvidia.com/cuda/cuda-c-programming-guide/">CUDA Programming Guide</a>.
</div>

### 5.7.2. SLURM Job Script for GPU

<div style="text-align: justify; margin-bottom: 15px;">
Next, you will create a SLURM job script to run your program on Cyclone. This script will request the necessary resources and manage the execution of the program. 
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>run_cuda.slurm</code> 
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ touch run_cuda.slurm
[cstyl@front02 tutorial_05]$ chmod +x run_cuda.slurm # make the file executable
[cstyl@front02 tutorial_05]$ nano run_cuda.slurm
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following code:
</div>

```bash
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

# Run the program
srun ./hello_gpu
```

<div style="text-align: justify; margin-bottom: 15px;">
In this script:
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<ul>
<li><code>--gres=gpu:1</code> specifies the request for one GPU. Maximum number of GPUs allowed per node is <code>4</code>.</li>
<li><code>--partition=gpu</code> is required to be able to use the part of the system with the GPUs.</li>
<li><code>module load CUDA/12.1.1</code> loads the CUDA compiler and relevant libraries for GPU programming.</li>
</ul>
</div>

### 5.7.3. Submit and Monitor the Job
<div style="text-align: justify; margin-bottom: 15px;">
Now that you’ve written both the CUDA program and the SLURM job script, the last step is to compile your code for GPU execution. You can compile the code from the login node by:
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ module load CUDA/12.1.1
[cstyl@front02 tutorial_05]$ nvcc -arch=sm_70  -o hello_gpu hello_cuda.cu
```

<div style="text-align: justify; margin-bottom: 15px;">
<blockquote>
<i>⚠️ It is important to use the <code>-arch=sm_70</code> in order to generate correct code for the V100 GPU.</i>
</blockquote>
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Now, you are ready to submit your job to SLURM using the sbatch command:
</div>

```bash
[cstyl@front02 tutorial_05]$ sbatch run_cuda.slurm
```

<div style="text-align: justify; margin-bottom: 15px;">
Monitor the job with squeue and check the output:
</div>

```bash
[cstyl@front02 tutorial_05]$ cat hello_gpu.out    # View output
Hello, World from GPU thread 0
Hello, World from GPU thread 1
Hello, World from GPU thread 2
Hello, World from GPU thread 3
Hello, World from GPU thread 4
Hello, World from GPU thread 5
Hello, World from GPU thread 6
Hello, World from GPU thread 7
Hello, World from GPU thread 8
Hello, World from GPU thread 9
[cstyl@front02 tutorial_05]$ cat hello_gpu.err    # View error messages (if any)
```

---

## 5.8. MPI C/C++ Programs
<div style="text-align: justify; margin-bottom: 15px;">
In this section, participants will learn how to write and run <a href="https://www.mpi-forum.org">MPI (Message Passing Interface)</a> programs, enabling parallel processing across multiple nodes and processors. MPI is a widely used standard for distributed computing, allowing different parts of a program to run concurrently on separate nodes in a cluster, sharing data and coordinating execution. The section begins with a basic MPI "Hello, World" program, where participants will use mpicc, the MPI compiler, to compile and run a simple parallel program across multiple tasks. As they progress, they will gain a deeper understanding of how to structure MPI programs for distributed computation, set up communication between processes, and utilize SLURM to manage resource allocation for MPI-based jobs on Cyclone.
</div>

### 5.8.1. Write an MPI "Hello, World" Program
<div style="text-align: justify; margin-bottom: 15px;">
First, create a <b><i>simple MPI program</i></b> that prints "<i>Hello, World from rank $PROCESS_ID of $NUMBER_OF_PROCESSES!</i>" to the console. 
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>hello_mpi.c</code> 
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ touch hello_mpi.c
[cstyl@front02 tutorial_05]$ nano hello_mpi.c
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following code:
</div>

```c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    printf("Hello, World from rank %d of %d!\n", rank, size);
    MPI_Finalize();
    return 0;
}
```

<div style="text-align: justify; margin-bottom: 15px;">
The MPI "Hello, World" program is a simple example that demonstrates how to use the <b>Message Passing Interface (MPI)</b> to run a program across multiple processes. The program begins by initializing MPI with the <code>MPI_Init</code> function and then retrieves the rank (unique identifier) of each process using <code>MPI_Comm_rank</code>. It also determines the total number of processes running by calling <code>MPI_Comm_size</code>. Each process then prints a message, including its rank and the total number of processes involved, using the <code>printf</code> function. This allows each process to output "Hello, World" from its own unique rank, showing how parallel processes can execute the same code but interact independently.
</div>

<div style="text-align: justify; margin-bottom: 15px;">
The program ends by finalizing MPI with <code>MPI_Finalize</code>, which ensures proper shutdown of the MPI environment. The use of MPI allows the program to scale across multiple nodes and processors, where each process executes in parallel. This simple example forms the foundation for more complex parallel programs where processes can communicate with each other, pass data, and work together to solve larger problems.
</div>

### 5.8.2. SLURM Job Script for MPI
<div style="text-align: justify; margin-bottom: 15px;">
Next, you will create a SLURM job script to run your program on Cyclone. This script will request the necessary resources and manage the execution of the program. 
</div>

<div style="text-align: justify; margin-bottom: 15px;">
Create a file called <code>run_mpi.slurm</code> 
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ touch run_mpi.slurm
[cstyl@front02 tutorial_05]$ chmod +x run_mpi.slurm # make the file executable
[cstyl@front02 tutorial_05]$ nano run_mpi.slurm
```

<div style="text-align: justify; margin-bottom: 15px;">
and add the following code:
</div>

```bash
#!/bin/bash
#SBATCH --job-name=hello_mpi
#SBATCH --output=hello_mpi.out
#SBATCH --error=hello_mpi.err
#SBATCH --partition=cpu
#SBATCH --ntasks=4                  # Runs on 4 Processes
#SBATCH --time=00:10:00
#SBATCH --account=<your_account>

module load OpenMPI/4.1.6-GCC-13.2.0

# Run the program
srun ./hello_mpi
```

<div style="text-align: justify; margin-bottom: 15px;">
In this script:
</div>

<div style="text-align: justify; margin-bottom: 15px;">
<ul>
<li>The <code>--ntasks=4</code> directive allocates 4 tasks (one per MPI process).</li>
<li>The script loads the appropriate MPI module using <code>module load OpenMPI/4.1.6-GCC-13.2.0</code>, ensuring that the MPI libraries are available.</li>
<li>It then compiles the MPI program using <code>mpicc</code> compiler by <a href="https://www.open-mpi.org">OpenMPI</a> and specifies the output executable </<code>hello_mpi</code>.</li>
<li>Finally, <code>srun</code> is used to run the MPI program across the allocated tasks. The script ensures that the job runs on 4 tasks and that each process executes the MPI program in parallel, distributing the workload across the compute nodes.</li>
</ul>
</div>

### 5.8.3. Submit and Monitor the Job
<div style="text-align: justify; margin-bottom: 15px;">
Now that you’ve written both the MPI program and the SLURM job script, the last step is to compile your code for distributed execution. You can compile the code from the login node by:
</div>

```bash
[cstyl@front02 ~]$ cd $HOME/tutorial_05
[cstyl@front02 tutorial_05]$ module load OpenMPI/4.1.6-GCC-13.2.0
[cstyl@front02 tutorial_05]$ mpicc -o hello_mpi hello_mpi.c
```

<div style="text-align: justify; margin-bottom: 15px;">
Now, you are ready to submit your job to SLURM using the sbatch command:
</div>

```bash
[cstyl@front02 tutorial_05]$ sbatch run_mpi.slurm
```

<div style="text-align: justify; margin-bottom: 15px;">
Monitor the job with squeue and check the output:
</div>

```bash
[cstyl@front02 tutorial_05]$ cat hello_mpi.out    # View output
Hello, World from rank 0 of 4!
Hello, World from rank 2 of 4!
Hello, World from rank 1 of 4!
Hello, World from rank 3 of 4!
[cstyl@front02 tutorial_05]$ cat hello_mpi.err    # View error messages (if any)
```

---

<!-- ## 5.9. Hybrid MPI+X Programs
The final configuration combines MPI with either OpenMP for multi-threading or CUDA for GPU acceleration, introducing hybrid programming techniques. Participants will learn to write hybrid C/C++ programs, compile them with appropriate compilers, and create SLURM scripts for hybrid execution. 

--- -->

## 5.9. Recap and Troubleshooting
<div style="text-align: justify; margin-bottom: 15px;">
This tutorial covered various methods for compiling and running C/C++ programs on Cyclone, including serial, multi-threaded, GPU-accelerated, and distributed (MPI) applications. You learned how to use SLURM for resource management and job execution, and how to leverage multiple compilers (e.g., GCC, Intel, CUDA, and MPI) to optimize program performance.
</div>

#### Common Issues and Troubleshooting
<div style="text-align: justify; margin-bottom: 15px;">
<ol>
<li><b>Compiler Not Found:</b> Ensure the correct module is loaded (e.g., module load GCC/11.3.0).</li>
<li><b>CUDA Errors:</b> If CUDA programs fail to run on GPUs, verify the correct CUDA module is loaded and that GPU resources are requested properly (e.g., with <code>--gres=gpu:1</code>).</li>
<li><b>MPI Job Failures:</b> If MPI jobs do not execute, check the job status with squeue and ensure the correct number of tasks is allocated (--ntasks=4).</li>
<li><b>General Debugging:</b> Use the SLURM job script's output and error files to investigate issues during compilation and execution, adjusting flags or resource requests accordingly.</li>
</ol>
By following these steps and utilizing the SLURM job scripts, you should be able to efficiently compile and execute a wide range of C/C++ programs on Cyclone.
</div>

---