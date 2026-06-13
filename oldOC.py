import pygame 
import random 
from time import sleep as wait
from datetime import datetime, timedelta
import json
import os

pygame.init()

screen = pygame.display.set_mode((1280,720 ))
pygame.display.set_caption("Keep Gambling!!! And never stop!")
White=(255, 255, 255)
Red=(255, 0, 0)
Green=(0, 255, 0)
Blue=(0, 0, 255)
Black=(0, 0, 0)
yellowish=(255, 255, 200)
Lightblue = (173, 216, 230)
Yellow = (255, 255, 0)
Gray = (128, 128, 128)
gesplayer = 0
gesdealr = 0
Spielname = "Blackjack"
Gegner = "Dealer"
dealvalone = 0
gesplayerstr = ""
gesdealrstr = ""
endprint = False
blackjackstartscreen = True
doubleornothingstartscreen = False

#Fonts und Starttext
font = pygame.font.SysFont("Arial", 48)
bjtitle_font = pygame.font.SysFont("Arial", 250)
dontitle_font = pygame.font.SysFont("Arial", 180)
title = bjtitle_font.render(Spielname, True, Black)
titlepos = title.get_rect(center=(640, 60))
starttxt = font.render("START", True, White)
esctxt = font.render("ESC", True, White)
startbutton = pygame.Rect(540, 500, 200, 70)
escbutton = pygame.Rect(20, 20, 100, 40)
menuButton = pygame.Rect(540, 500, 100, 40)
menuTxt = font.render("Menü", True, White)

#Spielernamen und Gesamtwerte
dealer = font.render(Gegner, True, Black)
dealerpos = dealer.get_rect(center=(640, 20))
player = font.render("Player", True, Black)
playerpos = player.get_rect(center=(640, 680))
playergesamttxt = font.render("Gesamt:", True, Black)
playergesamtpos = playergesamttxt.get_rect(center=(1000, 680))
dealergesamttxt = font.render("Gesamt:", True, Black)
dealergesamtpos = playergesamttxt.get_rect(center=(1000, 20))

#ask for next move
nextmove = font.render("Whats your next move? Double[Tab], Pass[p], Card[c] ?", True, Black)
nextmovepos = nextmove.get_rect(center=(640, 400))

nextmoveohnetab = font.render("Whats your next move? Pass[p], Card[c] ?", True, Black)
nextmoveohnetabpos = nextmoveohnetab.get_rect(center=(640, 400))

covermove = font.render("████████████████████████████████████████████████████████████████", True, White)
covermovepos = nextmove.get_rect(center=(640, 400))

ziehensecnd = font.render("Noch eine Karte? [j/n]", True, Black)
ziehensecndpos = nextmove.get_rect(center=(640, 400))
#🫵🤏🍆
slider_rect = pygame.Rect(400, 650, 500, 10)  # Leiste
knob_radius = 10
knob_x = slider_rect.x + slider_rect.width // 2
dragging = False
jetons_Einsatz = 0
slider_percent = 0.5  # Default to 50% position

if not os.path.exists("Blackjack.json"):
    with open("Blackjack.json", "w") as f:
        json.dump({"Jetons": 10000, 
                   "start": datetime.now().isoformat(),
                   "Belohnung": 1}, f)

filename = "Blackjack.json"

with open(filename, "r") as f:
    data = json.load(f)
Jetons = data.get("Jetons", 10000)

Belohnung = data.get("Belohnung", 1)

def update_data(new_data):
    with open(filename, "r") as f:
        data = json.load(f)
    data.update(new_data)
    with open(filename, "w") as f:
        json.dump(data, f)
    print("Daten aktualisiert:", new_data)
def update_everything():
    global Jetons, Belohnung
    update_data({"Jetons": Jetons, "Belohnung": Belohnung})

# Falls "start" fehlt, setze sie jetzt
if "start" not in data:
    data["start"] = datetime.now().isoformat()
    with open(filename, "w") as f:
        json.dump(data, f)

# Zeit berechnen
saved_time = datetime.fromisoformat(data["start"])
elapsed = datetime.now() - saved_time

print(f"Vergangene Zeit: {elapsed}")

# Belohnung prüfen
if elapsed.total_seconds() >= 86400:
    print("24 Stunden sind vergangen!")
    data["Belohnung"] = (data.get("Belohnung", 0) + 1)
    data["start"] = datetime.now().isoformat()  # Timer zurücksetzen

    # Speichern
    with open(filename, "w") as f:
        json.dump(data, f)
else:
    print("Noch nicht 24 Stunden.")

