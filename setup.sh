#!/bin/bash

# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda

# Initialize conda
eval "$($HOME/miniconda/bin/conda shell.bash hook)"
conda init

# Create and activate conda environment
conda create --name airquality python=3.8 -y
conda activate airquality

# Install required packages
conda install -c conda-forge prophet pandas altair streamlit numpy -y

# Print installed packages for verification
conda list
