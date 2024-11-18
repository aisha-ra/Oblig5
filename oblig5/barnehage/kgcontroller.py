# kgcontroller.py
import pandas as pd
import numpy as np
from dbexcel import forelder, barn, barnehage, soknad
from kgmodel import Foresatt, Barn, Barnehage, Soknad

def form_to_object_soknad(form_data):
    soknad = Soknad(
        foresatt_navn=form_data.get('foresatt_navn'),
        foresatt_adresse=form_data.get('foresatt_adresse'),
        foresatt_tlfnr=form_data.get('foresatt_tlfnr'),
        foresatt_pnr=form_data.get('foresatt_pnr'),
        foresatt_2_navn=form_data.get('foresatt_2_navn'),
        foresatt_2_adresse=form_data.get('foresatt_2_adresse'),
        foresatt_2_tlfnr=form_data.get('foresatt_2_tlfnr'),
        foresatt_2_pnr=form_data.get('foresatt_2_pnr'),
        barn_pnr=form_data.get('barn_pnr'),
        barn_2_pnr=form_data.get('barn_2_pnr'),
        fr_barnevern=form_data.get('fr_barnevern') == 'on',
        fr_sykd_familie=form_data.get('fr_sykd_familie') == 'on',
        fr_sykd_barn=form_data.get('fr_sykd_barn') == 'on',
        fr_annet=form_data.get('fr_annet'),
        liste_over_barnehager_prioritert_5=form_data.get('liste_over_barnehager_prioritert_5'),
        tidspunkt_oppstart=form_data.get('tidspunkt_oppstart'),
        sosken_i_barnehagen=form_data.get('sosken_i_barnehagen') == 'on',
        brutto_inntekt=int(form_data.get('brutto_inntekt', 0))
    )
    return soknad

# Insert functions
def insert_foresatt(f):
    global forelder
    new_id = forelder['foresatt_id'].max() + 1 if not forelder.empty else 1
    if not forelder[forelder['foresatt_pnr'] == f.foresatt_pnr].empty:
        return  # Avoid duplicate entries by personnummer
    forelder = pd.concat([forelder, pd.DataFrame([[new_id, f.foresatt_navn, f.foresatt_adresse, f.foresatt_tlfnr, f.foresatt_pnr]], columns=forelder.columns)], ignore_index=True)
    return forelder

def insert_barn(b):
    global barn
    new_id = barn['barn_id'].max() + 1 if not barn.empty else 1
    if not barn[barn['barn_pnr'] == b.barn_pnr].empty:
        return  # Avoid duplicate entries by personnummer
    barn = pd.concat([barn, pd.DataFrame([[new_id, b.barn_pnr]], columns=barn.columns)], ignore_index=True)
    return barn

def insert_soknad(s):
    global soknad

    # Check if the 'id' column exists, if not, add it
    if 'id' not in soknad.columns:  # Check for 'id' column
        soknad['id'] = pd.Series(dtype='int')  # Initialize empty 'id' column

    # Create a new ID for the application
    new_id = soknad['id'].max() + 1 if not soknad.empty else 1

    # Check the columns of the DataFrame before inserting
    print(soknad.columns)  # Debugging: Print out the columns

    # Add the new application to the dataframe, ensuring the data matches the number of columns
    soknad = pd.concat([
        soknad,
        pd.DataFrame([[
            new_id,
            s.foresatt_pnr,
            s.foresatt_2_pnr if s.foresatt_2_pnr else None,
            s.barn_pnr,
            s.fr_barnevern,
            s.fr_sykd_familie,
            s.fr_sykd_barn,
            s.fr_annet,
            s.liste_over_barnehager_prioritert_5,
            s.sosken_i_barnehagen,
            s.tidspunkt_oppstart,
            s.brutto_inntekt,
            None  # Ensure all columns are populated; this is for any missing column
        ]], columns=soknad.columns)
    ], ignore_index=True)

# Select functions
def select_alle_barnehager():
    return barnehage.apply(lambda r: Barnehage(r['barnehage_id'], r['barnehage_navn'], r['barnehage_antall_plasser'], r['barnehage_ledige_plasser']), axis=1).to_list()

