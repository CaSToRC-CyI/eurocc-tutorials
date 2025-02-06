<!--
 t01_introduction_to_hpc_systems.md

 CaSToRC, The Cyprus Institute

 (c) 2024 The Cyprus Institute

 Contributing Authors:
 Christodoulos Stylianou (c.stylianou@cyi.ac.cy)
 Kyriaki Kylili (k.kylili@cyi.ac.cy)
 Spyroulla Mavrommati (s.mavrommati@cyi.ac.cy)
 
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

# SSH Manager Installation Guide for Windows
## 1. OpenSSH
### 1.1 Check if OpenSSH Client is installed:
1. Open a Windows PowerShell as Administrator.
   - **Press Windows Key > Search "Windows PowerShell" > Right-click "Run as Administrator"**
2. Run the following command to see if the OpenSSH client is installed:
    ```powershell
    Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Client*'
    ```
    If installed, you should see something like:
    ```powershell
    Name: OpenSSH.Client~~~~0.0.1.0
    State: Installed
    ```

### 1.2 Install OpenSSH Client (If not already Installed!)
1. Open Settings
2. Search for OpenSSH Client:
   - Click on **Add a feature** and search for "OpenSSH Client"
   - Select it and click **Install**.

### 1.3 Activate OpenSSH (Start Services)
1. Open a Windows PowerShell as Administrator.
   - **Press Windows Key > Search "Windows PowerShell" > Right-click "Run as Administrator"**
2. Start the SSH Agent:
   ```powershell
    Start-Service ssh-agent
   ```

---

## 2. WSL
1. Open a Windows PowerShell as Administrator.
   - **Press Windows Key > Search "Windows PowerShell" > Right-click "Run as Administrator"**
2. For Windows 10 (build 19041 and higher) and Windows 11, you can use the simplified command to install WSL:
    ```powershell
    wsl --install
    ```

    This will:
    - Enable the WSL feature.
    - Install the default Linux distribution (usually Ubuntu).
    - Install the necessary Virtual Machine Platform and Windows Subsystem for Linux components.
3. Restart Your Computer:
If prompted, restart your computer to complete the installation.

---

## 3. Git Bash
1. Install Git Bash:
   - Install Git for Windows if you haven’t already [Download Git](https://git-scm.com/downloads).
2. Launch Git Bash
   - **Press Windows Key > Search "Git Bash"**

---