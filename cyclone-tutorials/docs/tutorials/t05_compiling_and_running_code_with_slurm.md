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

# Compiling C/C++ Source Code on HPC Systems

Compiling efficient C/C++ code on High-Performance Computing (HPC) systems is crucial for leveraging the available computational resources. This tutorial will guide you through the process, covering compiler options, optimization flags, and performance testing.

---

## 1. **Common Compilers on HPC Systems**

Different HPC systems support a variety of compilers tailored to specific hardware architectures:

- **GCC (GNU Compiler Collection)**: Open-source, widely used, supports many architectures.
- **Intel C/C++ Compiler (icc)**: Optimized for Intel processors, often provides better performance on Intel hardware.
- **NVCC (NVIDIA Compiler)**: For compiling CUDA programs targeting NVIDIA GPUs.
- **Clang/LLVM**: A modern compiler offering competitive performance and tools.
- **Cray Compiler**: Designed for Cray systems, with excellent support for vectorization and optimization.

---

## 2. **Using the `module` Command**

Most HPC systems manage software environments using the `module` command. Modules allow you to load specific versions of compilers and other software. To view available compilers, use:

```bash
module avail
```

To load a specific compiler module:

```bash
module load <compiler_name>/<version>
```

For example, to load GCC version 12.1:

```bash
module load gcc/12.1
```

To see which modules are currently loaded:

```bash
module list
```

---

## 3. **Optimization Flags**

Compilers offer optimization flags to improve performance. Commonly used flags include:

### General Optimization Levels:
- **`-O0`**: No optimization (default).
- **`-O1`**: Basic optimizations.
- **`-O2`**: Moderate optimizations without impacting debugging.
- **`-O3`**: Aggressive optimizations, often enabling vectorization and loop unrolling.

### Advanced Flags:
- **`-ffast-math`**: Enables faster floating-point calculations (may reduce precision).
- **`-funroll-loops`**: Unrolls loops to reduce overhead.
- **`-march=native`**: Optimizes code for the architecture of the system being used.
- **`-flto`**: Enables link-time optimization.
- **`-fopenmp`**: Enables OpenMP for parallel programming.

Each compiler has its specific flags. Refer to its documentation for more options.

---

## 4. **Example Code**

Here's an example C++ code that performs matrix multiplication:

```cpp
#include <iostream>
#include <vector>
#include <chrono>

void matrixMultiply(const std::vector<std::vector<double>>& A,
                    const std::vector<std::vector<double>>& B,
                    std::vector<std::vector<double>>& C, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    const int N = 512;
    std::vector<std::vector<double>> A(N, std::vector<double>(N, 1.0));
    std::vector<std::vector<double>> B(N, std::vector<double>(N, 2.0));
    std::vector<std::vector<double>> C(N, std::vector<double>(N, 0.0));

    auto start = std::chrono::high_resolution_clock::now();
    matrixMultiply(A, B, C, N);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << "Executable: " << argv[0] << std::endl;
    std::cout << "Matrix multiplication completed in " << elapsed.count() << " seconds." << std::endl;
    return 0;
}
```

---

## 5. **Compiling and Testing**

### Compile Without Optimization:
```bash
g++ -O0 matrix_multiply.cpp -o matrix_multiply
```
Run it and note the runtime.

### Compile with Optimization:
```bash
g++ -O3 -march=native -funroll-loops matrix_multiply.cpp -o matrix_multiply_optimized
```
Run it and compare the runtime with the non-optimized version.

### Additional Testing with Intel Compiler:
If available, try compiling with Intel's compiler:
```bash
module load intel
icc -O3 -xHost -ipo matrix_multiply.cpp -o matrix_multiply_intel
```

---

## 6. **Performance Testing**

### Tools for Performance Testing:
- **`time` command**: Measures execution time.
  ```bash
  time ./matrix_multiply
  time ./matrix_multiply_optimized
  time ./matrix_multiply_intel
  ```
- **Profiler tools**:
  - **`gprof`** (GCC): Use `-pg` during compilation for profiling.
  - **Intel VTune Profiler**: Optimizes performance on Intel hardware.
  - **`nvprof`** (NVIDIA): For profiling GPU-based applications.

---

## 7. **Conclusion**

Efficient compilation and optimization are crucial for HPC workloads. Understanding the available compilers, their flags, and how to test performance enables you to maximize the potential of your code on an HPC system.