def slider():
    global knob_x, jetons_Einsatz,dragging, Jetons, slider_rect, slider_percent
    # Ziehen mit Maus
    if dragging:
        mouse_x = pygame.mouse.get_pos()[0]
        knob_x = max(slider_rect.x, min(mouse_x, slider_rect.x + slider_rect.width))

    # Berechne Einsatz proportional zum Jetons-Guthaben
    slider_percent = (knob_x - slider_rect.x) / slider_rect.width
    jetons_Einsatz = int(slider_percent * Jetons)
    

    # Zeichnen
    slider_area = pygame.Rect(slider_rect.x, slider_rect.y - 50, slider_rect.width, slider_rect.height + 60)
    pygame.draw.rect(screen, White, slider_area)
    pygame.draw.rect(screen, Black, slider_rect)
    pygame.draw.circle(screen, Red, (knob_x, slider_rect.y + slider_rect.height // 2), knob_radius)

    einsatz_text = font.render(f"Einsatz: {jetons_Einsatz}", True, (0, 0, 0))
    screen.blit(einsatz_text, (slider_rect.x, slider_rect.y - 60))

#Endprints
endtxt = font.render(f"Spiel beendet! Drücke ESC zum Beenden", True, Black )
endtxt_rect = endtxt.get_rect(center=(640, 400))
gewonnentxt = font.render(f"Du hast gewonnen! Dealer hatte: {gesdealr} Du hattest: {gesplayer}", True, Black)
gewonnentxt_rect = gewonnentxt.get_rect(center=(600, 360))
verlorentxt = font.render(f"Du hast verloren! Dealer hatte: {gesdealr} Du hattest: {gesplayer}", True, Black)
verlorentxt_rect = verlorentxt.get_rect(center=(600, 360))
drawtxt = font.render((f"Unentschieden! Dealer hatte: {gesdealr} Du hattest: {gesplayer}"), True, Black)
drawtxt_rect = drawtxt.get_rect(center=(600, 360))
bjdealer = font.render(f"Dealer hatte Blackjack! Du hattest: {gesplayer} ", True, Black)
bjdealer_rect = bjdealer.get_rect(center=(600, 360))
bjplayer = font.render(f"Du hattest Blackjack! Dealer hatte: {gesdealr}", True, Black)
bjplayer_rect = bjplayer.get_rect(center=(600, 360))
bjp = False
bjd = False

#Positionen für die Karten
y_title = -100
zustand = "start"
x_cardstartplyr = 350
x_abstand = 120
Y_cardstartplyr = 560
aktion = None
x_cardstartdlr = 350
x_abstanddlr = 120
Y_cardstartdlr = 200
A=0
#karten werden ausgeteilt
karteEins = 0
karteZwei = 0 
dealerEins = 0
dealerZwei = 0
G=0
started = False

#doube or nothing
x=100
y=200

#Definitionen
def NeueKarte():
    
    return random.randint(1, 13)

def kartenname(karte):
        if karte == 1:
            return "A", 11
        elif 2 <= karte <= 10:
            return str(karte), karte
        elif karte == 11:
            return "B", 10
        elif karte == 12:
            return "Q", 10
        elif karte == 13:
            return "K", 10
    
def Kartenplyr(cardname ):
    global x_cardstartplyr
    Cardsplyrpos = pygame.Rect(x_cardstartplyr - 10, Y_cardstartplyr-10, 100, 140)
    symbol = random.randint(1,4)
    
    if symbol ==1 :
        cardplyr = font.render(f"{cardname}♠", True, Black)
        screen.blit(cardplyr, (x_cardstartplyr, Y_cardstartplyr))
        pygame.draw.rect(screen, yellowish, Cardsplyrpos, 2)
        x_cardstartplyr+= x_abstand
    elif symbol ==2 :
        cardplyr = font.render(f"{cardname}♣", True, Black)
        screen.blit(cardplyr,(x_cardstartplyr, Y_cardstartplyr))
        pygame.draw.rect(screen, yellowish, Cardsplyrpos, 2)
        x_cardstartplyr+= x_abstand
    elif symbol ==3 :
        cardplyr = font.render(f"{cardname}♥", True, Red)
        screen.blit(cardplyr,(x_cardstartplyr, Y_cardstartplyr))
        pygame.draw.rect(screen, yellowish, Cardsplyrpos, 2)
        x_cardstartplyr+= x_abstand
    elif symbol == 4 :
        cardplyr = font.render(f"{cardname}♦", True, Red)
        screen.blit(cardplyr,(x_cardstartplyr, Y_cardstartplyr))
        pygame.draw.rect(screen, yellowish, Cardsplyrpos, 2)
        x_cardstartplyr+= x_abstand
    else:
        return
    
def Kartendlr(cardname ):
    global x_cardstartdlr    
    symbol = random.randint(1,4)
    Cardsdlrpos = pygame.Rect(x_cardstartdlr - 10, Y_cardstartdlr-10, 100, 140)

    if symbol ==1 :
        carddlr = font.render(f"{cardname}♠", True, Black)
        screen.blit(carddlr, (x_cardstartdlr, Y_cardstartdlr))
        pygame.draw.rect(screen, yellowish, Cardsdlrpos, 2)
        x_cardstartdlr+= x_abstanddlr
    elif symbol ==2 :
        carddlr = font.render(f"{cardname}♣", True, Black)
        screen.blit(carddlr,(x_cardstartdlr, Y_cardstartdlr))
        pygame.draw.rect(screen, yellowish, Cardsdlrpos, 2)
        x_cardstartdlr+= x_abstanddlr
    elif symbol ==3 :
        carddlr = font.render(f"{cardname}♥", True, Red)
        screen.blit(carddlr,(x_cardstartdlr, Y_cardstartdlr))
        pygame.draw.rect(screen, yellowish, Cardsdlrpos, 2)
        x_cardstartdlr+= x_abstanddlr
    elif symbol == 4 :
        carddlr = font.render(f"{cardname}♦", True, Red)
        screen.blit(carddlr,(x_cardstartdlr, Y_cardstartdlr))
        pygame.draw.rect(screen, yellowish, Cardsdlrpos, 2)
        x_cardstartdlr+= x_abstanddlr
    else:
        return

def Kartennameundwert():
    global name1, wert1, name2, wert2, dealeins, dealvalone, dealzwei, dealvaltwo
    global gesplayer, gesdealr, gesplayerstr, gesdealrstr, dealvalonestr
    global playergesamtscore, dlrgesscorepos, dealergesamtscore
    global dealergesamtscorehdn, dlrgesscoreposhdn, plyrgesscorepos
    name1, wert1 = kartenname(karteEins)
    name2, wert2 = kartenname(karteZwei)
    dealeins, dealvalone = kartenname(dealerEins)
    dealzwei, dealvaltwo = kartenname(dealerZwei)
    gesplayer = wert1 + wert2
    gesdealr = dealvalone + dealvaltwo

#variablen für die Anzeige der Gesamtwerte und Layout + Löschen der alten Werte
def gesvalue():
    global gesplayer, gesdealr, dealeins, dealzwei, playergesamtscore, dlrgesscorepos,dealergesamtscore
    global dealergesamtscorehdn, dlrgesscoreposhdn, plyrgesscorepos, dealvalone, gesdealrstr, gesplayerstr
    global dealvalonestr
    gesplayerstr = str(gesplayer)
    gesdealrstr = str(gesdealr)
    dealvalonestr = str(dealvalone)
    dealergesamtscore = font.render(gesdealrstr, True, Black)
    dlrgesscorepos = dealergesamtscore.get_rect(center=(1100, 20))
    dealergesamtscorehdn = font.render(dealvalonestr, True, Black)
    dlrgesscoreposhdn = dealergesamtscorehdn.get_rect(center=(1100, 20))
    playergesamtscore = font.render(gesplayerstr, True, Black)
    plyrgesscorepos = playergesamtscore.get_rect(center=(1100, 680))

    #cover old scores
    plyroldscorerect =pygame.Rect(1080, 660, 150, 50)
    dlroldscorerect = pygame.Rect(1080, 0, 150, 50)
    screen.fill( White, plyroldscorerect)  
    screen.fill(White, dlroldscorerect)
    pygame.display.update(plyroldscorerect)
    pygame.display.update(dlroldscorerect)

def displaycards():
    
    gesvalue()
    Kartenplyr(name1)
    Kartenplyr(name2)
    Kartendlr(dealeins)
    print("Deine Karten:", name1, "und", name2,"Gesamt:", gesplayer)
    screen.blit(playergesamtscore, plyrgesscorepos)
    print("Dealer:", dealeins, "und", "Unknown", "Gesamt:", dealvalone)
    screen.blit(dealergesamtscorehdn, dlrgesscoreposhdn)

def printendscore():
    global gesplayer, gesdealr, dealeins, dealzwei, G, zustand, bjp, bjd, Jetons, jetons_Einsatz
    gesvalue()

    if bjp == True and bjd == True:
        print("Unentschieden, beide hatten Blackjack")
        screen.blit(drawtxt, drawtxt_rect)
        Jetons += jetons_Einsatz
        jetons_Einsatz = 0    
    
    elif bjp == True and bjd == False:
        print("Du hattest Blackjack, Dealer nicht")
        screen.blit(bjplayer, bjplayer_rect)
        Jetons += (jetons_Einsatz * 2.25)
        jetons_Einsatz = 0
    
    elif bjd == True and bjp == False:
        print("Dealer hatte Blackjack, du nicht")
        screen.blit(bjdealer, bjdealer_rect)
        jetons_Einsatz = 0
    
    elif gesdealr < gesplayer < 21 or gesdealr > 21 and gesplayer <= 21 :
        print("Du hast gewonnen! Dealer hatte", gesdealr, "Du hattest", gesplayer)
        screen.blit(gewonnentxt, gewonnentxt_rect)
        Jetons += (jetons_Einsatz * 2)
        jetons_Einsatz = 0
    
    elif gesplayer < gesdealr < 21 or gesplayer > 21 and gesdealr <= 21:
        print("Du hast verloren. Dealer hatte", gesdealr, "Du hattest", gesplayer)
        screen.blit(verlorentxt, verlorentxt_rect)
        jetons_Einsatz = 0

    elif gesplayer == gesdealr:
        print("Unentschieden! Dealer hatte", gesdealr, "Du hattest", gesplayer)
        screen.blit(drawtxt, drawtxt_rect)
        Jetons += jetons_Einsatz
        jetons_Einsatz = 0
        
def Pass():
        global gesdealr, dealeins, dealzwei, gesplayer, G, zustand
        gesvalue()
        screen.blit(playergesamtscore, plyrgesscorepos)
        screen.blit(dealergesamtscore, dlrgesscorepos)
        print("Dealer:", dealeins, "und", dealzwei, "→ Startwert:", gesdealr)
        Kartendlr(dealzwei)

        while gesdealr < 17:
            newCard = NeueKarte()
            dealnew, dealvalnew = kartenname(newCard)
            gesdealr += dealvalnew
            Kartendlr(dealnew)
            gesvalue()
            screen.blit(playergesamtscore, plyrgesscorepos)
            screen.blit(dealergesamtscore, dlrgesscorepos)

            if gesdealr > 21 and (dealeins == "A" or dealzwei == "A" or dealnew == "A") and ADealer < 1:
                gesdealr = gesdealr -10
                gesvalue()
                ADealer += 1
                screen.blit(playergesamtscore, plyrgesscorepos)
                screen.blit(dealergesamtscore, dlrgesscorepos)
            if gesdealr > 21:
                print("Dealer hat sich überkauft! Du hast gewonnen")
                pygame.time.wait(1000)
                zustand ="blackjackende"
                G=0
                return
            pygame.time.wait(100)

        print("Endwert Dealer:", gesdealr)
        zustand = "blackjackende"
        G = 0
  
def ziehen():
                global A, player_turn, gesplayer, gesdealr, dealeins, dealzwei, G, zustand, name3, wert3, karteDrei
                karteDrei = NeueKarte()
                
                name3, wert3 = kartenname(karteDrei)
                gesplayer = wert1 + wert2 + wert3 
                gesvalue()
                screen.blit(playergesamtscore, plyrgesscorepos)
                screen.blit(dealergesamtscore, dlrgesscorepos)
                print("Deine Karten:", name1, ",", name2, "und", name3, "Gesamt:", gesplayer)                
                Kartenplyr(name3)
                print("Dealer:", dealeins, "und", "Unkown", "Gesamt:", dealvalone)
    
                if gesplayer > 21 and (name1 == "A" or name2 == "A" or name3 == "A"):
                    gesplayer = gesplayer -10
                    gesvalue()
                    screen.blit(playergesamtscore, plyrgesscorepos)
                    screen.blit(dealergesamtscore, dlrgesscorepos)
                    A = A + 1
                if gesplayer > 21:
                    print("Verloren, überkauft!")
                    print("Dealer:", dealeins, "und", dealzwei, "Gesamt:", gesdealr)
                    Kartendlr(dealzwei)
                    gesvalue()
                    screen.blit(playergesamtscore, plyrgesscorepos)
                    screen.blit(dealergesamtscore, dlrgesscorepos)
                    zustand = "blackjackende"
                    G = 0
                else:
                    print("Noch eine Karte? [j/n]")

def ziehentwo():
                global A, player_turn, gesplayer, gesdealr, dealeins, dealzwei, G, zustand, name4, wert4, karteVier
                global name3, wert3
                karteVier = NeueKarte()
                
                name4, wert4 = kartenname(karteVier)
               
                gesplayer = wert1 + wert2 + wert3 + wert4
                gesvalue()
                screen.blit(playergesamtscore, plyrgesscorepos)
                screen.blit(dealergesamtscore, dlrgesscorepos)
                print("Deine Karten:", name1, ",", name2, ",", name3,"und", name4, "Gesamt:", gesplayer)                
                Kartenplyr(name4)
                print("Dealer:", dealeins, "und", "Unkown", "Gesamt:", dealvalone)
    
                if gesplayer > 21 and (name1 == "A" or name2 == "A" or name3 == "A" or name4 == "A"):
                    gesplayer = gesplayer -10
                    gesvalue()
                    screen.blit(playergesamtscore, plyrgesscorepos)
                    screen.blit(dealergesamtscore, dlrgesscorepos)
                    A = A + 1
                if gesplayer > 21:
                    print("Verloren, überkauft!")
                    print("Dealer:", dealeins, "und", dealzwei, "Gesamt:", gesdealr)
                    Kartendlr(dealzwei)
                    gesvalue()
                    screen.blit(playergesamtscore, plyrgesscorepos)
                    screen.blit(dealergesamtscore, dlrgesscorepos)
                    zustand = "blackjackende"
                    G = 0
                else:
                    Pass()
                    
def Tabulator():
                global gesplayer, gesdealr, dealeins, dealzwei, G, zustand, A, Jetons, jetons_Einsatz
                karteDrei = NeueKarte()
                name3, wert3 = kartenname(karteDrei)
                gesplayer = wert1 + wert2 + wert3 
                gesvalue()
                screen.blit(playergesamtscore, plyrgesscorepos)
                screen.blit(dealergesamtscore, dlrgesscorepos)
                print("Deine Karten:", name1, ",", name2, "und", name3, "Gesamt:", gesplayer)
                Kartenplyr(name3)
                print("Dealer:", dealeins, "und", "Unkown", "Gesamt:", dealvalone)
                
                Jetons -= jetons_Einsatz
                jetons_Einsatz *= 2
                Jetonsanzeige()
                
                if gesplayer > 21 and (name1 == "A" or name2 == "A" or name3 == "A"):
                    gesplayer = gesplayer -10
                    gesvalue()
                    screen.blit(playergesamtscore, plyrgesscorepos)
                    screen.blit(dealergesamtscore, dlrgesscorepos)
                    A=A+1
                if gesplayer > 21:
                    print("Verloren, überkauft!")
                    print("Dealer:", dealeins, "und", dealzwei, "Gesamt:", gesdealr)
                    Kartendlr(dealzwei)
                    gesvalue()
                    screen.blit(playergesamtscore, plyrgesscorepos)
                    screen.blit(dealergesamtscore, dlrgesscorepos)
                    pygame.time.wait(1000)
                    zustand = "blackjackende"
                    G=0
                else:
                    Pass()

def blackjack ():
    global gesplayer, gesdealr, dealeins, dealzwei, G, zustand, A, aktion, karteEins, karteZwei, dealerEins, dealerZwei
    global name1, wert1, name2, wert2, dealeins, dealvalone, dealzwei, dealvaltwo
    global bjp, bjd
    global player_turn, endprint
    karteEins = NeueKarte()
    karteZwei = NeueKarte()
    dealerEins = NeueKarte()
    dealerZwei = NeueKarte()
    Kartennameundwert()
    print("Neue Karten erfogreich gezogen")
    displaycards()
    
    if gesplayer == 21:
        print("Gesamt: Blackjack" )
        print("Dealer:", dealeins, dealzwei)
        Kartendlr(dealzwei)
        gesvalue()
        screen.blit(playergesamtscore, plyrgesscorepos)
        screen.blit(dealergesamtscore, dlrgesscorepos)
        if gesdealr == gesplayer :
            print("Unentschieden, Dealer hatte auch Blackjack")
            pygame.time.wait(1000)
            zustand = "blackjackende"
            bjp = True
            bjd = True
            G=0
        else:
            print("Dealer hatte ", gesdealr, "Du hast gewonnen!")
            pygame.time.wait(1000)
            zustand = "blackjackende"
            bjp = True
            bjd = False
            G=0 

    else:
        if gesdealr == 21:
            print("Dealer:", dealeins, "und", dealzwei,"Gesamt:", gesdealr)
            Kartendlr(dealzwei)
            gesvalue()
            screen.blit(playergesamtscore, plyrgesscorepos)
            screen.blit(dealergesamtscore, dlrgesscorepos)
            print("Du hast verloren, Dealer hatte Blackjack")
            pygame.time.wait(1000)
            zustand = "blackjackende"
            G=0
            
        else:
            print("Whats your next move? Double[Tab], Pass[p], Card[c] ?")
            return

#Funktion zum Zurücksetzen des Spiels        
def reset_blackjack():
    global gesplayer, gesdealr, x_cardstartplyr, x_cardstartdlr, y_title, zustand, G, A
    global x_abstand, x_abstanddlr, y_title, aktion, player_turn
    global name1, wert1, name2, wert2, dealeins, dealvalone, dealzwei, dealvaltwo, endprint
    global player_turn, endprint, Y_cardstartplyr, Y_cardstartdlr, ADealer, action_state

    gesplayer = 0
    gesdealr = 0
    x_cardstartplyr = 350
    x_cardstartdlr = 350
    y_title = -100
    screen.fill(White)
    zustand = "start"
    G = 0
    A = 0
    ADealer = 0
    aktion = None
    y_title = -100
    zustand = "start"
    x_cardstartplyr = 350
    x_abstand = 120
    Y_cardstartplyr = 560
    aktion = None
    action_state = 0
    

    x_cardstartdlr = 350
    x_abstanddlr = 120
    Y_cardstartdlr = 200
    
def doubleornothingrender():
    #Hier kommt der Code für den Double or Nothing Spielmodus hin
    global jetons_Gewinn, jetons_Einsatz, started
    if started == False:
        jetons_Gewinn = jetons_Einsatz 
        jetons_Einsatz = 0
        started = True
    screen.fill(White)
    winPotFont = pygame.font.SysFont("Arial", 60)
    winPotTxt = winPotFont.render(f"Gewinnpot: {jetons_Gewinn}", True, Black)
    winPotTxtRect = winPotTxt.get_rect(center=(640, 100))
    screen.blit(winPotTxt, winPotTxtRect)

def doubleornothing():
    global jetons_Gewinn, jetons_Einsatz, zustand, x, y
    symbolfont = pygame.font.SysFont("Arial", 50)
    winsymbol = symbolfont.render("✅", True, Green)
    losesymbol = symbolfont.render("❌", True, Red)

    pygame.draw.rect(screen, Black, (440, 500, 400, 70))
    doubleornothingbttn = font.render("Verdoppeln", True, White)
    screen.blit(doubleornothingbttn, (450, 510))
    pygame.draw.rect(screen, Black, (440, 600, 400, 70))
    takeprofitbttn = font.render("Gewinn nehmen", True, White)
    screen.blit(takeprofitbttn, (450, 610))
    if doubleornothingbttn.get_rect(topleft=(450, 510)).collidepoint(maus):
        pygame.draw.rect(screen, Red, (440, 500, 400, 70))
        doubleornothingbttn = font.render("Verdoppeln", True, White)
        if event.type == pygame.MOUSEBUTTONDOWN:
            probability = random.randint(1, 2)
            if probability == 1:
                print("Du hast verloren! Alles weg!")
                screen.blit(losesymbol, (x, y))
                jetons_Gewinn = 0
                zustand = "doubleornothingende"
            else:
                print("Verdoppelt!")
                screen.blit(winsymbol, (x, y))
                x += 100
                y += 100
                jetons_Gewinn *= 2
                

            pygame.time.wait(1000)

    if takeprofitbttn.get_rect(topleft=(450, 610)).collidepoint(maus):
        pygame.draw.rect(screen, Red, (440, 600, 400, 70))
        if event.type == pygame.MOUSEBUTTONDOWN:
            takeprofitbttn = font.render("Gewinn nehmen", True, White)
            Jetons += jetons_Gewinn
            jetons_Gewinn = 0
            pygame.time.wait(1000)

def doubleornothingreset():
    global x, y
    x=100
    y=200

#ESC Button Funktion
def ESCBTN(event):
        global zustand, click, maus, keys, escbutton, esctxt, running
        if escbutton.collidepoint(maus):
            pygame.draw.rect(screen, Red, escbutton)
            if event.type == pygame.MOUSEBUTTONDOWN :
                if zustand == "start":
                    running = False
                elif zustand == "blackjack" or zustand == "blackjackende" :
                    
                    reset_blackjack()
                    update_everything()
                    print("Spiel zurückgesetzt!")
                    zustand = "start"
                    
                    pygame.time.wait(500)
                elif zustand == "shop":
                    zustand = "start"
                    
                    pygame.time.wait(500)
                elif zustand == "doubleornothing" or zustand == "doubleornothingende":
                    
                    reset_blackjack()
                    update_everything()
                    print("Spiel zurückgesetzt!")
                    zustand = "start"
                    
                    pygame.time.wait(500)
                     
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if zustand == "start":
                running = False
            elif zustand == "blackjack" or zustand == "blackjackende":
                zustand = "start"
                reset_blackjack()
                print("Spiel zurückgesetzt!")
                pygame.time.wait(500)
            elif zustand == "shop":
                zustand = "start"
                pygame.time.wait(500)
        else:
            pygame.draw.rect(screen, Black, escbutton)
            text_rect = esctxt.get_rect(center=escbutton.center)
            screen.blit(esctxt, text_rect)  

def ChangeGamemode():
    global blackjackstartscreen, doubleornothingstartscreen
    if blackjackstartscreen == True:
        pygame.draw.polygon(screen, Lightblue, [ (100, 350), (100, 500), (25, 425)])
        gamemodeswitch=pygame.Rect(25, 350, 75, 150)
        if gamemodeswitch.collidepoint(maus):
            pygame.draw.polygon(screen, Blue, [ (100, 350), (100, 500), (25, 425)])
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if blackjackstartscreen == True:
                    blackjackstartscreen = False
                    doubleornothingstartscreen = True
                elif doubleornothingstartscreen == True:
                    doubleornothingstartscreen = False
                    blackjackstartscreen = True
                pygame.time.wait(300)
                print("Spielmodus gewechselt!")
    elif doubleornothingstartscreen == True:
        pygame.draw.polygon(screen, Lightblue, [ (1175, 350), (1175, 500), (1250, 425)])
        gamemodeswitch=pygame.Rect(1150, 350, 75, 150)
        if gamemodeswitch.collidepoint(maus):
            pygame.draw.polygon(screen, Blue, [ (1175, 350), (1175, 500), (1250, 425)])
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if blackjackstartscreen == True:
                    blackjackstartscreen = False
                    doubleornothingstartscreen = True
                elif doubleornothingstartscreen == True:
                    doubleornothingstartscreen = False
                    blackjackstartscreen = True
                pygame.time.wait(300)
                print("Spielmodus gewechselt!")
    
def startscreenrender():
        screen.fill(White)
        global y_title, zustand, maus, click, startbutton, starttxt, title, Jetons, slider_percent, blackjackstartscreen, doubleornothingstartscreen
        if y_title < 200:
            y_title += 5
        
        if blackjackstartscreen == True and doubleornothingstartscreen == False:
            title = bjtitle_font.render("Blackjack", True, Black)
            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, y_title))
        elif doubleornothingstartscreen == True:
            title = dontitle_font.render("Double or Nothing", True, Black)
            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, y_title))
    
        slider()
        #Start BJ button
        if blackjackstartscreen == True:
            if startbutton.collidepoint(maus):
                pygame.draw.rect(screen, Red, startbutton)
                if event.type == pygame.MOUSEBUTTONDOWN:
                        zustand = "blackjack"
                        jetons_Einsatz = int(slider_percent * Jetons)
                        Jetons -= jetons_Einsatz
                        print("Spiel beginnt!")
            
            else:
                pygame.draw.rect(screen, Green, startbutton)
            text_rect = starttxt.get_rect(center=startbutton.center)
            screen.blit(starttxt, text_rect)
        elif doubleornothingstartscreen == True:
            if startbutton.collidepoint(maus):
                pygame.draw.rect(screen, Red, startbutton)
                if event.type == pygame.MOUSEBUTTONDOWN:
                        zustand = "doubleornothing"
                        jetons_Einsatz = int(slider_percent * Jetons)
                        Jetons -= jetons_Einsatz
                        print("Spiel beginnt!")
            
            else:
                pygame.draw.rect(screen, Green, startbutton)
            text_rect = starttxt.get_rect(center=startbutton.center)
            screen.blit(starttxt, text_rect)

        #ESC button
        ESCBTN(event)
        