def select_barnehage_instans(barnehage_id):
    series = barnehage[barnehage['barnehage_id'] == barnehage_id]
    if series.empty:
        return np.nan
    return Barnehage(barnehage_id, series.iloc[0]['barnehage_navn'], series.iloc[0]['barnehage_antall_plasser'], series.iloc[0]['barnehage_ledige_plasser'])

def select_alle_soknader():
    all_soknader = []
    try:
        # Iterate over each row in the soknad DataFrame
        for _, row in soknad.iterrows():
            print("Processing soknad ID:", row['id'])  # Debug print

            # Retrieve guardian (foresatt) 1 data
            foresatt_1 = forelder[forelder['foresatt_id'] == row['foresatt_1']]
            if foresatt_1.empty:
                print("Warning: foresatt_1 not found for soknad ID:", row['id'])
                continue  # Skip this row if no matching foresatt_1 is found
            foresatt_1_obj = Foresatt(
                foresatt_id=foresatt_1.iloc[0]['foresatt_id'],
                foresatt_navn=foresatt_1.iloc[0]['foresatt_navn'],
                foresatt_adresse=foresatt_1.iloc[0]['foresatt_adresse'],
                foresatt_tlfnr=foresatt_1.iloc[0]['foresatt_tlfnr'],
                foresatt_pnr=foresatt_1.iloc[0]['foresatt_pnr']
            )

            # Check if there is a second guardian (foresatt)
            foresatt_2_obj = None
            if pd.notna(row['foresatt_2']):
                foresatt_2 = forelder[forelder['foresatt_id'] == row['foresatt_2']]
                if not foresatt_2.empty:
                    foresatt_2_obj = Foresatt(
                        foresatt_id=foresatt_2.iloc[0]['foresatt_id'],
                        foresatt_navn=foresatt_2.iloc[0]['foresatt_navn'],
                        foresatt_adresse=foresatt_2.iloc[0]['foresatt_adresse'],
                        foresatt_tlfnr=foresatt_2.iloc[0]['foresatt_tlfnr'],
                        foresatt_pnr=foresatt_2.iloc[0]['foresatt_pnr']
                    )

            # Retrieve child (barn) data
            barn_1 = barn[barn['barn_id'] == row['barn_1']]
            if barn_1.empty:
                print("Warning: barn not found for soknad ID:", row['id'])
                continue  # Skip this row if no matching barn is found
            barn_1_obj = Barn(
                barn_id=barn_1.iloc[0]['barn_id'],
                barn_pnr=barn_1.iloc[0]['barn_pnr']
            )

            # Create a Soknad object
            soknad_obj = Soknad(
                sok_id=row['id'],
                foresatt_1=foresatt_1_obj,
                foresatt_2=foresatt_2_obj,
                barn_1=barn_1_obj,
                fr_barnevern=row['fr_barnevern'],
                fr_sykd_familie=row['fr_sykd_familie'],
                fr_sykd_barn=row['fr_sykd_barn'],
                fr_annet=row['fr_annet'],
                barnehager_prioritert=row['barnehager_prioritert'],
                sosken__i_barnehagen=row['sosken__i_barnehagen'],
                tidspunkt_oppstart=row['tidspunkt_oppstart'],
                brutto_inntekt=row['brutto_inntekt']
            )

            all_soknader.append(soknad_obj)

    except Exception as e:
        print("Error occurred:", e)  # Debug print for any unexpected errors
    return all_soknader

# Save all data to Excel
def commit_all():
    with pd.ExcelWriter('kgdata.xlsx', mode='a', if_sheet_exists='replace') as writer:
        forelder.to_excel(writer, sheet_name='foresatt')
        barnehage.to_excel(writer, sheet_name='barnehage')
        barn.to_excel(writer, sheet_name='barn')
        soknad.to_excel(writer, sheet_name='soknad')

# Function to get all data from the database
def get_all_data():
    # Fetch data from the respective tables
    data = {
        'forelder': forelder.to_dict(orient='records'),
        'barn': barn.to_dict(orient='records'),
        'barnehage': barnehage.to_dict(orient='records'),
        'soknad': soknad.to_dict(orient='records')
    }
    return data

