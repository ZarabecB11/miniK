
import sqlite3
from datetime import *

datoteka_baze = "miniK.sqlite3"
baza = sqlite3.connect(datoteka_baze, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)

# dela :D
def poisciKnjigo(naslov="", avtor="", letomin=1000, letomax = 2015, zalozba="", kljucna_beseda=""):
    '''Funkcija poisce vse knjige glede na iskane parametre.'''
    
    with baza:
        cur = baza.cursor()
        cur.execute("""SELECT *
                     FROM knjige JOIN kljucneBesede ON knjige.id = kljucneBesede.knjiga
                     WHERE knjige.naslov LIKE ?
                     AND knjige.avtor LIKE ?
                     AND knjige.letoIzdaje BETWEEN ? AND ?
                     AND knjige.založba LIKE ?
                     AND kljucneBesede.beseda LIKE ?""",
        [naslov + "%", avtor + "%", letomin, letomax, zalozba + "%", kljucna_beseda + "%"])

    return cur.fetchall()

# ta dela :D :D
def poglejVse():
    '''Funkcija vrne vse knjige, ki jih hrani knjižnica.'''
    
    with baza:
        cur = baza.cursor()
        cur.execute("""SELECT * FROM knjige""")
        return cur.fetchall()


# kar je napisano dela :)
def izposodi(izvod, uporabnik):
    '''Funkcija izposodi izvod dane knjige danemu uporabniku. '''

    # uporabnik podan s številko uporabnika (oz. z id-jem)

    # ali ima uporabnik kaj dolga?
    with baza:
        cur = baza.cursor()
        cur.execute("""SELECT dolg FROM uporabniki WHERE id = ?""", [uporabnik])
        kolikoJe = cur.fetchone()
        if kolikoJe[0] != 0:
            raise Exception("Najprej morate poravnati dolg!")
    
    # kaj, ce ima rezervacijo uporabnik ????

    # preverimo, ce je knjiga sploh na voljo
    with baza:
        
        cur = baza.cursor()
        ## imetabele.imestolpca
        cur.execute("""SELECT na_voljo FROM izvodi_knjig WHERE id = ?""", [izvod])
        jeNaVoljo = cur.fetchone()
        
        if jeNaVoljo[0] != 1:
            # knjiga je izposojena ali pa jo je rezerviral nekdo drug
            raise Exception("Knjiga je izposojena ali rezervirana. ")
        
        elif jeNaVoljo[0] == 1:
            cur.execute("""INSERT INTO izposoje (izvod, uporabnik) VALUES (?, ?)""", [izvod, uporabnik])
            cur.execute("""UPDATE izvodi_knjig SET na_voljo = 0 WHERE id = ?""", [izvod])
            cur.execute("""UPDATE izposoje SET datum_izposoje = ?""", [date.today()]) # kdaj si je izposodil


def obracunajZamudnino(datumIzposoje, datumVrnitve):
    '''Funkcija vrne zamudnino uporabnikov.'''
    # zamudnina za en dan znaša 0.20 eur

    cur = baza.cursor()

    # glede na datum izposoje moramo pogledati današnji datum, da pogledam, èe je minilo > 20 dni 
    razlikaVDneh = datumVrnitve - datumIzposoje
    razlikaVDneh1 = razlikaVDneh.days
    if razlikaVDneh1 < 20:
        # v tem primeru ni zamudnine
        pass
    else:
        kolikoJe = (razlikaVDneh-20)*0.20
        cur.execute("""INSERT INTO uporabnik (dolg) VALUES (?)""", [kolikoJe])

def vrni(izvod, uporabnik):
    
    with baza:
        cur = baza.cursor()
        # vrne knjigo
        cur.execute("""UPDATE izvodi_knjig SET na_voljo = 1 WHERE id = ?""", [izvod])
        cur.execute("""SELECT dolg FROM uporabniki WHERE id = ?""", [uporabnik])
    # do tu je OK :)

        cur.execute("""SELECT datum_izposoje FROM izposoje""")
        kdajIzposodil = cur.fetchall()
        # vzemi prvi kdajIzposodil[0]!
        datumVrnitve = date.today()
        zamud = zamudnine(kdajIzposodil, datumVrnitve)
    pass

def placaj_dolg(uporabnik, znesek): # znesek??
    # napiše koliko je dolga in nekje mora biti kasneje gumb "Plačaj"
    
    pass

def rezerviraj(izvod, uporabnik):
    ''' Funkcija rezervira knjigo danemu uporabniku. '''

    pass

# dodaj/uredi knjigo - vsak ne more dodati knjige v bazo

