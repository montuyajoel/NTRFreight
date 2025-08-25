from utils.packages import install_packages
from utils.arg_parser import get_args

# Install dependencies first
install_packages()

# Get commandline arguments "input and outpuk filenames"
filenames=get_args()

import pandas as pd

ntr_data = pd.read_excel(f'./{filenames.input_file}', header=None, dtype=str)

print(ntr_data)