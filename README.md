# Complete Project Setup Guide

This guide covers two scenarios: setting up a new project from scratch and working with an existing project from GitHub.

## Option A: Clone Existing Project

If you're working with the Document Portal project:

```bash
# Clone the repository
git clone https://github.com/rohitsmagdum13/Document_Portal.git

# Navigate to the project directory
cd Document_Portal
```

## Option B: Create New Project

If you're starting a new project:

```bash
# Create project directory
mkdir <project_folder_name>
cd <project_folder_name>
```

## 2. Set Up Conda Virtual Environment

```bash
# Create virtual environment with Python 3.10
conda create -p venv python=3.10 -y

# Activate the environment
conda activate venv/
```

**Note:** When using `-p venv`, activate with `conda activate venv/` (with trailing slash)

## 3. Install Dependencies

```bash
# Install from requirements.txt (make sure this file exists in your project root)
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, create one with your dependencies:
```bash
pip freeze > requirements.txt
```

## 4. Git Setup (for new projects only)

If you created a new project (Option B), initialize Git:

```bash
# Initialize Git repository
git init

# Add all files to staging
git add .

# Make initial commit
git commit -m "Initial project setup"

# Add remote origin (replace with your repository URL)
git remote add origin <your_repository_url>

# Push to remote repository
git push -u origin main
```

## 5. Verify Setup

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Git status
git status
```

## Additional Notes

- Replace `<project_folder_name>` with your actual project name
- Replace `<your_repository_url>` with your GitHub repository URL
- For the Document Portal project, the repository is already set up, so skip the Git initialization steps
- Always ensure your virtual environment is activated before installing packages or running the project

## Deactivating Environment

When you're done working:
```bash
conda deactivate
```