def blackjackrender_p_and_d():
    
    screen.blit(dealer, dealerpos)
    screen.blit(player, playerpos)
    screen.blit(playergesamttxt, playergesamtpos)
    screen.blit(dealergesamttxt, dealergesamtpos)

Shopfont = pygame.font.SysFont("Segoe UI Emoji", 60)
Shoptxtin = Shopfont.render("Shop", True, Black)
Shoptxtout = font.render("Shop", True, Black)
def Shopbutton(event):
    global shopbtn, zustand, shop_rect
    shopbtn = pygame.Rect(1150, 20, 100, 40)
    if shopbtn.collidepoint(maus):
        pygame.draw.rect(screen, yellowish, shopbtn)
        if event.type == pygame.MOUSEBUTTONDOWN:
            zustand = "shop"
            print("Shop geöffnet")
    else:
        pygame.draw.rect(screen, Yellow, shopbtn)
    shop_rect = Shoptxtout.get_rect(center=shopbtn.center)
    screen.blit(Shoptxtout, shop_rect)

def slotsymbol(slot):
    symbols = {
        1: "♠",
        2: "▲",
        3: "#",
        4: "■",
        5: "♣",
        6: "❖",
        7: "7",
        8: "$",
    }
    return symbols.get(slot)
   
slotfont = pygame.font.SysFont("Arial", 72)
def Slotmaschine():
    global slot1, slot2, slot3, slot4, slot1_symbol, slot2_symbol, slot3_symbol, slot4_symbol
    global slot1_text, slot2_text, slot3_text, slot4_text
    slot1 = random.randint(1, 8)
    slot2 = random.randint(1, 8)
    slot3 = random.randint(1, 8)
    slot4 = random.randint(1, 8)

    slot1_symbol = slotsymbol(slot1)
    slot2_symbol = slotsymbol(slot2)
    slot3_symbol = slotsymbol(slot3)
    slot4_symbol = slotsymbol(slot4)

    print(f"Slot 1: {slot1_symbol}, Slot 2: {slot2_symbol}, Slot 3: {slot3_symbol}, Slot 4: {slot4_symbol}")
    slot1_text = slotfont.render(slot1_symbol, True, Black)
    slot2_text = slotfont.render(slot2_symbol, True, Black)
    slot3_text = slotfont.render(slot3_symbol, True, Black)
    slot4_text = slotfont.render(slot4_symbol, True, Black)




    if slot1 == slot2 == slot3 == slot4:
        print("Jackpot! Du hast gewonnen!")
        if slot1 == 8:
            print("Du hast 10000 Jetons gewonnen!")
            global Jetons
            Jetons += 10000
        elif slot1 == 7:
            print("Du hast 7500 Jetons gewonnen!")
            Jetons += 7500
        elif slot1 == 6:
            print("Du hast 5000 Jetons gewonnen!")
            Jetons += 5000
        elif slot1 == 5 or slot1 == 4 :
            print("Du hast 2500 Jetons gewonnen!")
            Jetons += 2500
        elif slot1 == 3 or slot1 == 2 or slot1 == 1:
            print("Du hast 1000 Jetons gewonnen!")
            Jetons += 1000
    else:
        if slot1 == 8 or slot1 == 7 or slot1 == 6 or slot1 == 5 or slot1 == 4 or slot1 == 3 or slot1 == 2 or slot1 == 1:
            print(f"Du hast {slot1* 50} Jetons gewonnen!")
            Jetons += 50 * slot1
        if slot2 == 8 or slot2 == 7 or slot2 == 6 or slot2 == 5 or slot2 == 4 or slot2 == 3 or slot2 == 2 or slot2 == 1:
            print(f"Du hast {slot2* 50} Jetons gewonnen!")
            Jetons += 50 * slot2
        if slot3 == 8 or slot3 == 7 or slot3 == 6 or slot3 == 5 or slot3 == 4 or slot3 == 3 or slot3 == 2 or slot3 == 1:
            print(f"Du hast {slot3* 50} Jetons gewonnen!")
            Jetons += 50 * slot3
        if slot4 == 8 or slot4 == 7 or slot4 == 6 or slot4 == 5 or slot4 == 4 or slot4 == 3 or slot4 == 2 or slot4 == 1:
            print(f"Du hast {slot4* 50} Jetons gewonnen!")
            Jetons += 50 * slot4
    update_everything()

