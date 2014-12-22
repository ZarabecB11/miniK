
import sqlite3
from datetime import *

datoteka_baze = "miniK.sqlite3"
baza = sqlite3.connect(datoteka_baze, isolation_level=None)

def poisciKnjigo(naslov="", avtor="", leto="", zalozba="", kljucna_beseda=""):
    '''Funkcija poisce vse knjige glede na iskane parametre.'''
    
    with baza:
        baza.execute("""SELECT *
                     FROM knjige JOIN kljucneBesede ON knjige.id = kljucneBesede.knjiga
                     WHERE knjige.naslov LIKE ?
                     AND knjige.avtor LIKE ?
                     AND knjige.leto LIKE ?
                     AND knjige.zalozba LIKE ?
                     AND kljucneBesede.beseda LIKE ?""",
        [naslov, avtor, leto, zalozba, kljucna_beseda])
    
    return baza.fetchall()

def poglejVse():
    '''Funkcija vrne vse knjige, ki jih hrani knjižnica.'''
    
    with baza:
        baza.execute("""SELECT * FROM knjige""")
        return baza.fetchall()

# v izdelavi 
def izposodi(izvod, uporabnik):
    '''Funkcija izposodi izvod dane knjige danemu uporabniku. '''

    # preverimo, ce je knjiga sploh na voljo
    with baza:
        ## imetabele.imestolpca
        baza.execute("""SELECT na_voljo FROM izvod_knjige WHERE id = ?""", [izvod])
        jeNaVoljo = baza.fetchone()
        if jeNaVoljo is None:
            raise Exception("Knjiga ne obstaja.")
        elif jeNaVoljo == 0:
            raise Exception("Knjiga je izposojena.")
        elif jeNaVoljo == 1:
            baza.execute("""INSERT INTO izposoja (izvod, uporabnik) VALUES (?, ?)""", [izvod, uporabnik])
            baza.execute("""UPDATE izvod_knjige SET na_voljo = 0 WHERE id = ?""", [izvod])
            baza.execute("""UPDATE izposoje SET datum_izposoje = ?""", [date.today()])

def zamudnine(datumIzposoje, datumVrnitve=date.today()):
    '''Funkcija vrne zamudnino uporabnikov.'''
    # zamudnina za en dan znaša 0.45 eur

    kolikoCasa = datumVrnitve - datumIzposoje
    if kolikoCasa < 20:
        # ni zamudnine
        pass
    else:
        # for zanja -> kolikoDniZamuja += zamudninaZaEnDan 
        kolikoDni = datumIzposoje + 20

def rezerviraj(izvod, uporabnik):
    ''' Funkcija rezervira knjigo danemu uporabniku. '''

    pass
