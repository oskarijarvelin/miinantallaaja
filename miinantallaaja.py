import random #Tuo satunnaisuuden mahdollistavan moduulin
import time #Tuo aikaan liittyviä työkaluja sisältävän moduulin

def paavalikko():
    """Luo peliin valikon, josta voi aloittaa uuden pelin, avata tilastot ja lopettaa ohjelman."""
    print(" ") 
    print("*** MIINANTALLAAJA ***")
    while True:
        print("*     Päävalikko     *") #Pelin kaikki printit ovat 22 kirjainta pitkiä
        print("(U)usi peli")
        print("(T)ilastot")
        print("(L)opeta")
        syote = input("Valitse toiminto: ")
        syote = syote.lower() #Hyväksyy kirjaimet koosta riippumatta
        if syote == "u":
            valinta = "u"
            break
        elif syote == "t":
            valinta = "t"
            break
        elif syote == "l":
            valinta = "l"
            break
        else:
            print("Virheellinen toiminto!")
    return valinta

def kysy_kentta():
    """Kysyy pelin alkaessa käyttäjältä toivotun kentän leveyden, korkeuden ja miinojen määrän."""
    while True:
        kentandata = input("Anna kentän leveys, korkeus ja miinojen määrä (esim. 9,9,2): ").split(",")
        if len(kentandata) != 3: #varmistaa, että käyttäjä antaa yhteensä kolme syötettä
            print("Anna kolme lukua pilkuilla erotettuna!")
        else:
            try:
                int(kentandata[0])
                int(kentandata[1])
                int(kentandata[2])
            except ValueError:
                print("Anna luvut kokonaislukuina.")
            else:
                if int(kentandata[0]) < 2:
                    print("Kentän leveyden tulee olla vähintään 2.")
                elif int(kentandata[1]) < 2:
                    print("Kentän korkeuden tulee olla vähintään 2.")
                else:
                    if int(kentandata[2]) < 1: #Asettaa pienimmän sallitun miinojen määrän
                        print("Miinoja on liian vähän.")
                    elif int(kentandata[2]) > ((int(kentandata[0]) * int(kentandata[1])) - 1): #Asettaa suurimman sallitun miinojen määrän
                        print("Miinoja on liian paljon.")
                    else:
                        try:
                            leveys = int(kentandata[0])
                            korkeus = int(kentandata[1])
                            miinoja = int(kentandata[2])
                        except ValueError:
                            print("Anna luvut kokonaislukuina.")
                        else:
                            break #Kysyy kolmea syötettä kunnes saa ne
    kentta = []
    rivi = []
    for rivi in range(korkeus): #luo kentän korkeuden
        kentta.append([])
        for sarake in range(leveys): #luo kentän leveyden
            kentta[-1].append("-")
    return kentta, miinoja
    
def miinoita_satunnainen(kentta, miinoittamatta):
    """Asettaa kentälle yhden miinan satunnaiseen, vapaaseen ruutuun ja palauttaa tämän ruudun koordinaatit."""
    miina = random.choice(miinoittamatta)
    miinax = miina[0]
    miinay = miina[1]
    #kentta[miinay][miinax] = "*" #Näyttää miinat
    miinoittamatta.remove((miinax, miinay))
    return miinax, miinay
    
