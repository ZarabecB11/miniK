
import sqlite3
datoteka_baze = "miniK.sqlite3"

def poisciKnjigo(nasl="", avt="", le = "", zaloz = "", kljucna="", ):
    ''' Funkcija poisce vse knjige glede na iskane parametre. '''
    
    c = baza.cursor()
    c.execute("""SELECT *
                 FROM knjige JOIN kljucnaBeseda ON knjige.id = kljucnaBeseda.knjiga
                 WHERE naslov LIKE ?
                 AND avtor LIKE ?
                 AND leto LIKE ?
                 AND zalozba LIKE ?
                 AND kljucna LIKE ?""",
              [nasl, avt, le, zaloz, kljucna])
    poiskane = c.fetchall()
    c.close()
    return poiskane

##def izposodi(naslov):
##    '''Funkcija izposodi knjigo. '''
##
##    c = baza.cursor()
##    c.execute("""SELECT na_voljo FROM izvod_knjige""")
##    jeNaVoljo = c.fetchall():
##    if jeNaVoljo == [1]:
##        c.execute("""SELECT """)


baza = sqlite3.connect(datoteka_baze, isolation_level=None)
