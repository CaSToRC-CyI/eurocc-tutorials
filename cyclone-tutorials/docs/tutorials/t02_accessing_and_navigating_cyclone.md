<!--
 t02_accessing_and_navigating_cyclone.md

 CaSToRC, The Cyprus Institute

 (c) 2024 The Cyprus Institute

 Contributing Authors:
 Giorgos Kosta (g.kosta@cyi.ac.cy)
 Emmanouil Kritikos (e.kritikos@cyi.ac.cy)
 Leonidas Christodoulou (l.christodoulou@cyi.ac.cy)
 
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

# 2. Accessing and Navigating Cyclone

## 2.1. Overview

<div style="text-align: justify;">This tutorial focuses on providing participants with the practical skills needed to access and navigate the Cyclone HPC system. It covers secure system access across different platforms, transferring files to and from Cyclone, and managing data within its file systems. Participants will also learn fundamental Linux commands to navigate directories and organize data effectively. By the end of this tutorial, users will have connected to Cyclone, transferred files, and explored the directory structure using basic Linux commands.</div>

---

## 2.2. Learning Objectives

<div style="text-align: justify;">
By the end of this tutorial, participants will be able to:
<ol>
<li>Securely access Cyclone using SSH, with tailored solutions for different operating systems (Linux, macOS, Windows).</li>
<li>Transfer data to and from Cyclone using tools like scp, rsync, and FileZilla.</li>
<li>Navigate Cyclone’s directory structure and manage files effectively using basic Linux commands.</li>
<li>Understand best practices for data organization and storage across Cyclone’s file systems, including strategies for long-term data management.</li>
</ol>
</div>

---