slot1_text = font.render("", True, Black)
slot2_text = font.render("", True, Black) 
slot3_text = font.render("", True, Black)
slot4_text = font.render("", True, Black)

def Shopseite():
    global zustand, running, maus, click, startbutton, starttxt, title, Shoptxtin, Shoptxtout, Belohnung, slot1, slot2, slot3, slot4
    global slot1_symbol, slot2_symbol, slot3_symbol, slot4_symbol
    global slot1_text, slot2_text, slot3_text, slot4_text
    global Belohnung
    screen.fill(White)
    Shoptxtpos = Shoptxtin.get_rect(center=(640, 60))
    screen.blit(Shoptxtin,Shoptxtpos)

    pygame.draw.rect(screen, Black, pygame.Rect(180, 100, 200, 500), 2)
    pygame.draw.rect(screen, Black, pygame.Rect(430, 100, 200, 500), 2)
    pygame.draw.rect(screen, Black, pygame.Rect(680, 100, 200, 500), 2)
    pygame.draw.rect(screen, Black, pygame.Rect(930, 100, 200, 500), 2)

    screen.blit(slot1_text, (280, 300))
    screen.blit(slot2_text, (530, 300))
    screen.blit(slot3_text, (780, 300))
    screen.blit(slot4_text, (1030, 300))

    slotbtn = pygame.Rect(610, 650, 100, 50)
    slotbtntxt = font.render("Spin", True, Black)
    slotbtntxtpos = slotbtntxt.get_rect(center=slotbtn.center)
    screen.blit(slotbtntxt, slotbtntxtpos)

    with open("Blackjack.json", "r") as f:
        data = json.load(f)
        saved_time = datetime.fromisoformat(data["start"])
        elapsed = datetime.now() - saved_time

    

    if elapsed.total_seconds() >= 86400:  # 86400 Sekunden = 24 Stunden
        Belohnung += 1
        start_time = datetime.now()
        with open("Blackjack.json", "w") as f:
            json.dump({"start": start_time.isoformat()}, f)
        print("Startzeit gespeichert:", start_time)
    
    if slotbtn.collidepoint(maus):
        if Belohnung > 0:
            pygame.draw.rect(screen, Green, slotbtn)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("startet Slotmaschiene")
                Belohnung -= 1
                Slotmaschine()
                update_everything()
                pygame.time.wait(1000)
                
        else:
            pygame.draw.rect(screen, Red, slotbtn)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Du hast keine Belohnung mehr übrig")
                print(f"Vergangene Zeit: {elapsed}")
        screen.blit(slotbtntxt, slotbtntxtpos)
    else:
        pygame.draw.rect(screen, yellowish, slotbtn)
        screen.blit(slotbtntxt, slotbtntxtpos)

