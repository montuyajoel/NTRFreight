from utils.packages import install_packages
from utils.arg_parser import get_args
from utils.classes import Region

# Install dependencies first
install_packages()

# Get commandline arguments "input and output filenames"
filenames=get_args()

# Import packages
import pandas as pd
import re

#Declare constants
CLIENT = "Intellyse bePro"          
CARRIER = "NTR Freight"  
MATCHING_STRATEGY = "zip_prefix_match"           
SERVICE_TYPES = {
    "Switzerland Export/Import — Express Worldwide",
    "Domestic Express Third Country",
    "Switzerland Export — Economy Select",
}

#------------------------------ 
# Data Extraction per sheet
#------------------------------
def load_sheets(file_path: str) -> dict[str, pd.DataFrame]:
    ntr_raw = pd.ExcelFile(file_path)
    sheets={}
    # Loop blocks to get country and 
    for name in ntr_raw.sheet_names:
        df = pd.read_excel(file_path, sheet_name=name, header=None, dtype=str, engine="openpyxl")
        sheets[name] = df
    return sheets

# Get Countries, Zone Number and Country Code
def get_countries(sheet_name):
    # Load Data
    df=load_sheets(f'./{filenames.input_file}')[sheet_name][3::] # removes top 3 rows
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

    # Drop rows with null values
    df = df.dropna(subset=['Code'])

    # Sort Values by Country
    df = df.sort_values(by=["Country"]).reset_index(drop=True)
    df.insert(0, "RegionID", range(1, len(df) + 1))

    return df

# Export data to xlsx file
def write_output(path_out: str, regions_df: pd.DataFrame, tariffs_df: pd.DataFrame, surcharges_df: pd.DataFrame) -> None:
    # Use openpyxl engine to export file
    with pd.ExcelWriter(path_out, engine="openpyxl") as w:
        # Create different sheets as required
        regions_df.to_excel(w, sheet_name="Regions", index=False)
        tariffs_df.to_excel(w, sheet_name="Tariffs", index=False)
        surcharges_df.to_excel(w, sheet_name="Surcharges", index=False)

# Format Dataframe to specified output format
def generate_regions(countries):
    # Create new objects with the require format
    region_objects = [
        Region(
            id=row.RegionID,
            matching_strategy=MATCHING_STRATEGY,
            client=CLIENT,
            carrier=CARRIER,
            country=row.Code
        )
        # Loop through all records
        for row in countries.itertuples(index=False)
    ]

    # Convert dataclass objects back into DataFrame
    regions_class_df = pd.DataFrame([r.__dict__ for r in region_objects])
    return regions_class_df

regions_df = generate_regions(get_countries('ZH Zones TDI Exp+Imp'))
write_output(filenames.output_file, regions_df, regions_df, regions_df)