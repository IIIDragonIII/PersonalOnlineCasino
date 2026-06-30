import os
import random

class Jetons:
    #Währungssystem
    if not os.path.exists("jetons.txt"):
        with open("jetons.txt", "w") as f:
            f.write("10000")
    
    def Einsatz(self):
        with open("jetons.txt", "r") as f:
            jetons = int(f.read())
        while True:
            try:
                einsatz = int(input("Wie viele Jetons möchten Sie setzen? "))
                if einsatz > jetons:
                    print("Sie haben nicht genug Jetons. Bitte setzen Sie einen niedrigeren Betrag.")
                elif einsatz <= 0:
                    print("Bitte setzen Sie einen positiven Betrag.")
                else:
                    print(f"Sie haben {einsatz} Jetons gesetzt.")
                    with open("jetons.txt", "w") as f:
                        f.write(str(jetons - einsatz))
                    return einsatz
            except ValueError:
                print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")
    def Auszahlung(self, einsatz, BJ):
        with open("jetons.txt", "r") as f:
            jetons = int(f.read())
        if BJ:
            gewinn = round((einsatz * 2.25), 0)
            with open("jetons.txt", "w") as f:
                f.write(str(jetons + gewinn))
        else:
            gewinn = einsatz * 2
            with open("jetons.txt", "w") as f:
                f.write(str(jetons + gewinn))

class Blackjack:
    #Kartendeck und Kartenfunktionen erstellen
    karten = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    symbole = ["♠", "♥", "♦", "♣"]
    kartenstapel = []
    kartenWert = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
    spieler_blackjack = False
    dealer_blackjack = False
    no_comparison = False
    dealer_win = False
    spieler_win = False
    cause = ""

    def DeckErstellen(self):
        for symbol in self.symbole:
            for karte in self.karten:
                self.kartenstapel.append((karte, symbol))
    def Mischen(self):
        random.shuffle(self.kartenstapel)
    def Ziehen(self):
        if len(self.kartenstapel) > 0:
            gezogen = self.kartenstapel.pop()
            wert = self.kartenWert[gezogen[0]]
            anzeige = f"{gezogen[1]}{gezogen[0]}"
            return anzeige, wert
        else:
            print("Der Kartenstapel ist leer.")
            return None
    def KartenBlackjack(self, spieler_gesamt_wert, dealer_gesamt_wert):
        if spieler_gesamt_wert == 21:
            self.spieler_blackjack = True
            self.no_comparison = True
            return self.spieler_blackjack
        elif dealer_gesamt_wert == 21:
            self.dealer_blackjack = True
            self.no_comparison = True
            return self.dealer_blackjack
    def ÜberEinundzwanzig(self, spieler_gesamt_wert, dealer_gesamt_wert):
        
        if spieler_gesamt_wert > 21:
            self.dealer_win, self.cause = True, "Spieler hat über 21"
        elif dealer_gesamt_wert > 21:
            self.spieler_win, self.cause = True, "Dealer hat über 21"
    def EndKartenWert(self, spieler_gesamt_wert, dealer_gesamt_wert):
        if spieler_gesamt_wert > dealer_gesamt_wert:
            self.spieler_win, self.cause = True, "Spieler hat mehr"
        elif spieler_gesamt_wert < dealer_gesamt_wert:
            self.dealer_win, self.cause = True, "Dealer hat mehr"
        elif spieler_gesamt_wert == dealer_gesamt_wert:
            self.cause = "Unentschieden"

    def GameVariableReset(self):
        self.spieler_blackjack = False
        self.dealer_blackjack = False
        self.no_comparison = False