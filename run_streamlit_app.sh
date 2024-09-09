#!/bin/bash

# Activate Conda
source /home/admin/miniconda3/etc/profile.d/conda.sh

# Activate the 'main' environment
conda activate main

# Navigate to the app directory
cd /home/admin/ai-startups-map/src

# Run the Streamlit app
exec streamlit run app.py 