def avaa_ruutuja(kentta, miinat):
    """Ylläpitää kyselykierrettä, kunnes saa None None. Muuttaa o-kirjaimet x-kirjaimiksi."""
    mimaara = int((len(miinat))) #Laskee miinojen määrän
    rumaara = int(((int(len(kentta[0]))) * (int(len(kentta))))) #Laskee ruutujen määrän
    vumaara = 0
    
    kentan_koko = "{}x{}".format(int(len(kentta[0])), int(len(kentta))) #Laskee kentän koon tilastoa varten
    miinojen_maara = int(len(miinat)) #Laskee miinojen määrän tilastoa varten
    alkuaika = time.time() #Tallentaa aloitusajan tilastointia varten
    
    while True:
        tulosta_kentta(kentta)
        t, x, y = kysy_koordinaatti(kentta)
        miinatymparilla = str(laske_miinat(x, y, kentta, miinat)) #Laskee ympärillä olevien miinojen määrän
        if miinatymparilla == "0": #Muuttaa 0-ruudut tyhjiksi
            miinatymparilla = " "

        if t == "a": #Kun avataan ruutuja            
            if miinat.count((x, y)) > 0:
                lopputulos = "Häviö"
                aika = time.strftime("%d.%m.%Y %H:%M:%S") #Muotoilee ajan muotoon DD.MM.YYY HH:MM:SS
                kesto = round((round(time.time() - alkuaika)) / 60) #Laskee aloitus- ja lopetusajan eron sekunteina ja pyöristää sen minuuteiksi
                tallenna_tilasto(aika, kesto, vumaara, lopputulos, kentan_koko, miinojen_maara) #Tallentaa tilaston
                return False #Game over
            else:
                if kentta[y][x] == "-": #Avaa ruudun vain jos ruutu on avaamaton
                    kentta[y][x] = miinatymparilla #Avaa ruudun
                    rumaara -= 1
                    vumaara += 1 #Laskee vuorot
                if rumaara == mimaara:
                    lopputulos = "Voitto"
                    aika = time.strftime("%d.%m.%Y %H:%M:%S") #Muotoilee ajan muotoon DD.MM.YYY HH:MM:SS
                    kesto = round((round(time.time() - alkuaika)) / 60) #Laskee aloitus- ja lopetusajan eron sekunteina ja pyöristää sen minuuteiksi
                    tallenna_tilasto(aika, kesto, vumaara, lopputulos, kentan_koko, miinojen_maara) #Tallentaa tilaston
                    return True #Victory!
        elif t == "l":
            kentta[y][x] = "L" #Liputtaa ruudun, liputus ei estä ruudun avaamista
        elif t == "?":
            kentta[y][x] = "?" #Epäilee ruutua, epäily ei estä ruudun avaamista

def kysy_koordinaatti(kentta):
    """Kysyy käytttäjältä toiminnon ja koordinaatin. Toiminto on a = avaa tai l = lippu. Syöte on muotoa a, 2, 2."""
    leveys = len(kentta[0])
    korkeus = len(kentta)    
    while True:
        koordinaatit = input("Anna toiminto ja koordinaatit (esim a,1,1): ").split(",")
        if len(koordinaatit) != 3: #varmistaa, että käyttäjä antaa yhteensä kolme syötettä
            print("Anna toiminto ja kaksi koordinaattia pilkulla erotettuna")
        else:
            t = koordinaatit[0] #tallentaa valitun toiminnon muuttujaan t
            t = t.lower()
            if t == "a" or t == "l" or t == "?": #määrittelee sallitut toiminnot
                try: #varmistaa, että koordinaatit ovat kokonaislukuja
                    x = int(koordinaatit[1])
                    y = int(koordinaatit[2])
                except ValueError:
                    print("Anna koordinaatit kokonaislukuina")
                else:
                    if x < 0 or x > (leveys - 1): #varmistaa, että koordinaatti on kentän sisällä
                        print("Koordinaatit ovat ruudukon ulkopuolella")
                    elif y < 0 or y > (korkeus - 1):
                        print("Koordinaatit ovat ruudukon ulkopuolella")
                    else:
                        break
            else:            
                print("Mahdolliset toiminnot: (A)vaa, (L)iputa, (?)") #tulostaa sallitut toiminnot
    return t, x, y

