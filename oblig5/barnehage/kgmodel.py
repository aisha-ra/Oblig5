# kgmodel.py
from dataclasses import dataclass
from typing import Optional
# kgmodel.py

class Foresatt:
    def __init__(self, foresatt_id, foresatt_navn, foresatt_adresse, foresatt_tlfnr, foresatt_pnr):
        self.foresatt_id = foresatt_id
        self.foresatt_navn = foresatt_navn
        self.foresatt_adresse = foresatt_adresse
        self.foresatt_tlfnr = foresatt_tlfnr
        self.foresatt_pnr = foresatt_pnr


class Barn:
    def __init__(self, barn_id, barn_pnr):
        self.barn_id = barn_id
        self.barn_pnr = barn_pnr


class Barnehage:
    def __init__(self, barnehage_id, barnehage_navn, barnehage_antall_plasser, barnehage_ledige_plasser):
        self.barnehage_id = barnehage_id
        self.barnehage_navn = barnehage_navn
        self.barnehage_antall_plasser = barnehage_antall_plasser
        self.barnehage_ledige_plasser = barnehage_ledige_plasser


class Soknad:
    def __init__(
        self, foresatt_navn, foresatt_adresse, foresatt_tlfnr, foresatt_pnr,
        foresatt_2_navn=None, foresatt_2_adresse=None, foresatt_2_tlfnr=None, foresatt_2_pnr=None,
        barn_pnr=None, barn_2_pnr=None,
        fr_barnevern=False, fr_sykd_familie=False, fr_sykd_barn=False, fr_annet=None,
        liste_over_barnehager_prioritert_5=None, tidspunkt_oppstart=None,
        sosken_i_barnehagen=False, brutto_inntekt=0
    ):
        self.foresatt_navn = foresatt_navn
        self.foresatt_adresse = foresatt_adresse
        self.foresatt_tlfnr = foresatt_tlfnr
        self.foresatt_pnr = foresatt_pnr
        self.foresatt_2_navn = foresatt_2_navn
        self.foresatt_2_adresse = foresatt_2_adresse
        self.foresatt_2_tlfnr = foresatt_2_tlfnr
        self.foresatt_2_pnr = foresatt_2_pnr
        self.barn_pnr = barn_pnr
        self.barn_2_pnr = barn_2_pnr
        self.fr_barnevern = fr_barnevern
        self.fr_sykd_familie = fr_sykd_familie
        self.fr_sykd_barn = fr_sykd_barn
        self.fr_annet = fr_annet
        self.liste_over_barnehager_prioritert_5 = liste_over_barnehager_prioritert_5
        self.tidspunkt_oppstart = tidspunkt_oppstart
        self.sosken_i_barnehagen = sosken_i_barnehagen
        self.brutto_inntekt = brutto_inntekt
