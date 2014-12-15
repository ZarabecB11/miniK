
import sqlite3
datoteka_baze = "miniK.sqlite3"
baza = sqlite3.connect(datoteka_baze, isolation_level=None)

def poisciKnjigo(nasl="", avt="", le = "", zaloz = "", kljucna="", ):
    ''' Funkcija poisce vse knjige glede na iskane parametre. '''
    
    with baza:
        baza.execute("""SELECT *
                     FROM knjige JOIN kljucnaBeseda ON knjige.id = kljucnaBeseda.knjiga
                     WHERE naslov LIKE ?
                     AND avtor LIKE ?
                     AND leto LIKE ?
                     AND zalozba LIKE ?
                     AND kljucna LIKE ?""",
        [nasl, avt, le, zaloz, kljucna])
    poiskane = baza.fetchall()
    return poiskane

# v izdelavi 
##def izposodi(ime, naslov):
##    '''Funkcija izposodi knjigo z danim naslovom nekemu uporabniku. '''
##
##    # preverimo, ce je knjiga sploh na voljo
##    with baza:
##        baza.execute("""SELECT na_voljo FROM izvod_knjige JOIN knjige ON knjige.id = izvod_knjige.knjiga
#### imetabele.imestolpca
##                 WHERE naslov.knjige LIKE ?""", [naslov])
##    jeNaVoljo = baza.fetchall():
##
##    # izposodimo knjigo uporabniku s pravo id stevilko    
##    if jeNaVoljo == [1]:
##        with baza:
##            # baza.execute("""SELECT id FROM uporabnik WHERE kdo == id.uporabnik""")
##            
##            baza.execute("""INSERT INTO izposoja (izvod, uporabnik)
##                     SELECT id.izvod_knjige FROM izvod_knjige,
##                     SELECT id.uporabnik FROM uporabnik WHERE id.uporabnik LIKE ?""", [ime])
##            baza.execute("""UPDATE izvod_knjige set na_voljo = 0 WHERE id.izvod_knjige = """)