def Jetonsanzeige():
    global jetons_Einsatz, Einsatztext, Einsatztextpos, Jetons
    Einsatztext = font.render(f"Einsatz: {jetons_Einsatz}", True, Black)
    Einsatztextpos = Einsatztext.get_rect(bottomleft=(20, 650))
    screen.blit(Einsatztext, Einsatztextpos)

    Jetonsanzeigetxt = font.render(f"Jetons: {Jetons}", True, Black)
    Jetonsanzeigetxtpos = Jetonsanzeigetxt.get_rect(bottomleft= (20, 700))
    screen.blit(Jetonsanzeigetxt, Jetonsanzeigetxtpos)

def endprintscreen():
    global endprint, zustand, endtxt_rect
    if endprint == False:
        Jetonsanzeige()
        screen.fill(White)
        endtxt = font.render("Spiel beendet! Drücke ESC oder Menü um zum Startblitschirm zurückzukehren", True, Black)
        
        screen.blit(endtxt, endtxt_rect)
        endprint = True
        printendscore()
    if menuButton.collidepoint(maus):
        pygame.draw.rect(screen, Lightblue, menuButton)
        if event.type == pygame.MOUSEBUTTONDOWN:
            endprint = False
            reset_blackjack()
            doubleornothingreset()
            update_everything()
            zustand = "start"
            pygame.time.wait(500)
            
    else:
        pygame.draw.rect(screen, Blue, menuButton)
    text_rect = menuTxt.get_rect(center=menuButton.center)
    screen.blit(menuTxt, text_rect)
    

