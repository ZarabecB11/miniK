import sqlite3
from datetime import *

datoteka_baze = "miniK.sqlite3"
baza = sqlite3.connect(datoteka_baze, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)

def ha(izvod):
    
    with baza:
        cur = baza.cursor()
        cur.execute("""UPDATE izvodi_knjig SET na_voljo = 1 WHERE id = ?""", [izvod])
        cur.execute("""DELETE FROM izposoje""")
        cur.execute("""DELETE FROM rezervacije""")
#################################################

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

##################################################

def poglejVse():
    '''Funkcija vrne vse knjige, ki jih hrani knjižnica.'''
    
    with baza:
        cur = baza.cursor()
        cur.execute("""SELECT * FROM knjige""")
        return cur.fetchall()

##################################################

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
    
    # kaj, ce ima rezervacijo naš uporabnik
        
##        if jeNaVoljo[0] == 2: # knjiga je rezervirana
##            aliJePravi = cur.execute("""SELECT uporabnik FROM rezervacije WHERE izvod = ?""", [izvod])
##            if uporabnik == aliJePravi:
##                cur.execute("""INSERT INTO izposoje (izvod, uporabnik) VALUES (?, ?)""", [izvod, uporabnik])
##                cur.execute("""UPDATE izvodi_knjig SET na_voljo = 0 WHERE id = ?""", [izvod])
##                cur.execute("""UPDATE izposoje SET datum_izposoje = ?""", [date.today()])
##                cur.execute("""DELETE rezervacije WHERE izvod = ?""", [izvod])
                
    # preverimo, ce je knjiga sploh na voljo
    with baza:
        cur = baza.cursor()
        ## imetabele.imestolpca
        cur.execute("""SELECT na_voljo FROM izvodi_knjig WHERE id = ?""", [izvod])
        jeNaVoljo = cur.fetchone()

        cur.execute("""SELECT uporabnik FROM rezervacije WHERE izvod = ?""", [izvod])
        aliJePravi = cur.fetchone()

        if jeNaVoljo[0] != 1 and uporabnik != aliJePravi[0]:

            # knjiga je izposojena ali pa jo je rezerviral nekdo drug
            raise Exception("Knjiga je izposojena ali rezervirana. ")
        
        elif jeNaVoljo[0] == 1:

            cur.execute("""INSERT INTO izposoje (izvod, uporabnik) VALUES (?, ?)""", [izvod, uporabnik])
            cur.execute("""UPDATE izvodi_knjig SET na_voljo = 0 WHERE id = ?""", [izvod])
            cur.execute("""UPDATE izposoje SET datum_izposoje = ?""", [date.today()]) # kdaj si je izposodil

        else:
            cur.execute("""INSERT INTO izposoje (izvod, uporabnik) VALUES (?, ?)""", [izvod, uporabnik])
            cur.execute("""UPDATE izvodi_knjig SET na_voljo = 0 WHERE id = ?""", [izvod])
            cur.execute("""UPDATE izposoje SET datum_izposoje = ?""", [date.today()])
            cur.execute("""DELETE FROM rezervacije WHERE izvod = ?""", [izvod])

##################################################
           
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

##################################################

def vrni(izvod, uporabnik):
    
    with baza:
        cur = baza.cursor()
        # vrne knjigo
##        cur.execute("""UPDATE izvodi_knjig SET na_voljo = 1 WHERE id = ?""", [izvod])
##        cur.execute("""SELECT dolg FROM uporabniki WHERE id = ?""", [uporabnik])
    # do tu je OK :)
        

        cur.execute("""SELECT izvod FROM rezervacije WHERE izvod = ?""", [izvod])
        aliRezerviran = cur.fetchone()
        try:
            if aliRezerviran[0] == 2:
                cur.execute("""UPDATE izvodi_knjig SET na_voljo = 2 WHERE id = ?""", [izvod])
        except:
            cur.execute("""UPDATE izvodi_knjig SET na_voljo = 1 WHERE id = ?""", [izvod])

        cur.execute("""SELECT datum_izposoje FROM izposoje WHERE id = ?""", [izvod])
        kdajIzposodil = cur.fetchall()
        datumVrnitve = date.today()
        zamudnina = obracunajZamudnino(kdajIzposodil[0][0], datumVrnitve)

        cur.execute("""DELETE from izposoje WHERE izvod = ?""", [izvod])
        return zamudnina

##################################################

def placaj_dolg(uporabnik):
    # napiše koliko je dolga in nekje mora biti kasneje gumb "Plačaj"
    with baza:
        cur = baza.cursor()
        cur.execute("""SELECT dolg FROM uporabniki WHERE id = ?""", [uporabnik])
        kolikoDolga = cur.fetchone()
        return kolikoDolga[0]

##################################################

def rezerviraj(izvod, uporabnik):
    ''' Funkcija rezervira knjigo danemu uporabniku. '''

    # Za rezervacijo je zapisana številka 2
    with baza:
        
        cur = baza.cursor()
        ## imetabele.imestolpca
        cur.execute("""SELECT na_voljo FROM izvodi_knjig WHERE id = ?""", [izvod])
        jeNaVoljo = cur.fetchone()
        
        if jeNaVoljo[0] == 1:
            # knjiga je na voljo za izposojo
            raise Exception("Knjiga je na voljo za izposojo, zato rezervacija ni možna. ")
        
        elif jeNaVoljo[0] != 1:
            # knjiga je izposojena ali rezervirana, zato je dodatna rezervacija možna 
            cur.execute("""INSERT INTO rezervacije (izvod, uporabnik) VALUES (?, ?)""", [izvod, uporabnik])
            cur.execute("""UPDATE izvodi_knjig SET na_voljo = 2 WHERE id = ?""", [izvod])
            cur.execute("""UPDATE rezervacije SET datumRezervacije = ?""", [date.today()]) # kdaj si je izposodil
