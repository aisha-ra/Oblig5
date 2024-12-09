import pandas as pd
import numpy as np
import dbexcel as db # Import everything from dbexcel globally
from kgmodel import *


def form_to_object_soknad(form_data):
    """
    Converts form data into a Soknad object.
    """
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


def insert_foresatt(f):
    """
    Inserts a new foresatt (guardian) into the foresatt DataFrame.
    """
    new_id = db.foresatt['foresatt_id'].max() + 1 if not db.foresatt.empty else 1
    if not db.foresatt[db.foresatt['foresatt_pnr'] == f.foresatt_pnr].empty:
        return  # Avoid duplicate entries by personnummer
    db.foresatt = pd.concat([
        db.foresatt,
        pd.DataFrame(
            [[new_id, f.foresatt_navn, f.foresatt_adresse, f.foresatt_tlfnr, f.foresatt_pnr]],
            columns=db.foresatt.columns
        )
    ], ignore_index=True)
    return db.foresatt


def insert_barn(b):
    """
    Inserts a new barn (child) into the barn DataFrame.
    """
    new_id = db.barn['barn_id'].max() + 1 if not db.barn.empty else 1
    if not db.barn[db.barn['barn_pnr'] == b.barn_pnr].empty:
        return  # Avoid duplicate entries by personnummer
    db.barn = pd.concat([
        db.barn,
        pd.DataFrame([[new_id, b.barn_pnr]], columns=db.barn.columns)
    ], ignore_index=True)
    return db.barn


def insert_soknad(s):
    """
    Inserts the submitted application into the database (soknad DataFrame).
    This function now works directly with the global db.soknad DataFrame.
    """
    # Ensure 'id' column exists
    if 'id' not in db.soknad.columns:
        db.soknad['id'] = pd.Series(dtype='int')  # Initialize empty 'id' column

    # Generate new application ID
    new_id = db.soknad['id'].max() + 1 if not db.soknad.empty else 1

    # Prepare the new row of data
    new_row = {
        'foresatt_pnr': s.foresatt_pnr,
        'foresatt_2_pnr': s.foresatt_2_pnr if s.foresatt_2_pnr else None,
        'barn_pnr': s.barn_pnr,
        'fr_barnevern': s.fr_barnevern,
        'fr_sykd_familie': s.fr_sykd_familie,
        'fr_sykd_barn': s.fr_sykd_barn,
        'fr_annet': s.fr_annet,
        'barnehager_prioritert': s.liste_over_barnehager_prioritert_5,
        'sosken_i_barnehagen': s.sosken_i_barnehagen,
        'tidspunkt_oppstart': s.tidspunkt_oppstart,
        'brutto_inntekt': s.brutto_inntekt,
        'kommune': 'Kristiansand',  # Set default kommune
        'id': new_id
    }

    # Insert the new row into the global db.soknad DataFrame
    db.soknad = pd.concat([db.soknad, pd.DataFrame([new_row])], ignore_index=True)
    
    # Debugging: Log what was inserted
    print("Inserted new soknad row into database:", new_row)
    print("Current state of db.soknad:")
    print(db.soknad)

def select_alle_barnehager():
    """
    Returns all barnehager (kindergartens) as Barnehage objects.
    """
    return db.barnehage.apply(
        lambda r: Barnehage(
            r['barnehage_id'],
            r['barnehage_navn'],
            r['barnehage_antall_plasser'],
            r['barnehage_ledige_plasser']
        ),
        axis=1
    ).to_list()


def select_barnehage_instans(barnehage_id):
    """
    Retrieves a single Barnehage object by its ID.
    """
    series = db.barnehage[db.barnehage['barnehage_id'] == barnehage_id]
    if series.empty:
        return None
    return Barnehage(
        barnehage_id,
        series.iloc[0]['barnehage_navn'],
        series.iloc[0]['barnehage_antall_plasser'],
        series.iloc[0]['barnehage_ledige_plasser']
    )

def select_alle_soknader():
    """
    Maps database rows from `db.soknad` into a structure expected by the template.
    Includes detailed debugging.
    """
    all_soknader = []
    try:
        for index, row in db.soknad.iterrows():
            # Debugging: Log each row
            print("Processing row:", row)

            # Map expected fields to the template's structure
            soknad_obj = {
                "id": row['id'],
                "foresatt_pnr": row['foresatt_pnr'],
                "barn_pnr": row['barn_pnr'],
                "barnehager_prioritert": row['barnehager_prioritert'],
                "tidspunkt_oppstart": row['tidspunkt_oppstart'],
                "brutto_inntekt": row['brutto_inntekt']
            }
            all_soknader.append(soknad_obj)

    except Exception as e:
        print("Error processing `db.soknad`: ", e)
    print("Mapped soknader:", all_soknader)  # Log mapped data
    return all_soknader


def commit_all():
    """
    Saves all DataFrames to the Excel file.
    """
    try:
        with pd.ExcelWriter('kgdata.xlsx', mode='w') as writer:
            db.foresatt.to_excel(writer, sheet_name='foresatt', index=True)
            db.barnehage.to_excel(writer, sheet_name='barnehage', index=True)
            db.barn.to_excel(writer, sheet_name='barn', index=True)
            db.soknad.to_excel(writer, sheet_name='soknad', index=True)
        print("Data committed successfully to Excel.")
    except Exception as e:
        print(f"Error committing data: {e}")
        raise


def get_all_data():
    """
    Retrieves all data from the database as a dictionary.
    """
    return {
        'foresatt': db.foresatt.to_dict(orient='records'),
        'barn': db.barn.to_dict(orient='records'),
        'barnehage': db.barnehage.to_dict(orient='records'),
        'soknad': db.soknad.to_dict(orient='records')
    }
