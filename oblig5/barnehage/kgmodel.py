from dataclasses import dataclass
from typing import Optional

@dataclass
class Foresatt:
    foresatt_id: int
    foresatt_navn: str
    foresatt_adresse: str
    foresatt_tlfnr: str
    foresatt_pnr: str

@dataclass
class Barn:
    barn_id: int
    barn_pnr: str

@dataclass
class Barnehage:
    barnehage_id: int
    barnehage_navn: str
    barnehage_antall_plasser: int
    barnehage_ledige_plasser: int

@dataclass
class Soknad:
    foresatt_navn: str
    foresatt_adresse: str
    foresatt_tlfnr: str
    foresatt_pnr: str
    foresatt_2_navn: Optional[str] = None
    foresatt_2_adresse: Optional[str] = None
    foresatt_2_tlfnr: Optional[str] = None
    foresatt_2_pnr: Optional[str] = None
    barn_pnr: Optional[str] = None
    barn_2_pnr: Optional[str] = None
    fr_barnevern: bool = False
    fr_sykd_familie: bool = False
    fr_sykd_barn: bool = False
    fr_annet: Optional[str] = None
    liste_over_barnehager_prioritert_5: Optional[str] = None
    tidspunkt_oppstart: Optional[str] = None
    sosken_i_barnehagen: bool = False
    brutto_inntekt: int = 0

