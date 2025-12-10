#!/bin/bash
# 'source setup.sh' in root
set -e
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
python src/translate_model.py
python -m ipykernel install --user --name=sd-model --display-name="Python (sd-model)"
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/*.ipynb