def laske_miinat(x, y, kentta, miinat):
    """Laskee ruudun ympärillä olevat ninjat."""
    tarkistettava = [[x - 1, y - 1],
                     [x - 1, y + 0],
                     [x - 1, y + 1],
                     [x + 0, y - 1],
                     [x + 0, y + 1],
                     [x + 1, y - 1],
                     [x + 1, y + 0],
                     [x + 1, y + 1]]                  
    maara = 0
    leveys = len(kentta[0])
    pituus = len(kentta)
    for i in range(0, 8):
        try:
            x = tarkistettava[i][0]
            y = tarkistettava[i][1]
            if x < 0:
                pass
            elif y < 0:
                pass
            elif x > (leveys - 1):
                pass
            elif y > (pituus - 1):
                pass
            else:
                if miinat.count((x, y)) > 0:
                    maara += 1
                else:
                    maara += 0
        except IndexError:
            pass
    return maara

def tulosta_kentta(kentta):
    """Tulostaa kentän."""
    for i in range(0, (len(kentta))):
        print(" ".join(kentta[i]))
    
def tallenna_tilasto(aika, kesto, vumaara, lopputulos, kentan_koko, miinojen_maara):
    """Tallentaa tilastoon päivämäärän, kellonajan, keston minuuteissa, keston vuoroissa, lopputuloksen, kentän koon ja miinojen lukumäärän."""
    rivinvaihto = "\n"
    try:
        with open("tilasto.txt", "a") as tilasto:        
            tilasto.write("{},{},{},{},{},{}{}".format(aika, kesto, vumaara, lopputulos, kentan_koko, miinojen_maara, rivinvaihto))
    except IOError:
        print("Tilastotiedoston avaaminen epäonnistui.")
   
def lue_tilasto():
    """Näyttää tilastoon tallennetut tiedot."""
    print(" ")
    tulokset = []
    try:
        with open("tilasto.txt", "r") as tilasto:        
            for rivi in tilasto.readlines():
                try:
                    aika, kesto, vumaara, lopputulos, kentan_koko, miinojen_maara = rivi.split(",") #Lukee datan riviltä
                    vumaara = int(vumaara)
                    lopputulos = lopputulos.strip()
                    kentan_koko = kentan_koko.strip()
                    miinojen_maara = int(miinojen_maara)
                    tulokset.append([aika, kesto, vumaara, lopputulos, kentan_koko, miinojen_maara]) #Lisää datan tulokset-listan alkioiksi
                except ValueError:
                    print("Riviä ei saatu luettua: {}".format(rivi))
            for i in range(0, (len(tulokset))): #Sijoittaa datan lukijaystävälliseen kontekstiin    
                print("Pelattu: {}, kesto: {}min / {} vuoroa, {}, kentän koko: {} ja {} miinaa.". format(tulokset[i][0], tulokset[i][1], tulokset[i][2], tulokset[i][3], tulokset[i][4], tulokset[i][5]))
    except IOError:
        print("Tilastotiedoston avaaminen epäonnistui.")
   
def tarkista_voitto():
    """Luo kentän, miinat ja tarkistaa voiton tai häviön"""
    kentta, miinoja = kysy_kentta()
    miinoittamatta = []
    miinat = []
    for x in range(0, (len(kentta[0]))): #laskee kentän kaikki (miinoittamattomat) koordinaatit
        for y in range(0, (len(kentta))):
            miinoittamatta.append((x, y))
    for i in range(0, miinoja): #Lisää käyttäjän toivoman määrän miinoja satunnaisiin paikkoihin    
        miinax, miinay = miinoita_satunnainen(kentta, miinoittamatta)
        miinat.append((miinax, miinay)) #Tallentaa kaikki miinat listaan

    if avaa_ruutuja(kentta, miinat) == False: #Häviön tarkistus
        tulosta_kentta(kentta)
        print(" ")
        print("***   GAME OVER!   ***")

    else: #Voiton tarkistus
        tulosta_kentta(kentta)
        print(" ")
        print("***    VICTORY!    ***")

def main():
    """Pyörittää peliä, kunnes miina räjähtää tai kaikki miinattomat ruudut ovat aukaistu."""        
    while True:
        valinta = paavalikko()
        if valinta == "u":
            tarkista_voitto()
        if valinta == "t":
            lue_tilasto()
        if valinta == "l":
            break

main()