import pandas as pd
from kgmodel import Barnehage  # Ensure Barnehage is imported correctly

def initiate_db(db_name):
    # Example kindergarten data
    barnehage_liste = [
        Barnehage(barnehage_id=1, barnehage_navn="Sunshine Preschool", barnehage_antall_plasser=50, barnehage_ledige_plasser=15),
        Barnehage(barnehage_id=2, barnehage_navn="Happy Days Nursery", barnehage_antall_plasser=25, barnehage_ledige_plasser=2),
        Barnehage(barnehage_id=3, barnehage_navn="123 Learning Center", barnehage_antall_plasser=35, barnehage_ledige_plasser=4),
        Barnehage(barnehage_id=4, barnehage_navn="ABC Kindergarten", barnehage_antall_plasser=12, barnehage_ledige_plasser=0),
        Barnehage(barnehage_id=5, barnehage_navn="Tiny Tots Academy", barnehage_antall_plasser=15, barnehage_ledige_plasser=5),
        Barnehage(barnehage_id=6, barnehage_navn="Giggles and Grins Childcare", barnehage_antall_plasser=10, barnehage_ledige_plasser=0),
        Barnehage(barnehage_id=7, barnehage_navn="Playful Pals Daycare", barnehage_antall_plasser=40, barnehage_ledige_plasser=6)
    ]
    
    # Define columns for each sheet
    kolonner_forelder = ['foresatt_id', 'foresatt_navn', 'foresatt_adresse', 'foresatt_tlfnr', 'foresatt_pnr']
    kolonner_barnehage = ['barnehage_id', 'barnehage_navn', 'barnehage_antall_plasser', 'barnehage_ledige_plasser']
    kolonner_barn = ['barn_id', 'barn_pnr']
    kolonner_soknad = ['sok_id', 'foresatt_1', 'foresatt_2', 'barn_1', 'fr_barnevern', 'fr_sykd_familie', 'fr_sykd_barn', 'fr_annet', 'barnehager_prioritert', 'sosken__i_barnehagen', 'tidspunkt_oppstart', 'brutto_inntekt']

    # Initialize empty dataframes for forelder, barn, and soknad
    forelder = pd.DataFrame(columns=kolonner_forelder)
    barn = pd.DataFrame(columns=kolonner_barn)
    soknad = pd.DataFrame(columns=kolonner_soknad)

    # Convert the list of kindergartens to a DataFrame
    barnehage = pd.DataFrame([vars(b) for b in barnehage_liste], columns=kolonner_barnehage)

    # Write each DataFrame to a separate sheet in kgdata.xlsx
    with pd.ExcelWriter(db_name) as writer:
        forelder.to_excel(writer, sheet_name='foresatt')
        barnehage.to_excel(writer, sheet_name='barnehage')
        barn.to_excel(writer, sheet_name='barn')
        soknad.to_excel(writer, sheet_name='soknad')

# Initialize database
initiate_db("kgdata.xlsx")
