
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

def izposodi(izvod, uporabnik):
    '''Funkcija izposodi izvod dane knjige danemu uporabniku. '''

    # ali ima uporabnik kaj dolga?
    with baza:
        baza.execute("""SELECT dolg FROM uporabniki WHERE id = ?""", [uporabnik])
        kolikoJe = baza.fetchone()
        if kolikoJe != 0:
            raise Exception("Najprej morate poravnati dolg!")
    
    
    # kaj, ce ima rezervacijo uporabnik

    # preverimo, ce je knjiga sploh na voljo
    with baza:
        ## imetabele.imestolpca
        baza.execute("""SELECT na_voljo FROM izvod_knjige WHERE id = ?""", [izvod])
        jeNaVoljo = baza.fetchone()
        if jeNaVoljo != 1:
            # knjiga je izposojena ali pa jo je rezerviral nekdo drug
            raise Exception("Knjiga je izposojena ali rezervirana. ")
        elif jeNaVoljo == 1:
            baza.execute("""INSERT INTO izposoja (izvod, uporabnik) VALUES (?, ?)""", [izvod, uporabnik])
            baza.execute("""UPDATE izvod_knjige SET na_voljo = 0 WHERE id = ?""", [izvod])
            baza.execute("""UPDATE izposoje SET datum_izposoje = ?""", [date.today()]) # kdaj si je izposodil


def zamudnine(datumIzposoje, datumVrnitve=date.today()):
    '''Funkcija vrne zamudnino uporabnikov.'''
    # zamudnina za en dan znaša 0.20 eur

    razlikaVDneh = (abs(datumVrnitve - datumIzposoje)).days
    if razlikaVDneh < 20:
        raise Exception("Zamudnine ni.")
    else:
        kolikoJe = (razlikaVDneh-20)*0.20
        baza.execute("""INSERT INTO uporabnik (dolg) VALUES (?)""", [kolikoJe])

def vrni(izvod):
    # obracunaj tudi zamudnino
    with baza:
        # vrne knjigo
        baza.execute("""UPDATE izvod_knjige SET na_voljo = 1 WHERE id = ?""", [izvod])
        baza.execute("""SELECT dolg FROM uporabniki WHERE id = ?""", [uporabnik])

 #####?????            
    pass

def placaj_dolg(uporabnik, znesek): # znesek??
    # napiše koliko je dolga in nekje mora biti kasneje gumb "Plačaj"
    
    pass

def rezerviraj(izvod, uporabnik):
    ''' Funkcija rezervira knjigo danemu uporabniku. '''

    pass

# dodaj/uredi knjigo

