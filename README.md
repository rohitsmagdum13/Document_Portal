# Project Setup Guide

Follow these steps to set up your project environment and initialize version control.

## 1. Create and Enter Project Directory

```bash
mkdir <project_folder_name>
cd <project_folder_name>
```

## 2. Set Up Conda Virtual Environment

```bash
conda create -p venv python=3.10 -y
conda activate venv
```

## 3. Install Dependencies

Make sure you have a `requirements.txt` file in your project directory.

```bash
pip install -r requirements.txt
```

## 4. Initialize Git Repository

```bash
git init
git add .
git commit -m "your_commit_message"
git push
```

---

Replace `<project_folder_name>` with your desired project name and `"your_commit_message"` with an appropriate commit message.