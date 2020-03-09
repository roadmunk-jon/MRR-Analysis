# MRR-Analysis

Setting up Python:

Python is generally pre-installed on Mac OSX. To determine what version you are using, you can type 'python --version' into the terminal.

pip, Python's package manager, is already installed on version 3.4 or later of Python. If it is not installed, you can use 'python get-pip.py' to install it.

It is also highly recommended to use a virtual environment to manage the various packages you may install. To do this, use 'python3 -m venv /path/', replacing '/path/' with the file path to where you'd like the virtual environment directory. You can then run the virtual environment with 'source ./env/bin/activate'.

Setting up git:

git is a system used to save work in progress. First, you must install git. You can do this by running git --version from the terminal or by downloading it from the GitHub website. Following this, you can initialize a git repository in your current directory with 'git init'. Lastly, you can connect your git repo to this repository with 'git remote add origin https://github.com/roadmunk-jon/MRR-Analysis.git'.