## 2.3. Prerequisites
<div style="text-align: justify;">
<ul>
<li>A Cyclone account (contact your system administrator if you don't have one)</li>
<li>A computer with internet connection</li>
<li>Administrator rights or permission to install software (for some setup options)</li>
</div>

---

## 2.4. Getting Started

### 2.4.1. What is SSH and Why is it Important?

<div style="text-align: justify;">SSH, or Secure Shell, is a secure way to access and manage remote systems, such as High-Performance Computing (HPC) resources, over a network. It encrypts all communication, protecting sensitive information from being intercepted by unauthorized users. SSH is essential because it provides a safe and efficient way to connect to powerful remote systems for tasks like running simulations, managing files, and analyzing data. Instead of using vulnerable passwords, SSH often uses a system called public-key cryptography to verify your identity.
<br><br>
Here’s how it works: SSH relies on a pair of keys—a public key and a private key. The public key is shared with the remote system (the server), acting like a lock, while the private key stays safely on your computer, working as the unique key that can open that lock. When you try to connect, the server sends a challenge that only your private key can solve. If it’s solved correctly, the server knows it’s you, and the connection is established securely. This approach ensures that even if someone intercepts the communication, they can’t access your data or impersonate you. SSH combines simplicity and robust security, making it an indispensable tool for accessing and using HPC systems effectively.</div>

### 2.4.2. For MacOS and Linux Users

<div style="text-align: justify;">
Open the Terminal application
<ul>
<li>On MacOS: Use Spotlight (Command + Space) and type "Terminal"</li>
<li>On Linux: Use your system's application launcher and search for "Terminal"</li>
<li>Keep this Terminal window open throughout the setup process</li>
</ul>
</div>

### 2.4.3. For Windows Users

<div style="text-align: justify;">
Choose your terminal:
<ul>
<li>If using PowerShell: Search for "PowerShell" in the Start menu and run as Administrator</li>
<li>If using Git Bash (recommended): Launch Git Bash from the Start menu</li>
</ul>
</div>

---

## 2.5. Setting Up SSH and your keys

> ⚠️ Remember to replace `username` with your actual Cyclone username in all examples.

### 2.5.1. MacOS and Linux

<div style="text-align: justify;">Using SSH keys is more secure and convenient than password authentication. Here's how to set them up:</div>

#### Managing SSH Keys

<div style="text-align: justify;">Start the SSH agent:</div>

```bash
eval "$(ssh-agent -s)"
```

<div style="text-align: justify;">
Add your SSH key to the agent:

<blockquote>
If you used another filename or directory to store your ssh key you generated, make sure to change it
</blockquote>
</div>

```bash
ssh-add ~/.ssh/id_rsa
```

#### SSH Config File Setup

<div style="text-align: justify;">Navigate to your SSH directory:</div>

```bash
cd ~/.ssh/
```

<div style="text-align: justify;">To simplify connections create or edit <code>~/.ssh/config</code> with nano:</div>

```bash
nano config
```

<div style="text-align: justify;">In the nano editor, add these lines:</div>

```bash
Host cyclone
    HostName cyclone.hpcf.cyi.ac.cy
    User your_username
    IdentityFile ~/.ssh/id_rsa
```

<div style="text-align: justify;">If you're using macOS, add this to your <code>~/.ssh/config</code> file to make the key persistent:</div>

```bash
Host *
  UseKeychain yes
  AddKeysToAgent yes
  IdentityFile ~/.ssh/id_rsa
```

<div style="text-align: justify;">
To save the file:

<ul>
<li>Press Ctrl + X</li>
<li>Press Y to confirm</li>
<li>Press Enter to save</li>
</ul>

Once you save the file, return to your Terminal window to test the connection:
</div>

```bash
ssh cyclone
```

### 2.5.2. Windows

#### Option 1: Using PowerShell

##### 1. Start the SSH Agent

<div style="text-align: justify;">Open PowerShell as Administrator. Then check if the SSH agent service is running:</div>

```bash
Get-Service ssh-agent
```

<div style="text-align: justify;">If the service is stopped, enable and start it:</div>

```bash
# Set the service to manual startup
Set-Service ssh-agent -StartupType Manual

# Start the service
Start-Service ssh-agent
```

##### 2. Add Your SSH Key

<div style="text-align: justify;">Add your private key to the SSH agent:</div>

```powershell
ssh-add $env:USERPROFILE\.ssh\id_rsa
```

<div style="text-align: justify;">To verify if the key was added:</div>

```powershell
ssh-add -l
```

##### 3. Connect to Cyclone

```powershell
ssh username@cyclone.hpcf.cyi.ac.cy
```

<div style="text-align: justify;">Replace <code>username</code> with your Cyclone username.</div>
<br>

#### Option 2: Using Git Bash (Recommended)

<div style="text-align: justify;">
<blockquote>
Using git bash <b>doesn't require administrator permissions</b>. Therefore this option will work even if Administrator restrictions apply on your computer.
</blockquote>
</div>

##### 1. Start Git Bash

<div style="text-align: justify;">
<ul>
<li>Download Git Bash from <a href="https://git-scm.com/downloads"> https://git-scm.com/downloads</a></li>
<li>Install Git Bash accepting the default options</li>
<li>Open Git Bash from your start menu</li>
</ul>
</div>

##### 2. Add Your SSH Key

```bash
ssh-add ~/.ssh/id_rsa
```

##### 3. Create SSH Config (Optional but Recommended)

<div style="text-align: justify;">Create or edit <code>~/.ssh/config</code>:</div>

```bash
nano ~/.ssh/config
```

<div style="text-align: justify;">Add these lines:</div>

```bash
Host cyclone
    HostName cyclone.hpcf.cyi.ac.cy
    User your_username
    IdentityFile ~/.ssh/id_rsa
```
<div style="text-align: justify;">
<blockquote>
Replace <code>your_username</code> with your Cyclone username.
</blockquote>

Save and close the file (Ctrl+X, then Y, then Enter)
</div>
<br>

##### 4. Connect to Cyclone

<div style="text-align: justify;">If using SSH config:</div>

```bash
ssh cyclone
```

<div style="text-align: justify;">Without SSH config:</div>

```bash
ssh username@cyclone.hpcf.cyi.ac.cy
```

<div style="text-align: justify;">When you successfully ssh/login, you'll be greeted with this message:</div>

![successfull login](../images/t02/ssh.png)

<div style="text-align: justify;">
<blockquote>
If you are having trouble ssh/logging, refer to the troubleshooting steps at the end or try again the process from the beginning. 
</blockquote>
</div>

---

## 2.6. Managing Data and Directories on Cyclone

### 2.6.1. Home Directory Structure

<div style="text-align: justify;">When you log in, your home directory (<code>/nvme/h/<username></code>) typically contains:</div>

```bash
# Project data links
data_p166/  -> /onyx/data/p166    # Shared project storage
data_p184/  -> /onyx/data/p184    # Another project
data_p213/  -> /onyx/data/p213    # And so on...

# Scratch space link
scratch/    -> /nvme/scratch/<username>  # Personal scratch space

# Scratch space link for event
edu26/    -> /nvme/scratch/edu26  # Shared scratch space for events
```

<div style="text-align: justify;">
<blockquote>
While these project directories (like <code>data_p166/</code>) will appear to be in your home directory, they are actually symbolic links (shortcuts) pointing to their real location on the <code>/onyx/data/</code> storage system. This is why you'll see them listed when you run <code>ls</code> in your home directory, even though they're physically stored elsewhere.
</blockquote>
</div>

<span style="text-align: justify;">For more information on Cyclones FileSystem please look at </span> [Tutorial 01](t01_introduction_to_hpc_systems.md#142-file-system-overview).


<div style="text-align: justify;">To see the contents of your own directory you can use the <code>ls</code> command when you login:</div>

```bash
ls -a   # prints all files/directories, including hidden ones

ls -l   # prints visible directories in a list including important information like ownership, permissions, last date of modification

ls -la  # you can combine flags, this creates a list with all files/directories
```

<div style="text-align: justify;">To see your current working directory:</div>

```bash
pwd
```

### 2.6.2. Directory Organization Best Practices

#### Project Data Organization

```bash
# In your project directory (e.g., ~/data_p166/)
data_p166/
├── datasets/           # Shared input data
├── results/           # Project results
│   ├── experiment1/
│   └── experiment2/
└── shared_scripts/    # Project-specific scripts

# In your scratch space
scratch/
├── job_outputs/      # Temporary job results
├── temp_data/       # Temporary processing
└── checkpoints/     # Job checkpoints
```

#### Personal Organization

```bash
# In your home directory
scripts/              # Personal script collection
├── job_templates/    # Slurm job templates
├── analysis/         # Analysis scripts
└── utils/           # Utility scripts

```

<div style="text-align: justify;">
<blockquote>
These directories aren't created by default, except the scratch and project specific parent directories
</blockquote>
</div>

### 2.6.3. Data Management Best Practices

#### Setting up a New Project Space

<div style="text-align: justify;">Using the <code>cd</code> command to change directories:</div>

```bash
# Navigate to your project directory
cd ~/data_p166
```

<div style="text-align: justify;">
<blockquote>
The <code>~/</code> we use in our commands points to the home directory  
</blockquote>
</div>

<div style="text-align: justify;">Using the <code>mkdir</code> command to make a directory.</div>

```bash
# Create standard project structure
mkdir -p datasets           # For input data
mkdir -p results            # For processed results
mkdir -p shared_scripts     # For project-specific scripts
mkdir -p documentation      # For project documentation
```

<div style="text-align: justify;">
<blockquote>
The <code>-p</code> makes sure that any parent directories that don't already exist are created.
</blockquote>
</div>

#### Working with Project Data

```bash
# Create a workspace in scratch for processing
mkdir -p ~/scratch/myanalysis
cd ~/scratch/myanalysis

# Copy input data to scratch for processing
cp ~/data_p166/datasets/input.dat ./

# After processing is complete, save important results
cp -r ./results ~/data_p166/results/analysis_20240319

# Clean up scratch space
cd ~
rm -rf ~/scratch/myanalysis
```

#### Space Management

<div style="text-align: justify;">
Using the <code>du</code> command you can view storage usage.

<br><br>
To monitor storage:
</div>

```bash
# Check project space usage
du -h /onyx/data/p166
```

<div style="text-align: justify;">
<blockquote>
The <code>-h</code> flag makes the sizes 'human readable' meaning it's converting them from bytes to MB/GB/TB
</blockquote>
</div>

```bash
# Check scratch usage
du -hs ~/scratch
```

<div style="text-align: justify;">
<blockquote>
The <code>-s</code> flag summarizes the storage usage of the hole directory. So if you want file by file usage, remove <code>s</code>.
</blockquote>
</div>

#### Data Safety

<div style="text-align: justify;">
<ul>
<li>Keep important data in project directories</li>
<li>Use scratch for temporary processing only</li>
<li>Regularly clean scratch space</li>
<li>Document data organization for team members</li>
</ul>
</div>

---

## 2.7. Best Practices Summary

1. **Project Organization**:

    - Keep project data organized in project directories
    - Use consistent structure across projects

2. **Data Management**:

    - Store shared data in project directories
    - Use scratch for temporary processing
    - Clean up scratch regularly
    - Document organization for team members

3. **Job Workflow**:

    - Read input from project directories
    - Process in scratch space
    - Save results back to project directories
    - Clean up scratch after job completion

4. **Collaboration**:

    - Use project directories for sharing
    - Maintain consistent directory structure
    - Document data organization
    - Communicate changes with team members

Remember that your project memberships determine both your compute resource allocation (via Slurm) and your access to shared storage spaces. Always specify the correct project ID in your Slurm jobs and organize your data accordingly.

---

## 2.8. Transferring Files

### 2.8.1. Before starting

1. Open a terminal on your local machine (not on Cyclone)
2. Make sure you know:
    - The full path of the file/directory on your local machine
    - Where you want it to go on Cyclone (or vice versa)

3. All commands below should be run from your local machine's terminal

### 2.8.2. Using SCP (Secure Copy):

#### Transferring FROM your local machine TO Cyclone:

```bash
# Run this command on your local machine's terminal
scp /path/on/your/local/machine/localfile.txt cyclone:~/destination/on/cyclone/
```

#### Transferring FROM Cyclone TO your local machine:

```bash
# Run this command on your local machine's terminal
scp cyclone:~/path/on/cyclone/remotefile.txt /path/on/your/local/machine/
```

> If you have not created an ssh config file, replace `cyclone` with `username@cyclone.hpcf.cyi.ac.cy`

This is what it should look like:

![scp screenshot](../images/t02/scp.png)

### 2.8.3. Using Rsync (Recommended for Large Transfers)
#### Copying FROM your local machine TO Cyclone:

```bash
# Run this on your local machine's terminal
# The ./ refers to the current directory on your local machine
rsync -avz ./local_directory/ cyclone:~/remote_directory/
```

![rsync screenshot pc to cyclone](../images/t02/rsync-pc2cyc.png)

#### Copying FROM Cyclone TO your local machine:

```bash 
# Run this on your local machine's terminal
rsync -avz cyclone:~/remote_directory/ ./local_directory/
```

> 💡 Note: All file transfer commands should be run from your local machine's terminal, not from within Cyclone. The paths before the colon (\:) refer to your local machine, while paths after the colon refer to locations on Cyclone.

### 2.8.4. Using FileZilla (Graphical Interface)

Download and install FileZilla. Then, go to `Edit → Settings`

![filezilla-toolbar](../images/t02/filezilla-toolbar.png)

Go to `SFTP`

![filezilla-settings-page](../images/t02/filezilla-settings-page.png)

Add your key

![filezilla-add-key](../images/t02/filezilla-add-key.png)

If your key is in OpenSSH format, you'll be prompted to convert your key. Press yes:

![filezilla-convertkey](../images/t02/filezilla-convertkey.png)

Then input your passphrase:

![filezilla-input-passphrase](../images/t02/filezilla-input-passphrase.png)

And then save the converted key. It's a good idea to keep it at the same place as the original in case you go looking for it in the future.

1. Set up connection:
   <ul>
   <li>Host: <code>sftp://cyclone.hpcf.cyi.ac.cy</code></li>
   <li>Username: <code>your_username</code></li>
   <li>Port: <code>22</code></li>
   </ul>
2. Quick connect

![filezilla](../images/t02/filezilla.png)

Once you're connected you'll see your local directory on the left and cyclone on the right. You can now just **drag and drop** between the two and the transfer wil happen automatically!

---

## 2.9. Security Best Practices

1. Use different keys for different services
2. Regularly rotate keys (yearly)
3. Always use strong passphrases
4. Back up your private keys securely
5. Never share private keys

---

## **2.10. Notes and Troubleshooting**

### **2.10.1 Installing Required Tools**
<span style="text-align: justify;">If you don’t have OpenSSH, WSL, or Git Bash installed, refer to the </span> [Installation Guide]("../utils/Windows_SSH_Setup.md").

### **2.10.2. `~/.ssh` directory does not exist on Windows**

#### **Option 1: Using Powershell**
1. Open PowerShell.
   <ul>
   <li><b>Press Windows Key > Search "Windows PowerShell" > Enter</b></li>
   </ul>
  
1. Navigate to your Home directory
   
    ```
        cd ~
    ```

    This will take you to your home directory, typically something like `C:\Users\<YourUsername>`.

2. Create the `.ssh` directory:
   
    ```
    mkdir .ssh
    ```

3. Verify that the directory was created:
   
    ```
    ls .ssh
    ```
   
    If the `.ssh` folder exists, the command will list its contents (it may be empty if just created).

#### **Option 2: Using File Explorer**
1. Open File Explorer.
2. Navigate to your home directory: `C:\Users\<YourUsername>`.
3. Create a new folder named `.ssh`:
    - Right-click and choose **New > Folder**.
    - Name it `.ssh` (include the period).
    - Confirm if prompted about using a name that starts with a period.

### **2.10.3 Changing and Removing File Extensions (Windows)**
File extensions (like `.txt`, `.png`, `.exe`) are often hidden by default in Windows, so you'll first need to make extensions visible before removing or changing them.

1. Open **File Explorer**.
   - Press **Win + E** or click the folder icon in the taskbar.
2. Access View Options:
    - **Windows 10**: Click on the View tab in the toolbar at the top.
    - **Windows 11**: Click on the three dots (`...`) in the toolbar at the top and choose **Options**.
3. Click on the tab **View**, go to *"Advanced settings"* and uncheck the checkbox *"Hide extensions for known file types"* if already checked.
4. (Now that the extension is visible) Rename the file:
   - Right-click the file and choose **Rename**.
   - Remove or modify the extension as needed.
   - Confirm the change when prompted.

### **2.10.4. Show/Unhide `.ssh` directory (Windows)**
File extensions (like `.txt`, `.png`, `.exe`) are often hidden by default in Windows, so you'll first need to make extensions visible before removing or changing them.
1. Open **File Explorer**.
   - Press **Win + E** or click the folder icon in the taskbar.
2. Access View Options:
    - **Windows 10**: Click on the View tab in the toolbar at the top.
    - **Windows 11**: Click on the three dots (`...`) in the toolbar at the top and choose **Options**.
3. Click on the tab **View**, go to *"Advanced settings"*.
4. Scroll down to *"Hidden files and folders"* and select the option **Show hidden files, folders, and drives**.

### 2.10.5. SSH agent issues (MacOS/Linux/Git Bash)

To set Up SSH Agent Automatically, first open or create the `~/.bashrc` file:

```bash
nano ~/.bashrc
```

Add these lines to the file:

``` bash
# Start SSH agent if not running
if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval `ssh-agent -s` > /dev/null
fi
``` 

Save, close the file (Ctrl+X, then Y, then Enter) and then reload the configuration:

```bash
source ~/.bashrc
```

### 2.10.6. Connection issues (MacOS/Linux/Git Bash)

First, check the SSH agent:

```bash
ssh-add -l #This will list all of your added keys
```

Then verify the relevant files and directories have the correct permissions:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

> This makes sure your private/public key and the directory they are in have the correct read write and execute permissions for the ssh client to allow a connection.

Finally, test connection with verbose output:

```bash
ssh -v cyclone # Adding the `-v` flag prints debuging information 
```

### 2.10.7 SSH Permission Issues (Powershell)

If your key doesn't have the correct permissions:

```powershell
icacls <path-to-your-id_rsa> /inheritance:r /grant:r "$($env:USERNAME):(F)"
```

> ⚠️ Remember to replace `username` with your actual Cyclone username in all examples.

---
