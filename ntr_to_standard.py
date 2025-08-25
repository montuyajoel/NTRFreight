from utils.packages import install_packages
from utils.arg_parser import get_args

# Install dependencies first
install_packages()

# Get commandline arguments "input and output filenames"
filenames=get_args()

# Import packages
import pandas as pd
import re

#------------------------------ 
# Data Extraction per sheet
#------------------------------
def load_sheets(file_path: str) -> dict[str, pd.DataFrame]:
    ntr_raw = pd.ExcelFile(file_path)
    sheets={}

    for name in ntr_raw.sheet_names:
        df = pd.read_excel(file_path, sheet_name=name, header=None, dtype=str, engine="openpyxl")
        sheets[name] = df
    return sheets

# Get Countries, Zone Number and Country Code
def get_countries(sheet_name):
    # Load Data
    df=load_sheets(f'./{filenames.input_file}')[sheet_name][3::] # removes 3 rows
    countries=[]

    # Loop through each block
    for i in range(0, df.shape[1], 3):
        block = df.iloc[:, i:i+2]
        block = block.dropna().values.tolist()
        countries.extend(block)
    
    # Convert to DataFrame
    df = pd.DataFrame(countries[1:], columns=countries[0])  # drop header row

    # Extract country code inside parentheses using regex
    df["Code"] = df["Country"].str.extract(r"\((.*?)\)")

    # Remove code from country names
    df["Country"] = df["Country"].str.replace(r"\s*\(.*?\)", "", regex=True)
    
    df = df.sort_values(by=["Country"]).reset_index(drop=True)
    df.insert(0, "RegionID", range(1, len(df) + 1))
   
    print(df)

get_countries('ZH Zones TDI Exp+Imp')