player_turn = 0
action_state = 0 
running = True
clock = pygame.time.Clock()
zustand = "start"
while running:
    maus = pygame.mouse.get_pos()
    
    click = pygame.mouse.get_pressed()
    
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        if zustand == "start"and event.type == pygame.MOUSEBUTTONDOWN :
            if abs(pygame.mouse.get_pos()[0] - knob_x) < knob_radius:
                dragging = True            
        elif zustand == "start" and event.type == pygame.MOUSEBUTTONUP:
            dragging = False    
        if event.type == pygame.KEYDOWN and zustand == "start":
            if event.key == pygame.K_LEFT:
                knob_x = max(slider_rect.x, knob_x - 10)
            elif event.key == pygame.K_RIGHT:
                knob_x = min(slider_rect.x + slider_rect.width, knob_x + 10)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PLUS and zustand == "start":
            if Jetons < 10000000 or Belohnung < 10:
                Jetons += 10000
                Belohnung += 1
                print("Jetons erhöht auf:", Jetons)
                update_everything()

        if action_state==0 and zustand == "blackjack" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                aktion = "pass"
                action_state = 1
            elif event.key == pygame.K_c:
                aktion = "ziehen"
                player_turn += 1
                action_state = 1
            elif event.key == pygame.K_TAB:
                aktion = "double"
                action_state = 1
            
        if action_state >= 1 and zustand == "blackjack" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                aktion ="jo bro"
                player_turn += 1
            elif event.key == pygame.K_n:
                aktion = "nein bro"
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
            print(maus)

    if zustand == "start" and Jetons > 0:
        startscreenrender()
        Shopbutton(event)
        Jetonsanzeige()
        ChangeGamemode()
        
    elif zustand =="blackjack":
        blackjackrender_p_and_d()
        Jetonsanzeige()
        zustand = "blackjack"
        if G ==0:
            screen.fill(White)
            blackjack()
            G=1
            if jetons_Einsatz <= Jetons:
                screen.blit(nextmove, nextmovepos)
            else:
                screen.blit(nextmoveohnetab, nextmoveohnetabpos)
        if aktion == "pass":
            Pass()
            screen.blit(covermove,covermovepos)
            aktion = None
            action_state= 1
            zustand = "blackjackende"
        elif aktion == "ziehen":
            ziehen()
            aktion = None
            action_state= 1
            
            #Noch eine Karte? [j/n]
            screen.blit(covermove,covermovepos)
            screen.blit(ziehensecnd,ziehensecndpos)
        elif aktion == "double" and jetons_Einsatz <= Jetons:
            Tabulator()
            screen.blit(covermove,covermovepos)
            aktion = None
            action_state= 1
        if action_state == 1 and aktion == "jo bro":
            ziehentwo()
            action_state += 1
            aktion = None
        elif action_state == 1 and aktion == "nein bro":
            Pass()
            action_state += 1
            aktion = None 

    elif zustand == "blackjackende":
        endprintscreen()
        
    
    elif zustand == "doubleornothing":
        doubleornothingrender()
        Jetonsanzeige()
        doubleornothing()  

    elif zustand == "doubleornothingende":
        endprintscreen()

    elif zustand == "shop":
        Shopseite()

    ESCBTN(event)        
    if Jetons <= 0 and zustand == "start":
        screen.fill(Red)
        alljetonslost = bjtitle_font.render("YOU LOST EVERYTHING!", True, Black)
        screen.blit(alljetonslost, (640 - alljetonslost.get_width() // 2, 360 - alljetonslost.get_height() // 2))
        
        lostbttn = font.render("Reset Game", True, White)
        text_rect = lostbttn.get_rect(center=startbutton.center)
        screen.blit(lostbttn, text_rect)
        if startbutton.collidepoint(maus):
            pygame.draw.rect(screen, Gray, startbutton)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Fortschritt wird zurückgesetzt...")
                os.remove("Blackjack.json")
                running = False
        else:
            pygame.draw.rect(screen, Gray, startbutton)
        lostbttn = font.render("Close Game", True, White)
        text_rect = lostbttn.get_rect(center=startbutton.center)
        screen.blit(lostbttn, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
import sys
sys.exit()
