import pandas as pd

# Load Excel File
kgdata = pd.ExcelFile('kgdata.xlsx')

# Load DataFrames
foresatt = pd.read_excel(kgdata, 'foresatt', index_col=0)
barn = pd.read_excel(kgdata, 'barn', index_col=0)
barnehage = pd.read_excel(kgdata, 'barnehage', index_col=0)
soknad = pd.read_excel(kgdata, 'soknad', index_col=0)

# Ensure barnehage_id is a column, not an index
if 'barnehage_id' not in barnehage.columns:
    barnehage.reset_index(inplace=True)
    barnehage.rename(columns={"index": "barnehage_id"}, inplace=True)

# Ensure kommune column exists in barnehage
if 'kommune' not in barnehage.columns:
    barnehage['kommune'] = 'Kristiansand'

# Ensure kommune column exists in soknad (if required)
if 'kommune' not in soknad.columns:
    soknad['kommune'] = 'Kristiansand'

# Ensure the necessary columns exist in db.soknad
required_columns = ['y15', 'y16', 'y17', 'y18', 'y19', 'y20', 'y21', 'y22', 'y23']

for col in required_columns:
    if col not in soknad.columns:
        soknad[col] = 0  # Default to 0 if missing

# Debugging: Print the columns of each DataFrame
print("foresatt columns:", foresatt.columns)
print("barn columns:", barn.columns)
print("barnehage columns:", barnehage.columns)
print("soknad columns:", soknad.columns)
