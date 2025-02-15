Here's a **step-by-step guide** to set up **VS Code, Git, WSL, and GitHub CLI (`gh`)** and push your first commit to GitHub.

---

# 🚀 **Step-by-Step Guide: Setting Up GitHub in VS Code (WSL/Linux/Mac)**
This guide will help you:
✅ Install **VS Code, Git, WSL (for Windows), and GitHub CLI (`gh`)**  
✅ **Create a GitHub account & private repository**  
✅ **Authenticate GitHub in VS Code**  
✅ **Clone, commit, and push your files to GitHub**  
✅ **Add collaborators (MAD-1, MAD-2)**  

---

## **🛠 Step 1: Install Required Software**
### **For Windows Users**
1️⃣ **Install VS Code:**  
   👉 [Download & Install VS Code](https://code.visualstudio.com/download)  

2️⃣ **Install Git:**  
   👉 [Download & Install Git](https://git-scm.com/downloads)  

3️⃣ **Install WSL (Windows Subsystem for Linux)**  
   Open **PowerShell (Admin)** and run:  
   ```sh
   wsl --install
   ```
   Restart your system.

4️⃣ **Install GitHub CLI (`gh`)**  
   Open **WSL Terminal** and run:
   ```sh
   sudo apt update && sudo apt install gh -y
   ```

### **For Mac & Linux Users** (Skip WSL)
- **Git & VS Code** are pre-installed in most Linux/macOS systems.
- Install **GitHub CLI (`gh`)** using:
  ```sh
  brew install gh  # macOS
  sudo apt install gh -y  # Linux
  ```

---

## **🌐 Step 2: Create a GitHub Account & Repository**
1️⃣ Open **[GitHub](https://github.com/)** in your browser.  
2️⃣ **Sign up or log in** to your account.  
3️⃣ Click on **"New Repository"** and:  
   - Repository Name: **Your Roll Number**  
   - Visibility: **Private**  
   - Initialize with: ✅ `README.md`  

---

## **🔗 Step 3: Open VS Code & Clone Your Repo**
1️⃣ Open **VS Code**  
2️⃣ Open **WSL Terminal** (Windows) OR **Terminal** (Mac/Linux)  
   - Shortcut: **Ctrl + `** (tilde key)  
   - OR go to **View → Terminal**  

3️⃣ **Authenticate GitHub CLI in VS Code**
   ```sh
   gh auth login
   ```
   - Choose **GitHub.com**
   - Choose **HTTPS**
   - Copy the **auth link** shown in the terminal.
   - **Paste it into your browser** and log in.
   - **After successful login, return to the terminal.**

4️⃣ **Clone the repository from GitHub**  
   ```sh
   git clone "your_repo_link"
   ```
   - Get this **repo link** from **GitHub → Code → Clone → HTTPS**  
   - Example:
     ```sh
     git clone https://github.com/your-username/your-repo.git
     ```
   - Change directory to the repo:
     ```sh
     cd your-repo
     ```

---

## **📝 Step 4: Add, Commit, and Push Files**
1️⃣ **Create a new file inside your repo folder**  
   Example:
   ```sh
   touch example.txt
   echo "This is my first GitHub file" > example.txt
   ```

2️⃣ **Stage the file (Add to Git)**
   ```sh
   git add example.txt
   ```

3️⃣ **Commit the changes with a message**
   ```sh
   git commit -m "Added example.txt"
   ```

4️⃣ **Check status**
   ```sh
   git status
   ```

5️⃣ **Push changes to GitHub**
   ```sh
   git push origin main
   ```
   *(Replace `main` with your branch if it's different.)*

---

## **🔎 Step 5: Verify Your Changes on GitHub**
1️⃣ **Go to GitHub → Your Repository**  
2️⃣ **Check if your new file (`example.txt`) is uploaded.**  
3️⃣ If the file is there, your push was successful! ✅  

---

## **👥 Step 6: Add Collaborators (MAD-1, MAD-2)**
1️⃣ Open your repository on **GitHub**  
2️⃣ **Go to Settings → Manage Access**  
3️⃣ Click on **Invite Collaborators**  
4️⃣ **Add users:**  
   - **MAD-1**
   - **MAD-2**  
5️⃣ Send **collaboration invites** and wait for them to accept.  

---

## 🎯 **Now You're Ready to Work with GitHub in VS Code + WSL!**
