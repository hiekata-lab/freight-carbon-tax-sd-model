import pysd
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the .mdl file
mdl_file = os.path.join(BASE_DIR, 'vensim', 'model.mdl')

model = pysd.read_vensim(mdl_file)

generated_py_file = os.path.join(BASE_DIR, 'vensim', 'model.py')
target_py_file = os.path.join(SRC_DIR, 'model.py')

if os.path.exists(generated_py_file):
    shutil.move(generated_py_file, target_py_file)
else:
    raise FileNotFoundError(f"Generated file {generated_py_file} not found")
